import logging
import queue
import time
from threading import Event, Thread
from typing import Optional, ClassVar


class Executor:
    """
    Класс, умеющий запускать указанные коллбеки в порядке очереди.

    Для использования необходимо указать количество worker-ов.

    Для добавления коллбеков используется метод .submit(). В него
    следует передать коллбек. Callback будет вызван когда подойдёт его очередь.

    Методом .stop() можно остановить работу исполнителя.

    Например:

    >>> from classic.executor import Executor
    ...
    ... executor = Executor(workers_num=1)
    ...
    ... def some_task():
    ...     print('Hello, world!')
    ...
    ... executor.submit(some_task)
    ... executor.stop(block=True) # Дожидается остановки
    """

    _workers_num: int
    _inbox: queue.Queue
    _logger: logging.Logger
    _stopped: Event
    _threads: list[Thread]

    TIMEOUT: ClassVar[float] = 0.001

    def __init__(
            self,
            workers_num: int,
            inbox: Optional[queue.Queue] = None,
            logger: Optional[logging.Logger] = None
    ) -> None:
        self._workers_num = workers_num
        self._inbox = inbox or queue.Queue()
        self._logger = logger or logging.getLogger('Executor')
        self._stopped = Event()
        self._threads = []
        for _ in range(self._workers_num):
            thread = Thread(target=self._execute)
            self._threads.append(thread)
            thread.start()

    def submit(
            self, callback, block: bool = True, timeout: Optional[float] = None
    ) -> None:
        """
        Запрашивает добавление callback-а в очередь исполнителя.

        Если параметры не указаны: 'block' - true, а 'timeout' - None,
        блокирует очередь до тех пор, пока не появится свободный слот.
        Если 'timeout' - неотрицательное число, то блокировка длится
        не более 'timeout' секунд и вызывает исключение Full,
        если в течение этого времени свободный слот не был доступен.
        В противном случае ('block' = false), если свободный слот доступен,
        то элемент помещается в очередь немедленно, иначе вызывается
        исключение Full ('timeout' в этом случае игнорируется).
        """
        self._inbox.put(callback, block, timeout)

    def _execute(self) -> None:
        """
        Запуск исполнителя в текущем потоке.
        Метод блокирует исполнение, пока не будет запрошена остановка извне.
        Аналогичен методу run у Thread.
        """
        while not self._stopped.is_set():
            try:
                callback = self._inbox.get(timeout=self.TIMEOUT)
            except queue.Empty:
                continue
            try:
                callback()
            except Exception as exception:
                self._logger.exception(exception)

    def stop(self, block: bool = True, timeout: Optional[float] = None) -> None:
        """
        Запрашивает остановку потока исполнителя.
        Исполнитель будет остановлен не сразу, а после вызова всех callback-ов!
        """
        self._stopped.set()
        if block:
            if timeout:
                for thread in self._threads:
                    started_at = time.monotonic()
                    thread.join(timeout=timeout)
                    timeout -= time.monotonic() - started_at
                    if timeout <= 0.0:
                        break
            else:
                for thread in self._threads:
                    thread.join()

    def __del__(self) -> None:
        self.stop(block=True)
