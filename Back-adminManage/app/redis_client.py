"""Redis 缓存客户端。

为「用户管理统计卡片」提供缓存读写能力，采用 cache-aside 模式：
先查 Redis，命中直接返回；未命中则查询数据库，再把结果写入 Redis。
所有 Redis 异常都被捕获并降级为直连数据库，保证 Redis 挂了不影响主流程。
"""

import json
import logging

import redis

from .config import (
    REDIS_DB,
    REDIS_DECODE_RESPONSES,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
    REDIS_STATS_TTL,
)

logger = logging.getLogger(__name__)

# 全局 Redis 客户端（连接是惰性建立的，首次读写时才真正连接）
redis_client = redis.Redis(
    host=REDIS_HOST,                       # Redis 地址，默认 127.0.0.1
    port=REDIS_PORT,                       # Redis 端口，默认 6379
    db=REDIS_DB,                           # 使用的库编号，默认 0
    password=REDIS_PASSWORD,               # 密码，无则 None
    decode_responses=REDIS_DECODE_RESPONSES,  # 返回 str 而非 bytes，便于 json 处理
    protocol=2,                            # Windows 版 Redis 5.0 不支持 RESP3 / HELLO，强制走 RESP2
)


def get_redis():
    """获取全局 Redis 客户端实例，供依赖注入或其它模块直接使用。"""
    return redis_client


def stats_cache_key(page: int, page_size: int, keyword: str) -> str:
    """拼接统计缓存的 key。

    以「分页页码 + 每页条数 + 搜索关键字」作为缓存维度，
    不同查询条件使用不同的 key，避免缓存串数据。
    """
    return f"users:stats:{page}:{page_size}:{keyword or ''}"


def get_cached_stats(page: int, page_size: int, keyword: str):
    """读取统计缓存。

    命中返回反序列化后的 dict；未命中或 Redis 异常时返回 None，
    调用方拿到 None 后走数据库查询逻辑。
    """
    key = stats_cache_key(page, page_size, keyword)
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except redis.RedisError as exc:
        logger.warning("Redis read failed, falling back to database: %s", exc)
    return None


def set_cached_stats(page: int, page_size: int, keyword: str, stats: dict):
    """写入统计缓存，并设置过期时间（REDIS_STATS_TTL）。

    写入失败仅记录告警，不抛出异常，避免影响接口返回。
    """
    key = stats_cache_key(page, page_size, keyword)
    try:
        redis_client.set(key, json.dumps(stats), ex=REDIS_STATS_TTL)
    except redis.RedisError as exc:
        logger.warning("Redis write failed, skipping cache: %s", exc)


def invalidate_users_stats():
    """清空所有用户统计缓存。

    在用户增 / 删 / 改之后调用，保证缓存数据与数据库一致，
    下次请求会重新查库并写入新缓存。
    """
    try:
        for key in redis_client.scan_iter(match="users:stats:*"):
            redis_client.delete(key)
    except redis.RedisError as exc:
        logger.warning("Redis invalidation failed: %s", exc)
