# classic-thread-pool-executor

Библиотека дает простой класс Executor для исполнения задач в порядке очереди.

Для использования необходимо передать количество worker-ов.

Для добавления callback-ов используется метод .submit(). В него
следует передать callback. Callback будет вызван когда подойдёт его очередь.

Методом .stop() можно остановить работу исполнителя.

Например:
```python
from classic.executor import Executor

executor = Executor(workers_num=1)

def some_task():
    print('Hello, world!')

executor.submit(some_task)
executor.stop(block=True) # Дожидается остановки
```
