import asyncio
import concurrent.futures
import os

from graia.application.event.messages import GroupMessage
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, Source
from graia.application.group import Group, Member

from graia.saya import Saya, Channel
from graia.saya.event import SayaModuleInstalled
from graia.saya.builtins.broadcast.schema import ListenerSchema

from pony.orm import *


saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[SayaModuleInstalled]))
def initialize():
    # 创建模块文件夹
    os.environ.update(
        {
            "RECORD_STATIC_FILEPATH": os.path.join(
                os.getcwd(), "data", "graiax_sayamod_record"
            )
        }
    )

    if not os.path.exists(
        db_filepath := (os.path.join(os.environ.get("RECORD_STATIC_FILEPATH"), "db"))
    ):
        os.makedirs(db_filepath)

    from . import tables  # 初始化数据库


@channel.use(ListenerSchema(listening_events=[GroupMessage]))  # 填入你需要监听的事件
async def record(group: Group, member: Member, messageChain: MessageChain):
    if messageChain.has(Plain):

        @db_session
        def task():
            from .tables import GroupMessage

            GroupMessage(
                groupId=str(group.id),
                dateTime=messageChain.getFirst(Source).time,
                memberId=str(member.id),
                plain=messageChain.include(Plain).asDisplay(),
            )
            commit()

        with concurrent.futures.ThreadPoolExecutor() as excutor:
            saya.broadcast.loop.run_in_executor(excutor, task)
