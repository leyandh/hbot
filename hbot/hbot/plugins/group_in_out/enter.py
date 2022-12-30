# from nonebot.typing import overrides
# class a():
#     # @overrides(list)
#     def __init__(self,s:str) -> None: 
#         self.s = s
#     def p(self,):
#         return self.s
# def b(c:a):
#     d = c.p()
#     print(d)

# b(a('sb'))

# n=[1]
import requests
head = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
                }
params = {
    
    "size": 'original',
    "tag":  ['制服','ntr'],
    "r18": 1,
}
url = requests.get('https://api.lolicon.app/setu/v2', headers=head, params=params).json()
print(url)