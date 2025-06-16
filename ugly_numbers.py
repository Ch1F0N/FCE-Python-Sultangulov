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

    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    """Очередь FIFO на односвязном списке."""

    __slots__ = ("head", "tail")

    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, item):
        new_node = Node(item)
        if self.tail is not None:
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node

    def dequeue(self):
        if self.head is None:
            print("Очередь пуста")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data

    def peek(self):
        if self.head is None:
            print("Очередь пуста")
        return self.head.data


class UglyNumberGenerator:
    """Генератор ugly-чисел (делители ≤ 5)."""

    def min3(self, a, b, c):
        """Минимум из трёх чисел без builtin min()."""
        m = a
        if b < m:
            m = b
        if c < m:
            m = c
        return m

    def generate(self, n):
        """Вернуть список из первых n ugly-чисел (n > 0)."""
        if n <= 0:
            print("n должно быть положительным целым числом")

        result = []
        produced = 0

        q2, q3, q5 = LinkedQueue(), LinkedQueue(), LinkedQueue()
        q2.enqueue(2)
        q3.enqueue(3)
        q5.enqueue(5)

        while produced < n:
            a = q2.peek()
            b = q3.peek()
            c = q5.peek()
            x = self._min3(a, b, c)

            if q2.peek() == x:
                q2.dequeue()
            if q3.peek() == x:
                q3.dequeue()
            if q5.peek() == x:
                q5.dequeue()

            result.append(x)
            produced += 1

            q2.enqueue(x * 2)
            q3.enqueue(x * 3)
            q5.enqueue(x * 5)

        return result


def main():
    """Простейший CLI."""
    gen = UglyNumberGenerator()

    while True:
        try:
            raw = input("Введите n (0 — выход): ")
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
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            return

    try:
        nums = gen.generate(n)
    except KeyboardInterrupt:
        print("\nГенерация прервана.")
        return

    groups = {2: [], 3: [], 5: []}
    for num in nums:
        if num % 2 == 0:
            groups[2].append(num)
        if num % 3 == 0:
            groups[3].append(num)
        if num % 5 == 0:
            groups[5].append(num)

    print(f"Первые {n} чисел с простыми множителями только 2, 3, 5:")
    print(*nums)

    print("\nРазбиение по включённым простым множителям:")
    for p in (2, 3, 5):
        if groups[p]:
            print(f"\nЧисла, делящиеся на {p}:")
            print(*groups[p])


if __name__ == "__main__":
    main()
