
from httpx import AsyncClient, HTTPError
from nonebot.log import logger
import asyncio
from PIL import Image
import os
from io import BytesIO
import base64

async def get_url(num: int, down_choose:int ,tags: list, r18 = 0) ->list:
    '''
    The number of setu is num
    Up to three tags
    0 is non-r18,1 is r18

    Usage:
    ```
        import asyncio
        tasks = [get_url(num = 1,tags = '白丝',r18 = 1),]
        asyncio.run(asyncio.wait(tasks))
    or

    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(get_url(num = 1,tags = '白丝',r18 = 1)),
        loop.create_task(get_url(num = 1,r18 = 0))
    ]

    loop.run_until_complete(asyncio.wait(tasks))
    print(tasks[0].result())
    print(tasks[1].result())
        
    ```
    '''
    head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    }
    
    params = {
        "r18": r18,
        "size": 'regular',
        "tag": tags,
    }
    async with AsyncClient(proxies=None) as client:

        datas = []
        url = f"https://api.lolicon.app/setu/v2?num={num}"
        try:
            res = await client.get(url=url, params=params, headers=head, timeout=None)
        except HTTPError as e:
            # logger.error(e)
            print('请求超时！')
        res = res.json()
        data = res['data']
        if not data:
            return ""
        datas.extend(data)  #请求num次，并将返回的json合并到数组
        
        img = await down_pic(datas, down_choose, r18) 
        print('ok')


async def down_pic(datas:list,down_choose:int , r18:int =0):

    async with AsyncClient(proxies=None) as client:
        head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    }
        for i in datas:
            img = i['urls']['regular']
            pid = i['pid']
            down_img = await client.get(img, headers=head, timeout=None)
            if r18:
                
                pic_path = './setu/r18/%s.png'%str(pid) #r18和非r18为两个目录，取决于r18为1 or 0
            else :
                pic_path = './setu/non-r18/%s.png'%str(pid)
            # pic_path = './'+str(pid)+'.png'


            if down_choose ==0:  #如果为假，就返回图片信息，否则下载图片
                info_pic = {'pid': pid,
                                'base64': f"base64://{base64.b64encode(BytesIO(down_img.content).getvalue()).decode()}"}
                return info_pic

            print("正在下载...")
            with open(pic_path, 'wb') as f:
                f.write(down_img.content)
            try:
                image = Image.open(pic_path)  # 检查文件是否能正常打开
                image.verify()  # 检查文件完整性
                image.close()
                print("文件完好")
            except:
                os.remove(pic_path)
                print("文件错误")



if __name__ == '__main__':


    # loop = asyncio.get_event_loop()
    
    # tasks = [
    #     loop.create_task(get_url(num = 20,tags = '白丝',down_choose=1,r18 = 1)),
    # ]

    # loop.run_until_complete(asyncio.wait(tasks))
    asyncio.run(get_url(num = 20,tags = '白丝',down_choose=1,r18 = 1))


