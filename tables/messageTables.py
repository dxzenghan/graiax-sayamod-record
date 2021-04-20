import os
from datetime import datetime

from pony.orm import *


db = Database()

class GroupMessage(db.Entity):
    id = PrimaryKey(int, auto=True)
    dateTime = Required(datetime, precision=6)
    groupId = Required(str)  # 群号
    memberId = Required(str)  # 成员 QQ 号
    plain = Required(str)  # 消息的文本内容

# 每个 orm 文件必须要有一下两行代码
db.bind(provider='sqlite',
        filename=os.path.join(os.getenv("DB_FILEPATH"), os.getenv("SQLITE_DB_NAME")),
        create_db=True)
db.generate_mapping(create_tables=True)


