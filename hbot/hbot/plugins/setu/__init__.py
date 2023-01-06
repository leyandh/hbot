from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment,GroupMessageEvent
from nonebot.plugin import on_regex,on_command
import re
import time
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from get_setu import get_setu

group_r18 = []

Setu = on_regex("^涩图")
down_setu = on_command("下载涩图", permission= SUPERUSER)

@Setu.handle()
async def _(bot:Bot,event:GroupMessageEvent):
    msg = event.get_plaintext()
    res = re.search(r"^涩图(tag.*){0,1}", msg)
    if event.group_id in group_r18:r18 = 1
    else:r18 = 0
    if res is not None and res!='':
        if res[1] is not None:
            tag:list = res[1].replace('tag',',')[1:].split(",")
        else:
            tag=[]
        i = await get_setu(r18 = r18, tags=tag)
        if i =='未找到tag' or i=='tag最多三个哟~':
            await Setu.send(MessageSegment.text(i), at_sender=True)

        else:
            await Setu.send(MessageSegment.image(i), at_sender=True)
        time.sleep(0.1)

@down_setu.handle()
async def _(bot:Bot,event:Event):
    msg = event.get_plaintext()
    res = re.search(r"^下载涩图\*([0-9]*)$", msg)
    if res is not None:
        await Setu.send(message =MessageSegment.text('开始下载...'), at_sender=True)
        num = int(res[1])
        good = 0
        bad = 0

        for j in range(num):
            i = await get_setu(r18 = 0, down = True)
            if i =='good':
                good+=1
            if i =='bad':
                bad+=1
        message = f"下载成功{good}个，失败{bad}个"
        await Setu.send(message = MessageSegment.text(message), at_sender=True)