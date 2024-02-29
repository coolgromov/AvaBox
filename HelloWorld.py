Конечно! Вот полные примеры программ для каждой задачи:

1.1. Пример запуска программы для системы электронного документооборота:

```python
class Document:
    def __init__(self, number, date, content):
        self.number = number
        self.date = date
        self.content = content


class Letter(Document):
    def __init__(self, number, date, content, sender, recipient):
        super().__init__(number, date, content)
        self.sender = sender
        self.recipient = recipient


class Order(Document):
    def __init__(self, number, date, content, department, due_date, approver):
        super().__init__(number, date, content)
        self.department = department
        self.due_date = due_date
        self.approver = approver


class BusinessTripOrder(Document):
    def __init__(self, number, date, content, employee, trip_start_date, trip_end_date, destination):
        super().__init__(number, date, content)
        self.employee = employee
        self.trip_start_date = trip_start_date
        self.trip_end_date = trip_end_date
        self.destination = destination


class DocumentFactory:
    def create_document(self, document_type, *args, **kwargs):
        if document_type == "letter":
            return Letter(*args, **kwargs)
        elif document_type == "order":
            return Order(*args, **kwargs)
        elif document_type == "business_trip_order":
            return BusinessTripOrder(*args, **kwargs)
        else:
            raise ValueError("Invalid document type.")


def main():
    documents = []

    # Создание объектов документов с помощью фабрики
    document_factory = DocumentFactory()

    document1 = document_factory.create_document("letter", "001", "2024-02-28", "Содержание 1", "Отправитель 1", "Получатель 1")
    documents.append(document1)

    document2 = document_factory.create_document("order", "002", "2024-02-29", "Содержание 2", "Отдел IT", "2024-03-10", "Утверждающий 2")
    documents.append(document2)

    document3 = document_factory.create_document("business_trip_order", "003", "2024-03-01", "Содержание 3", "Сотрудник 3", "2024-03-15", "Лондон")
    documents.append(document3)

    # Вывод полного перечня документов
    for document in documents:
        print(f"Тип документа: {type(document).__name__}, Номер: {document.number}, Дата: {document.date}")

    # Вывод содержания выбранного документа
    document_number = input("Введите номер документа: ")
    for document in documents:
        if document.number == document_number:
            print(f"Содержание: {document.content}")
            break
    else:
        print("Документ не найден.")


if __name__ == "__main__":
    main()
```


1.2. Пример запуска программы для интернет-магазина:

```python
class Product:
    def __init__(self, item_number, name, price):
        self.item_number = item_number
        self.name = name
        self.price = price


class Motherboard(Product):
    def __init__(self, item_number, name, price, socket, ram_slots, ram_type, max_ram_speed):
        super().__init__(item_number, name, price)
        self.socket = socket
        self.ram_slots = ram_slots
        self.ram_type = ram_type
        self.max_ram_speed = max_ram_speed


class Processor(Product):
    def __init__(self, item_number, name, price, socket, cores, clock_speed, manufacturing_process):
        super().__init__(item_number, name, price)
        self.socket = socket
        self.cores = cores
        self.clock_speed = clock_speed
        self.manufacturing_process = manufacturing_process


class HardDrive(Product):
    def __init__(self, item_number, name, price, capacity, rotation_speed, interface):
        super().__init__(item_number, name, price)
        self.capacity = capacity
        self.rotation_speed = rotation_speed
        self.interface = interface


class ProductFactory:
    def create_product(self, product_type, *args, **kwargs):
        if product_type == "motherboard":
            return Motherboard(*args, **kwargs)
        elif product_type == "processor":
            return Processor(*args, **kwargs)
        elif product_type == "hard_drive":
            return HardDrive(*args, **kwargs)
Продолжение 1.2. Пример запуска программы для интернет-магазина:

```python
def main():
    products = []

    # Создание объектов продуктов с помощью фабрики
    product_factory = ProductFactory()

    product1 = product_factory.create_product("motherboard", "001", "Материнская плата 1", 150, "Socket AM4", 4, "DDR4", "3200 МГц")
    products.append(product1)

    product2 = product_factory.create_product("processor", "002", "Процессор 1", 200, "Socket AM4", 6, "3.4 ГГц", "7 нм")
    products.append(product2)

    product3 = product_factory.create_product("hard_drive", "003", "Жесткий диск 1", 80, "1 ТБ", "7200 об/мин", "SATA")
    products.append(product3)

    # Вывод полного перечня продуктов
    for product in products:
        print(f"Тип продукта: {type(product).__name__}, Номер: {product.item_number}, Название: {product.name}, Цена: {product.price}")

    # Вывод информации о выбранном продукте
    product_number = input("Введите номер продукта: ")
    for product in products:
        if product.item_number == product_number:
            print(f"Тип: {type(product).__name__}")
            print(f"Название: {product.name}")
            print(f"Цена: {product.price}")
            if isinstance(product, Motherboard):
                print(f"Сокет: {product.socket}")
                print(f"Слоты под ОЗУ: {product.ram_slots}")
                print(f"Тип ОЗУ: {product.ram_type}")
                print(f"Максимальная скорость ОЗУ: {product.max_ram_speed}")
            elif isinstance(product, Processor):
                print(f"Сокет: {product.socket}")
                print(f"Количество ядер: {product.cores}")
                print(f"Тактовая частота: {product.clock_speed}")
                print(f"Техпроцесс: {product.manufacturing_process}")
            elif isinstance(product, HardDrive):
                print(f"Емкость: {product.capacity}")
                print(f"Скорость вращения: {product.rotation_speed}")
                print(f"Интерфейс: {product.interface}")
            break
    else:
        print("Продукт не найден.")


if __name__ == "__main__":
    main()
```

1.3. Пример запуска программы для информационной системы об абитуриентах:

```python
class Applicant:
    def __init__(self, last_name, first_name, middle_name, date_of_birth, grades, specialties):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.date_of_birth = date_of_birth
        self.grades = grades
        self.specialties = specialties


class TextApplicant(Applicant):
    def __init__(self, last_name, first_name, middle_name, date_of_birth, grades, specialties):
        super().__init__(last_name, first_name, middle_name, date_of_birth, grades, specialties)


class XmlApplicant(Applicant):
    def __init__(self, last_name, first_name, middle_name, date_of_birth, grades, specialties):
        super().__init__(last_name, first_name, middle_name, date_of_birth, grades, specialties)


class DatabaseApplicant(Applicant):
    def __init__(self, last_name, first_name, middle_name, date_of_birth, grades, specialties):
        super().__init__(last_name, first_name, middle_name, date_of_birth, grades, specialties)


class ApplicantFactory:
    def create_applicant(self, format_type, last_name, first_name, middle_name, date_of_birth, grades, specialties):
        if format_type == "text":
            return TextApplicant(last_name, first_name, middle_name, date_of_birth, grades, specialties)
        elif format_type == "xml":
            return XmlApplicant(last_name, first_name, middle_name, date_of_birth, grades, specialties)
        elif format_type == "database":
            return DatabaseApplicant(last_name, first_name, middle_name, date_of_birth, grades, specialties)
        else:
            return None


def main():
    applicant = None

    # Создание объекта абитуриента с помощью фабрики
    applicant_factory = ApplicantFactory()
