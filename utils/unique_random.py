import random
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock = Lock()  # 锁对象，确保线程安全

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class UniqueRandomGenerator(metaclass=SingletonMeta):
    def __init__(self, history_size=100000):
        self.history_size = history_size
        self.generated_numbers = set()
        self.pool = []
        self._fill_pool()

    def _fill_pool(self):
        while len(self.pool) < self.history_size:
            new_random = random.randint(10 ** 12, 10 ** 13 - 1)
            if new_random not in self.generated_numbers:
                self.generated_numbers.add(new_random)
                self.pool.append(new_random)

    def _generate(self):
        if not self.pool:
            self._fill_pool()
        return self.pool.pop()

    @staticmethod
    def generate():
        instance = UniqueRandomGenerator()
        return instance._generate()


if __name__ == '__main__':
    print(UniqueRandomGenerator.generate())
    print(UniqueRandomGenerator.generate())
