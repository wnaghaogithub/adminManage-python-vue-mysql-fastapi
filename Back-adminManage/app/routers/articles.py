from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Article
from ..schemas import ArticleCreate, ArticleOut, ArticlePageOut, ArticleUpdate
from .auth import get_current_admin

router = APIRouter(prefix="/api", tags=["articles"])

_ALLOWED_TYPES = {"厨艺", "科学", "编程"}


def _to_out(a: Article) -> ArticleOut:
    return ArticleOut(
        id=a.id,
        title=a.title,
        image=a.image,
        type=a.type,
        content=a.content,
        create_time=a.create_time,
    )


@router.get("/articles", response_model=ArticlePageOut)
def list_articles(
    page: int = 1,
    page_size: int = 10,
    keyword: str = "",
    type: str = "",
    db: Session = Depends(get_db),
    _: Article = Depends(get_current_admin),
):
    query = db.query(Article)
    if keyword:
        query = query.filter(Article.title.like(f"%{keyword}%"))
    if type:
        query = query.filter(Article.type == type)
    total = query.count()
    articles = (
        query.order_by(Article.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return ArticlePageOut(total=total, items=[_to_out(a) for a in articles])


@router.post("/articles", response_model=ArticleOut, status_code=201)
def create_article(
    data: ArticleCreate,
    db: Session = Depends(get_db),
    _: Article = Depends(get_current_admin),
):
    if data.type not in _ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="文章类型仅支持：厨艺 / 科学 / 编程")
    article = Article(
        title=data.title,
        image=data.image,
        type=data.type,
        content=data.content,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return _to_out(article)


@router.put("/articles/{article_id}", response_model=ArticleOut)
def update_article(
    article_id: int,
    data: ArticleUpdate,
    db: Session = Depends(get_db),
    _: Article = Depends(get_current_admin),
):
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    fields = data.model_dump(exclude_unset=True)
    if "type" in fields and fields["type"] is not None:
        if fields["type"] not in _ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="文章类型仅支持：厨艺 / 科学 / 编程")
    for key in ("title", "image", "type", "content"):
        if key in fields and fields[key] is not None:
            setattr(article, key, fields[key])
    db.commit()
    db.refresh(article)
    return _to_out(article)


@router.delete("/articles/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    _: Article = Depends(get_current_admin),
):
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(article)
    db.commit()
    return {"message": "删除成功"}
