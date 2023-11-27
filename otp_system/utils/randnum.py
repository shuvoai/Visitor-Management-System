import random


class RandomNumberMixin:
    def generate_random_number(self, digit=6):
        return str(random.randint(10 ** (digit - 1), (10 ** digit) - 1))
