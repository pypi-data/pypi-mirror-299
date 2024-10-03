import time

from sources.classic.executor.executor import Executor

result = None


def change_result():
    global result
    result = 'Ok'


def test_executor():
    executor = Executor(workers_num=1)
    executor.submit(change_result)
    time.sleep(0.001)
    executor.stop()
    assert result == 'Ok'
