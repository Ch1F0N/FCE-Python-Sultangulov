"""
Напечатать в порядке возрастания первых n натуральных чисел, в разложение
которых на простые множители входят только числа 2,3,5.
Идея решения: введем три очереди x2, x3, x5 в которых будем хранить
элементы, которые соответственно в 2, 3, 5 раз больше напечатанных, но еще
не напечатаны. Рассмотрим наименьший из ненапечатанных элементов: пусть
это x. Тогда он делится нацело на одно из чисел 2, 3, 5; x находится в одной из
очередей и является в ней первым элементом (меньшие его уже напечатаны,
а элементы очередей не напечатаны). Напечатав x, нужно изъять его из
очереди и добавить в очередь кратные ему элементы. Длины очередей не
превосходят числа напечатанных элементов. Изначально в очередях хранится
по одному числу.
"""

class Node:
    """Узел односвязного списка."""

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    """Минимальная очередь FIFO на односвязном списке."""

    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, item):
        new_node = Node(item)
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node

    def dequeue(self):
        if self.head is None:
            print("Двухсторонняя очередь из пустой очереди!")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data

    def peek(self):
        if self.head is None:
            print("Выбор из пустой очереди!")
        return self.head.data


class UglyNumberGenerator:
    """Генерирует первые n чисел, чьи множители — только 2, 3, 5."""

    def generate(self, n):
        if n < 0:
            print("n должна быть >= 1")

        result = []

        x2, x3, x5 = LinkedQueue(), LinkedQueue(), LinkedQueue()
        x2.enqueue(2)
        x3.enqueue(3)
        x5.enqueue(5)

        while len(result) < n:
            a, b, c = x2.peek(), x3.peek(), x5.peek()

            if a <= b and a <= c:
                x = x2.dequeue()
            elif b <= a and b <= c:
                x = x3.dequeue()
            else:
                x = x5.dequeue()

            if not x2.is_empty() and x2.peek() == x:
                x2.dequeue()
            if not x3.is_empty() and x3.peek() == x:
                x3.dequeue()
            if not x5.is_empty() and x5.peek() == x:
                x5.dequeue()

            result.append(x)

            x2.enqueue(x * 2)
            x3.enqueue(x * 3)
            x5.enqueue(x * 5)

        return result


def factorize(number):
    """Определяет, входит ли в число простое 2,3,5 и в какой степени."""
    exps = {2: 0, 3: 0, 5: 0}
    for p in (2, 3, 5):
        while number % p == 0:
            exps[p] += 1
            number //= p
    return exps


def main():
    """Запрашивает n и выводит группы чисел по множителям."""
    gen = UglyNumberGenerator()
    while True:
        try:
            raw = input("Введите положительное целое число n (0 для выхода): ")
            n = int(raw)
            if n == 0:
                print("Выход.")
                return
            if n < 0:
                print("Ошибка: n должно быть > 0.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число.")
        except KeyboardInterrupt:
            print("\nВыход.")
            return

    try:
        nums = gen.generate(n)
    except KeyboardInterrupt:
        print("\nГенерация прервана.")
        return

    groups = {2: [], 3: [], 5: []}
    for num in nums:
        exp = factorize(num)
        for p in (2, 3, 5):
            if exp[p] > 0:
                groups[p].append(num)

    if groups[2]:
        print("Числа, в которые входят при разложении на множители цифра 2:")
        for x in groups[2]:
            print(x, end=" ")
        print()
    if groups[3]:
        print("Числа, в которые входят при разложении на множители цифра 3:")
        for x in groups[3]:
            print(x, end=" ")
        print()
    if groups[5]:
        print("Числа, в которые входят при разложении на множители цифра 5:")
        for x in groups[5]:
            print(x, end=" ")
        print()

if __name__ == "__main__":
    main()
