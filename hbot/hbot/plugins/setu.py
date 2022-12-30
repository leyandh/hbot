from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.plugin import on_regex
import requests
from PIL import Image
import os
import re
import time
def get_setu(down=False)->str:
    url = requests.get('https://api.lolicon.app/setu/v2?r18=1').json()
    img_url:str = url['data'][0]['urls']['original']
    pid = url['data'][0]['pid']
    ext = url['data'][0]['ext']
    if down == True:
        res =requests.get(img_url)
        pic = res.content
        pic_path = 'C:/Users/leyandh/Desktop/bot_q/'+str(pid)+ext
        print("正在下载...")
        with open(pic_path, 'wb') as f:
            f.write(pic)
        try:
            image = Image.open(pic_path)  # 检查文件是否能正常打开
            image.verify()  # 检查文件完整性
            image.close()
            print("文件完好")
            return "good"
        except:
            os.remove(pic_path)
            print("文件错误")
            return "bad"
    return img_url
setu = on_regex("^涩图")
down_setu = on_regex("^下载涩图")
@setu.handle()
async def _(bot:Bot,event:Event):
    msg = event.get_plaintext()
    res = re.search(r"^涩图(tag.*){0,3}\*([0-9]*)$", msg)
    if res is not None:
        num = int(res[2])
        if 0 < num <= 10:
            for j in range(num):
                i = get_setu()
                await setu.send(MessageSegment.image(i), at_sender=True)
                time.sleep(0.1)
@down_setu.handle()
async def _(bot:Bot,event:Event):
    msg = event.get_plaintext()
    res = re.search(r"^下载涩图\*([0-9]*)$", msg)
    if res is not None:
        await setu.send(MessageSegment.text('开始下载...'), at_sender=True)
        num = int(res[1])
        good = 0
        bad = 0
        for j in range(num):
            i = get_setu(down = True)
            if i =='good':
                good+=1
            if bad =='bad':
                bad+=1
        message = f"下载成功{good}个，失败{bad}个"
        await setu.send(MessageSegment.text(message), at_sender=True)

