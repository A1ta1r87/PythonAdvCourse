# import random
# import time
# from threading import Thread, Lock
#
# counter = 0
# _lock_counter = Lock()
#
# class MyThread(Thread):
#     """
#     A threading example
#     """
#
#     def __init__(self, name):
#         """Инициализация потока"""
#         Thread.__init__(self)
#         self.name = name
#
#     def run(self):
#         """Запуск потока"""
#         global counter
#
#         for i in range(10000000):
#             # _lock_counter.acquire()
#             counter += 1
#             # _lock_counter.release()
#
#
# def create_threads():
#     """
#     Создаем группу потоков
#     """
#
#     for i in range(10):
#         name = "Thread #%s" % (i + 1)
#         my_thread = MyThread(name)
#         my_thread.start()
#
#
#
# if __name__ == "__main__":
#     create_threads()
#     print(counter)
a = 5
print(f'{a:5}')
