import os
import timeit
import psutil
from Timer import Timer  # Ваш класс Timer
from ArmTimer import ArmTimer  # Ваш класс ArmTimer
from PySide6.QtCore import QTimer
import time

process = psutil.Process(os.getpid())

def example_callback():
    pass

def measure_performance(timer_class, interval, iterations, single_shot=False):
    cpu_usage_start = psutil.cpu_percent(interval=None)
    mem_usage_start = process.memory_info().rss / (1024 ** 2)  # В МБ


    def run_timer():
        timer = timer_class(interval=interval, callback=example_callback, single_shot=single_shot)
        timer.start()
        if not single_shot:
            time.sleep(interval * iterations)  # Подождать несколько интервалов
        timer.stop()

    execution_time = timeit.timeit(run_timer, number=1)

    cpu_usage_end = psutil.cpu_percent(interval=None)
    mem_usage_end = process.memory_info().rss / (1024 ** 2)  # В МБ

    cpu_usage = cpu_usage_end - cpu_usage_start
    mem_usage = mem_usage_end - mem_usage_start

    return execution_time, cpu_usage, mem_usage

# Тесты для Timer
execution_time, cpu_usage, mem_usage = measure_performance(Timer, interval=0.1, iterations=100)
print(f"Timer Performance: Time: {execution_time}s, CPU: {cpu_usage}%, Memory: {mem_usage}MB")

# Тесты для ArmTimer
execution_time, cpu_usage, mem_usage = measure_performance(ArmTimer, interval=0.1, iterations=100)
print(f"ArmTimer Performance: Time: {execution_time}s, CPU: {cpu_usage}%, Memory: {mem_usage}MB")

