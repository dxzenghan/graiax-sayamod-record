from graia.application.event.messages import GroupMessage
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain, Source
from graia.application.group import Group, Member

from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from pony.orm import *

from . import tables

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]  # 填入你需要监听的事件
                            ))
@db_session
async def record(group: Group, member: Member, messageChain: MessageChain):
    if messageChain.has(Plain):
        tables.messageTables.GroupMessage(
            groupId=str(group.id),
            dateTime=messageChain.getFirst(Source).time,
            memberId=str(member.id),
            plain=messageChain.include(Plain).asDisplay())
        commit()