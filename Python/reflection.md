Reflection is a language's ability to **inspect** and **dynamically call** classes, methods, attributes, etc. at runtime.


```py
# routing example

class Person:
    def __int__(self, name):
        self.name = name

    def eat(self, food):
        print(f"I love eat {food}")


def rout(url):
    uris = url.split("&")
    mapping = {}
    for uri in uris:
        u = uri.split('=')
        mapping[u[0]] = u[1]
        
    obj = globals()[mapping.get('cls')]()
    func = getattr(obj, mapping.get('method')) # hasattr, getattr, setattr
    func(mapping.get('value'))
    
    
    
route("cls=Person&method=eat&value=meat")

```
[link](https://www.jianshu.com/p/4175f21a18c7)      
[reference](https://www.liujiangblog.com/course/python/48)




