from httpx import AsyncClient, HTTPError
# from nonebot.log import logger
import asyncio
from PIL import Image
import os
from io import BytesIO
import base64
from typing import List,Union
import json
from tqdm import tqdm
async def down_pic(datas:List[dict] ,down_choose:int , r18:int =0)->Union[list,dict]:
    async with AsyncClient(proxies=None) as client:
        head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        'referer': 'https://www.pixiv.net/'
    }
        tmp_ok:int=0 #下载成功的个数
        tmp_bad:int=0 #下载失败的个数
        bad_list:List[dict]=[] #失败链接datas
        pbar = tqdm(datas, desc='Downloading', colour='green') #进度条
        for i in datas:
            img:str = i['urls']['regular']
            pid:int = i['pid']
            ext:str = i['ext']
            down_img = await client.get(img, headers=head, timeout=None) #下载图片
            pbar.update(1)
            if r18: pic_path = './setu/r18/%s.%s'%(str(pid),ext) #r18和非r18为两个目录，取决于r18为1 or 0
            else : pic_path = './setu/non-r18/%s.%s'%(str(pid),ext)
            if down_choose ==0:  #如果为假，就返回图片信息，否则下载图片
                info_pic = {'pid': pid,
                            'base64': f"base64://{base64.b64encode(BytesIO(down_img.content).getvalue()).decode()}"
                }
                return info_pic
            with open(pic_path, 'wb') as f:
                f.write(down_img.content)
            try:
                image = Image.open(pic_path)  # 检查文件是否能正常打开
                image.verify()  # 检查文件完整性
                image.close()
                print("文件完好")
                tmp_ok+=1
            except:
                os.remove(pic_path)
                print("文件错误")
                tmp_bad+=1
                bad_list.append(i) 
        pbar.close()    
        return [tmp_ok,tmp_bad,bad_list] #返回一个列表包含两个为int的下载状态,一个失败列表
async def get_url(num: int, down_choose:int ,tags: Union[list,str,None]=None, r18:int = 0) :
    head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    }
    params = {
        "r18": r18,
        "size": 'regular',
        "tag": tags,
    }
    async with AsyncClient(proxies=None) as client:

        datas:List[dict] = []
        url = f"https://api.lolicon.app/setu/v2?num={num}"
        try:
            res = await client.get(url=url, params=params, headers=head, timeout=10.0) #获取图片链接
            res = json.loads(res.text)
            data:list = res['data']
            if not data:
                return ""
            datas.extend(data)  #请求num次，并将返回的json合并到数组
            img = await down_pic(datas, down_choose, r18) 
            print(f'下载成功{img[0]}个')
            print(f'下载失败{img[1]}个')
            print('失败链接:')
            out:str = ''
            for i in img[2]:
                tag = ''
                for a in i['tags']: tag=tag+","
                out += i['urls']['regular']+":"+tag+"\n"
            print(out)
        except HTTPError as e:
            # logger.error(e)
            print('请求超时！')
if __name__ == '__main__':
    asyncio.run(get_url(num = 20,down_choose=1,r18 = 1))
    # loop = asyncio.get_event_loop()
    # tasks = [
    #     loop.create_task(get_url(num = 20,tags = '白丝',down_choose=1,r18 = 1)),
    # ]
    # loop.run_until_complete(asyncio.wait(tasks))


