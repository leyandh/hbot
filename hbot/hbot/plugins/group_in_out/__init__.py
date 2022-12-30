from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Message,GroupIncreaseNoticeEvent,Bot


gid = []
welcome=on_notice()
@welcome.handle()
async def do(bot: Bot, event: GroupIncreaseNoticeEvent):
    user = event.get_user_id()
    at_ = "欢迎！：[CQ:at,qq={}]".format(user)
    msg = at_ + '大佬加入聊天组'

    print(at_)
    if event.group_id == gid:
        await welcome.finish(message=Message(f'{msg}'))
    else:
        await welcome.finish(message = "欢迎新人")