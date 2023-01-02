from typing import Any


class test():
    def __init__(self, text) -> None:
        self.text = text
    def __getitem__(self, index):
        return self.text[index]
    def __setitem__(self,index,val)->Any:
        self.text[index] = val
        
a = test("Helle World!")
for i in a:
    print(i)
print(a[:])
a[1]="6"
print(a[:])
