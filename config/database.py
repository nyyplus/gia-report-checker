from motor.motor_asyncio import AsyncIOMotorClient
from environs import Env

env = Env()
env.read_env()

connection = AsyncIOMotorClient(
    env.str("MONGODB_HOST"),
    env.int("MONGODB_PORT")
)
db = connection[env.str("MONGODB_DBNAME")]
table_tasks = db["tasks"]
table_gia_reports = db["reports"]
