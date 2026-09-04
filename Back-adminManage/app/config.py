import base64
import hashlib
import os

# ---- 数据库 ----
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "root1234567")
DB_NAME = os.environ.get("DB_NAME", "managedata_base")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}?charset=utf8mb4"
)

# ---- JWT ----
JWT_SECRET = os.environ.get("JWT_SECRET", "admin-manage-secret-key-please-change")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

# ---- 密码可逆加密（Fernet）----
# 需求要求前端可切换显示明文密码，故采用可逆加密而非单向哈希
def _derive_fernet_key() -> str:
    return base64.urlsafe_b64encode(
        hashlib.sha256(b"admin-manage-fernet-key-v1").digest()
    ).decode()

FERNET_KEY = os.environ.get("FERNET_KEY", _derive_fernet_key())

# ---- 上传目录 ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

# ---- Redis 缓存 ----
REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_DB = int(os.environ.get("REDIS_DB", "0"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None) or None
REDIS_DECODE_RESPONSES = True
REDIS_STATS_TTL = int(os.environ.get("REDIS_STATS_TTL", "3600"))
