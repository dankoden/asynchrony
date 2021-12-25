# Конструкция yield from берет на себя передачу данных, передачу исключений, получает возращаемый
# с помощью return результат который дополнительно можно было бы обработать. В других
# языках даная конструкция называется await. И смысл в том что вызывающий код напрямую управляет работой
# подгенератора, и пока это происходит делегирующий генератор заблокированный! Есть важный момент ,
# подгенератор должен содержать в себе механизм завершающий его работу!
# Строго говоря можно сказать еще что конструкция yield from генерит нам результат с переданого итератора
def a():
    yield from "ihor"

for i in a():
    print(i)

def courutine(func):
    def inner(*args,**kwargs):
        g = func(*args,**kwargs)
        g.send(None)
        return g

    return inner


def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print(f"&&&&&& {message} &&&&&&&")
    return "Returned from subgen"

@courutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except Exception:
    #         g.throw(Exception)
    res = yield from g
    print(res)


# sb = subgen()
# g = delegator(sb)
# g.send("hello")
# g.throw(StopIteration)