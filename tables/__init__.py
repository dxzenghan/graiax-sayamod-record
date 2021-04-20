import os

db_filepath = config_db_filepath if (
    config_db_filepath := os.getenv("DB_FILEPATH")) else os.path.join(
        os.getcwd(), "data", "graiax_sayamod_record", "db")
if not os.path.exists(db_filepath):
    os.makedirs(db_filepath)
os.putenv("DB_FILEPATH", db_filepath)

sqlite_db_name = sqlite_db_name if (sqlite_db_name := os.getenv("SQLITE_DB_NAME")) else "graiaxDB.sqlite"
os.putenv("SQLITE_DB_NAME", sqlite_db_name)
os.environ.update({
    "DB_FILEPATH": db_filepath,
    "SQLITE_DB_NAME": sqlite_db_name
})

# 定义好的 orm 在此引用注册
from . import messageTables




