import aioredis
from src.config import Config

JTI_EXPIRY=3600

token_blocklist=aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async def add_jti_to_block(jti:str)->None:
    print("-------------------")
    print("-------------------")

    print(jti)
    print("-------------------")
    print("-------------------")

    await token_blocklist.set(
        name=jti,
        value="blocked",
        ex=JTI_EXPIRY
    )



async def token_in_blockList(jti:str)->bool:
    jti =await token_blocklist.get(jti)

    print("-------------------")
    print(jti)
    print("-------------------")
    return jti is not None