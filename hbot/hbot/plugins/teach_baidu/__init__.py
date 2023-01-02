from nonebot.params import RegexGroup
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.plugin import on_regex


baidu = on_regex(f"^百度搜索(.+)")

async def get_baidu(keyword:str) -> str:
    url = f'https://lab.magiconch.com/buhuibaidu.me/?s={keyword}'
    return url
@baidu.handle()
async def _(bot:Bot,event:Event,foo = RegexGroup()):
    msg=await get_baidu(foo[0])
    await baidu.finish(message='拿去用吧'+msg)

