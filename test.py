def test():
    for i in range(10):
        yield i

tt = test()
for x in tt:
    print(x)

    if x == 4:
        print('oh its 4')

        x = next(tt)
        print('heres the last one', x)
        break