import jwt
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Admin
from ..schemas import LoginRequest, TokenResponse
from ..security import create_access_token, decode_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == data.username).first()
    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_access_token(str(admin.id))
    return TokenResponse(token=token, username=admin.username)


@router.post("/logout")
def logout():
    # JWT 无状态方案：前端清除本地 token 即完成退出
    return {"message": "退出成功"}


def get_current_admin(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
) -> Admin:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录或登录已过期")
    token = authorization[7:]
    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    admin = db.query(Admin).get(int(payload["sub"]))
    if not admin:
        raise HTTPException(status_code=401, detail="登录状态无效")
    return admin
