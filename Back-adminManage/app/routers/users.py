import os
import shutil
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..config import UPLOAD_DIR
from ..database import get_db
from ..models import User
from ..redis_client import get_cached_stats, invalidate_users_stats, set_cached_stats
from ..schemas import PageOut, UserCreate, UserOut, UserStatsOut, UserUpdate
from ..security import decrypt_password, encrypt_password
from .auth import get_current_admin

router = APIRouter(prefix="/api", tags=["users"])

_ALLOWED_IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}


def _to_out(u: User) -> UserOut:
    return UserOut(
        id=u.id,
        username=u.username,
        province=u.province,
        city=u.city,
        area=u.area,
        avatar=u.avatar,
        age=u.age,
        password=decrypt_password(u.password),
        create_time=u.create_time,
    )


@router.get("/users", response_model=PageOut)
def list_users(
    page: int = 1,
    page_size: int = 10,
    keyword: str = "",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    query = db.query(User)
    if keyword:
        query = query.filter(User.username.like(f"%{keyword}%"))
    total = query.count()
    users = (
        query.order_by(User.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return PageOut(total=total, items=[_to_out(u) for u in users])


@router.get("/users/stats", response_model=UserStatsOut)
def get_user_stats(
    page: int = 1,
    page_size: int = 10,
    keyword: str = "",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    cached = get_cached_stats(page, page_size, keyword)
    if cached:
        return UserStatsOut(**cached)

    query = db.query(User)
    if keyword:
        query = query.filter(User.username.like(f"%{keyword}%"))

    total = query.count()
    users = (
        query.order_by(User.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    page_count = len(users)
    avg_age = round(sum(u.age for u in users) / page_count, 1) if page_count else 0.0

    stats = UserStatsOut(total=total, page_count=page_count, avg_age=avg_age)
    set_cached_stats(page, page_size, keyword, stats.model_dump())
    return stats


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = User(
        username=data.username,
        province=data.province,
        city=data.city,
        area=data.area,
        avatar=data.avatar,
        age=data.age,
        password=encrypt_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    invalidate_users_stats()
    return _to_out(user)


@router.put("/users/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    fields = data.model_dump(exclude_unset=True)
    if "username" in fields and fields["username"]:
        exists = (
            db.query(User)
            .filter(User.username == fields["username"], User.id != user_id)
            .first()
        )
        if exists:
            raise HTTPException(status_code=400, detail="用户名已存在")
        user.username = fields["username"]
    if "password" in fields and fields["password"]:
        user.password = encrypt_password(fields["password"])
    for key in ("province", "city", "area", "avatar", "age"):
        if key in fields and fields[key] is not None:
            setattr(user, key, fields[key])
    db.commit()
    db.refresh(user)
    invalidate_users_stats()
    return _to_out(user)


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    invalidate_users_stats()
    return {"message": "删除成功"}


@router.post("/upload")
def upload_avatar(
    file: UploadFile = File(...),
    _: User = Depends(get_current_admin),
):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in _ALLOWED_IMAGE_EXT:
        raise HTTPException(status_code=400, detail="仅支持图片文件")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as out:
        shutil.copyfileobj(file.file, out)
    return {"url": f"/uploads/{filename}"}
