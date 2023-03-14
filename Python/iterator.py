# iterator 


__iter__
my_iterator = iter(my_list)


__next__
next(my_iterator))



# generator
generator_1 = (x*x for x in range(3))
generator_1

def func(n):
    for x in range(n):
        yield x*x
        
generator_2 = func(3)
generator_2

next(generator_2)






# hasNext() and next()



