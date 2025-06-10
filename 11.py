class StackNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, value):
        new_node = StackNode(value)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Попытка выгрузки из пустого отсека")
        value = self.top.value
        self.top = self.top.next
        self.size -= 1
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("Отсек пуст")
        return self.top.value

    def is_empty(self):
        return self.top is None

    def get_size(self):
        return self.size

class BargeSimulator:
    def __init__(self, num_compartments, max_barrels):
        self.compartments = [Stack() for _ in range(num_compartments)]
        self.total_barrels = 0
        self.max_barrels = 0
        self.capacity = max_barrels

    def process_operation(self, action, compartment, fuel_type):
        try:
            compartment_idx = compartment - 1  # Переводим в 0-based индекс
            if action == '+':
                if self.total_barrels >= self.capacity:
                    return False
                self.compartments[compartment_idx].push(fuel_type)
                self.total_barrels += 1
                if self.total_barrels > self.max_barrels:
                    self.max_barrels = self.total_barrels
                return True

            elif action == '-':
                if (self.compartments[compartment_idx].is_empty() or
                        self.compartments[compartment_idx].peek() != fuel_type):
                    return False
                self.compartments[compartment_idx].pop()
                self.total_barrels -= 1
                return True

            return False
        except:
            return False

    def is_empty(self):
        return self.total_barrels == 0

def read_input(filename):
    try:
        with open(filename, 'r') as file:
            # Чтение первой строки
            first_line = file.readline().strip()
            while not first_line:
                first_line = file.readline().strip()

            # Парсинг N, K, P
            try:
                parts = first_line.split()
                if len(parts) != 3:
                    raise ValueError("Первая строка должна содержать 3 числа")

                N = int(parts[0])
                K = int(parts[1])
                P = int(parts[2])

                if not (1 <= N <= 100000 and 1 <= K <= 100000 and 1 <= P <= 100000):
                    raise ValueError("N, K и P должны быть от 1 до 100000")
            except ValueError as e:
                raise ValueError(f"Неверный формат первой строки: {str(e)}")

            operations = []
            for _ in range(N):
                line = file.readline().strip()
                while not line:
                    line = file.readline().strip()

                parts = line.split()
                if len(parts) != 3:
                    raise ValueError(f"Неверный формат операции: {line}")

                action = parts[0]
                try:
                    compartment = int(parts[1])
                    fuel_type = int(parts[2])
                except ValueError:
                    raise ValueError(f"Нечисловые значения в операции: {line}")

                if action not in ('+', '-'):
                    raise ValueError(f"Неизвестная операция: {action}")

                if not (1 <= compartment <= K):
                    raise ValueError(f"Неверный номер отсека: {compartment}")

                operations.append((action, compartment, fuel_type))

            return N, K, P, operations

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except Exception as e:
        raise ValueError(f"Ошибка чтения файла: {str(e)}")

def main():
    try:
        try:
            N, K, P, operations = read_input('input.txt')
        except Exception as e:
            print("Error")
            return

        simulator = BargeSimulator(K, P)

        for action, compartment, fuel_type in operations:
            if not simulator.process_operation(action, compartment, fuel_type):
                print("Error")
                return

        print(simulator.max_barrels if simulator.is_empty() else "Error")

    except Exception:
        print("Error")

if __name__ == "__main__":
    main()