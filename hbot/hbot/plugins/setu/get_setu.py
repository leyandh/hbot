
import requests
from PIL import Image
import os
import time
from httpx import AsyncClient, HTTPError
from typing import Union


async def get_setu(r18 , tags:Union[str,list]='', down=False)->str:
    if len(tags)>3:
        return 'tag最多三个哟~'

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
        async with AsyncClient(proxies=None) as client:
            img_url:str = url['data'][0]['urls']['original']
            if down == True:
                pid:int = url['data'][0]['pid']
                ext:str = url['data'][0]['ext']
                res =await client.get(url = img_url,headers=head, timeout=None)
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
    except HTTPError:
        return '返回超时'
    except Exception as e:
        return '未找到tag'
        # return '未找到tag/'+str(e)        
    
