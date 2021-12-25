

def courutine(func):
    def inner(*args,**kwargs):
        g = func(*args,**kwargs)
        g.send(None)
        return g

    return inner

@courutine
def subgen():
    x = "Ready to accept message"
    message = yield x
    print("Subgen recivied",message)


@courutine
def average():
    count = 0
    sum = 0
    average = 0
    while True:
        try:
            x = yield average
        except StopIteration:
            print("Done")
        else:
            count += 1
            sum += x
            average = round(sum/count,2)
