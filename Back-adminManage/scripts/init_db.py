"""初始化数据库：建库 -> 建表 -> 写入管理员与真实感用户数据。

用法：python -m scripts.init_db
"""

import pymysql
from sqlalchemy import text

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.database import Base, SessionLocal, engine
from app.models import Admin, Article, User
from app.security import encrypt_password, hash_password

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

SEED_ARTICLES = [
    (
        "家常红烧肉的详细做法",
        "",
        "厨艺",
        "<p>红烧肉是一道经典的家常菜。选用肥瘦相间的五花肉，先焯水去腥，再小火慢炖上色，"
        "加入冰糖、生抽、老抽和八角桂皮，炖至软糯收汁即可。关键在火候：先大火烧开，再转小火焖 40 分钟。</p>",
    ),
    (
        "为什么天空是蓝色的",
        "",
        "科学",
        "<p>阳光是由多种颜色的光混合而成的。当阳光穿过大气层时，空气中的分子会把波长较短的蓝光"
        "散射到四面八方，所以我们抬头看到的天空呈现蓝色。这就是瑞利散射。</p>",
    ),
    (
        "Python 快速入门指南",
        "",
        "编程",
        "<p>Python 是一门简洁易学的高级编程语言。学习顺序建议：先掌握变量、数据类型、条件与循环，"
        "再理解函数、模块和类，最后用 FastAPI 或 Django 搭建一个 Web 服务。</p>",
    ),
]

SEED_USERS = [
    ("张伟", "北京市", "市辖区", "朝阳区", 28, "Zhangwei888"),
    ("王芳", "上海市", "市辖区", "浦东新区", 32, "Wangfang123"),
    ("李娜", "广东省", "广州市", "天河区", 25, "Lina2024"),
    ("刘洋", "浙江省", "杭州市", "西湖区", 30, "Liuyang666"),
    ("陈静", "江苏省", "南京市", "鼓楼区", 27, "Chenjing521"),
    ("杨帆", "四川省", "成都市", "武侯区", 33, "Yangfan0808"),
    ("赵敏", "湖北省", "武汉市", "洪山区", 29, "Zhaomin123"),
    ("黄磊", "陕西省", "西安市", "雁塔区", 35, "Huanglei888"),
    ("周婷", "山东省", "青岛市", "市南区", 26, "Zhouting0717"),
    ("吴强", "福建省", "厦门市", "思明区", 31, "Wuqiang2023"),
    ("徐丽", "湖南省", "长沙市", "岳麓区", 28, "Xuli520520"),
    ("孙涛", "河南省", "郑州市", "金水区", 34, "Suntao6666"),
    ("马超", "重庆市", "市辖区", "渝北区", 30, "Machao1234"),
    ("朱琳", "安徽省", "合肥市", "蜀山区", 27, "Zhulin0808"),
    ("胡军", "辽宁省", "沈阳市", "和平区", 36, "Hujun666888"),
    ("郭婷", "云南省", "昆明市", "五华区", 25, "Guoting123"),
    ("何伟", "河北省", "石家庄市", "长安区", 32, "Hewei2022"),
    ("高翔", "吉林省", "长春市", "南关区", 29, "Gaoxiang0909"),
    ("林静", "海南省", "海口市", "美兰区", 31, "Linjing0520"),
    ("罗成", "贵州省", "贵阳市", "南明区", 33, "Luocheng777"),
    ("梁宇", "江西省", "南昌市", "红谷滩区", 26, "Liangyu111"),
    ("宋佳", "山西省", "太原市", "小店区", 30, "Songjia1234"),
    ("郑爽", "黑龙江省", "哈尔滨市", "南岗区", 28, "Zhengshuang1"),
    ("冯磊", "内蒙古自治区", "呼和浩特市", "新城区", 35, "Fenglei8888"),
]


def create_database():
    conn = pymysql.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, connect_timeout=5
    )
    with conn.cursor() as cur:
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
    conn.commit()
    conn.close()


def seed():
    with SessionLocal() as db:
        # 管理员
        if not db.query(Admin).filter(Admin.username == ADMIN_USERNAME).first():
            db.add(
                Admin(
                    username=ADMIN_USERNAME,
                    password_hash=hash_password(ADMIN_PASSWORD),
                )
            )
            print(f"[+] 管理员已创建：{ADMIN_USERNAME} / {ADMIN_PASSWORD}")

        # 用户
        if db.query(User).count() == 0:
            for username, province, city, area, age, password in SEED_USERS:
                db.add(
                    User(
                        username=username,
                        province=province,
                        city=city,
                        area=area,
                        age=age,
                        password=encrypt_password(password),
                    )
                )
            db.commit()
            print(f"[+] 已写入 {len(SEED_USERS)} 条用户数据")
        else:
            print("[=] users 表已有数据，跳过用户种子写入")

        # 文章
        if db.query(Article).count() == 0:
            for title, image, type_, content in SEED_ARTICLES:
                db.add(
                    Article(
                        title=title,
                        image=image,
                        type=type_,
                        content=content,
                    )
                )
            db.commit()
            print(f"[+] 已写入 {len(SEED_ARTICLES)} 条文章数据")
        else:
            print("[=] articles 表已有数据，跳过文章种子写入")

        # 检查字符集
        result = db.execute(text("SELECT @@character_set_database, @@collation_database")).fetchone()
        print(f"[i] 数据库字符集：{result[0]} / {result[1]}")


if __name__ == "__main__":
    print(f"[*] 连接数据库 {DB_USER}@{DB_HOST}:{DB_PORT}")
    create_database()
    print(f"[*] 数据库 {DB_NAME} 已就绪，开始建表")
    Base.metadata.create_all(bind=engine)
    print("[+] 数据表已创建")
    seed()
    print("[√] 初始化完成")
