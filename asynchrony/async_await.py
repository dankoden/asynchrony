# Для понимании библиотеки Asincyo нужно понимать основной принцип асиннхронности а
# это наш event_loop . Нужно понимать как он работает. Который является менеджером , планировщиком
# задач, и суть его работы заключается в реагировании на происходящии
# события. Тоесть Работу можно описать такой фразой:"Когда случается событие А отреагируем на него вызовом B"
# В данном модуле мы заменили форму записи yield from на await , сделали запись async def , которая нам говорит о том
# что данная функция будет корутиной(сопрограмой) , крутится в событийном цикле
# также подключили модуль asyncio , НАША цель составить список задач (корутин) которые будут выполнятся
# в событийном цикле


import asyncio
import inspect

async def print_num():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(0.5)


async def print_time():
    count = 0
    while True:
        count += 1
        if count % 3 == 0:
            print(f"{count} have passed seconds")
        await asyncio.sleep(0.5)


async def main():
    task1 = asyncio.create_task(print_num()) # Создаем задачу
    task2 = asyncio.create_task(print_time()) # Создаем задачу

    await asyncio.gather(task1,task2) # Планирует события!



if __name__ == "__main__":
    asyncio.run(main())