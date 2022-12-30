from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.plugin import on_regex
import requests
from PIL import Image
import os
import re
import time
from typing import Union

import time
class do:
    def __init__(self) -> None:
        pass
    def get_setu(self, r18:int=1, tags:Union[str,list]='', down=False)->str:

        head = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
                }
        params = {
            "r18": r18,
            "size": 'original',
            "tag": tags,
        }
        url = requests.get('https://api.lolicon.app/setu/v2', headers=head, params=params).json()
        try:
            img_url:str = url['data'][0]['urls']['original']
            if down == True:
                pid:int = url['data'][0]['pid']
                ext:str = url['data'][0]['ext']
                res =requests.get(url = img_url,headers=head, timeout=None)
                pic = res.content
                # pic_path = 'C:/Users/leyandh/Desktop/bot_q/'+str(pid)+ext
                pic_path = f"se/{'r18/' if r18 else 'non-r18/'}{pid}.{ext}"
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
        except Exception:
            return '未找到tag'
        


Setu = on_regex("^涩图")
down_setu = on_regex("^下载涩图")

@Setu.handle()
async def _(bot:Bot,event:Event):
    msg = event.get_plaintext()
    res = re.search(r"^涩图(tag.*){0,3}\*{0,1}([0-9]*)$", msg)
    if res is not None and res!='':
        if res[2] !='':
            num = int(res[2])
        else : num=1
        if  0 < num <= 10:
            if res[1] is not None:
                tag = res[1].replace('tag',',')[1:].split(",")
            else:
                tag=[]
            setu = do()
            for j in range(num):
                i =  setu.get_setu(tags=tag)
                if i =='未找到tag':
                    await Setu.send(MessageSegment.text(i), at_sender=True)
                else:
                    await Setu.send(MessageSegment.image(i), at_sender=True)
                time.sleep(0.1)
@down_setu.handle()
async def _(bot:Bot,event:Event):
    msg = event.get_plaintext()
    res = re.search(r"^下载涩图\*([0-9]*)$", msg)
    if res is not None:
        await Setu.send(MessageSegment.text('开始下载...'), at_sender=True)
        num = int(res[1])
        good = 0
        bad = 0
        setu = do()
        for j in range(num):
            i = setu.get_setu(down = True)
            if i =='good':
                good+=1
            if i =='bad':
                bad+=1
        message = f"下载成功{good}个，失败{bad}个"
        await Setu.send(MessageSegment.text(message), at_sender=True)

