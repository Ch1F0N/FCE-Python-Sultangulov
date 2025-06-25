"""
Напечатать в порядке возрастания первых n натуральных чисел, в разложение
которых на простые множители входят только числа 2,3,5.
"""

class Node:
    """
    Узел односвязного списка.

    Атрибуты
    --------
    data : int
        Полезная нагрузка узла.
    next : Node | None
        Ссылка на следующий узел списка (None — конец списка).
    """

    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    """
    Простейшая очередь FIFO, основанная на односвязном списке.

    Атрибуты
    --------
    head : Node | None
        Первый элемент в очереди (точка извлечения).
    tail : Node | None
        Последний элемент в очереди (точка вставки).

    Методы
    ------
    is_empty() -> bool
        Проверяет, пуста ли очередь.
    enqueue(item) -> None
        Добавляет элемент в конец очереди.
    dequeue() -> int
        Извлекает элемент из начала очереди, бросает IndexError, если очередь пуста.
    peek() -> int
        Возвращает первый элемент без извлечения, бросает IndexError, если очередь пуста.
    """

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
        value = self.head.data
        self.head = self.head.next
        if self.head is None:               
            self.tail = None
        return value

    def peek(self):
        if self.head is None:
            print("Очередь пуста")
        return self.head.data


class UglyNumberGenerator:
    """
    Генератор ugly-чисел

    Алгоритм
    --------
    Поддерживаются три очереди:
        queue2 — кандидаты, полученные умножением напечатанных чисел на 2;
        queue3 — … на 3;
        queue5 — … на 5.
    Минимум из первых элементов очередей является очередным ugly-числом.
    После вывода x все копии x убираются из голов очередей, а x·2, x·3, x·5
    помещаются в соответствующие очереди.
    """

    def _min_of_three(self, value2, value3, value5):
        """Возвратить минимальное из трёх чисел без builtin min()."""
        minimum = value2
        if value3 < minimum:
            minimum = value3
        if value5 < minimum:
            minimum = value5
        return minimum

    def generate(self, count):
        """
        Сформировать первые *count* ugly-чисел.

        Параметры
        ---------
        count : int
            Количество требуемых чисел (count > 0).

        Возврат
        -------
        list[int]
            Монотонно возрастающий список длиной count.
        """
        if count <= 0:
            print("count должно быть положительным целым числом")

        ugly_numbers = []
        generated_count = 0                 

        queue2, queue3, queue5 = LinkedQueue(), LinkedQueue(), LinkedQueue()
        queue2.enqueue(2)
        queue3.enqueue(3)
        queue5.enqueue(5)

        while generated_count < count:
            candidate_from_2 = queue2.peek()
            candidate_from_3 = queue3.peek()
            candidate_from_5 = queue5.peek()

            next_ugly = self._min_of_three(
                candidate_from_2, candidate_from_3, candidate_from_5
            )

            if queue2.peek() == next_ugly:
                queue2.dequeue()
            if queue3.peek() == next_ugly:
                queue3.dequeue()
            if queue5.peek() == next_ugly:
                queue5.dequeue()

            ugly_numbers.append(next_ugly)
            generated_count += 1

            queue2.enqueue(next_ugly * 2)
            queue3.enqueue(next_ugly * 3)
            queue5.enqueue(next_ugly * 5)

        return ugly_numbers


def main():
    generator = UglyNumberGenerator()

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
        ugly_nums = generator.generate(n)
    except KeyboardInterrupt:
        print("\nГенерация прервана.")
        return

    
    groups = {2: [], 3: [], 5: []}
    for num in ugly_nums:
        if num % 2 == 0:
            groups[2].append(num)
        if num % 3 == 0:
            groups[3].append(num)
        if num % 5 == 0:
            groups[5].append(num)

    print(f"Первые {n} чисел с простыми множителями только 2, 3, 5:")
    print(*ugly_nums)

    print("\nРазбиение по спискам:")
    for p in (2, 3, 5):
        if groups[p]:
            print(f"\nЧисла, делящиеся на {p}:")
            print(*groups[p])


if __name__ == "__main__":
    main()
