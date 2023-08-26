# generator
# a special type of function that returns an iterator
def generator(n):  
    i = 0
    while i < n:
        yield i
        i += 1
      
for i in generator(3):
    print(i)
  
# generator expression
gen = (i for i in range(5))

for i in gen:
    print(i)


# iterator
arr = [4, 7, 0]
iterator = iter(arr)

for i in iterator:
    print(i)

# custom iterator
# for a class to be considered an iterator, it needs to implement __iter__() and __next__()
class Container:    
    def __init__(self, size):
        self.size = size
        self.index = 0
      
    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.size:
            raise StopIteration
        
        v = self.index
        self.index += 1
        return v

obj = Container(5)
iterator = iter(obj)
print(next(iterator))
  
