import tkinter as tk

class Document:
    def __init__(self, number, date, content):
        self.number = number
        self.date = date
        self.content = content

class Letter(Document):
    def __init__(self, number, date, content, letter_type, correspondent):
        super().__init__(number, date, content)
        self.letter_type = letter_type
        self.correspondent = correspondent

class Order(Document):
    def __init__(self, number, date, content, department, deadline, executor):
        super().__init__(number, date, content)
        self.department = department
        self.deadline = deadline
        self.executor = executor

class BusinessTrip(Document):
    def __init__(self, number, date, content, employee, period, destination):
        super().__init__(number, date, content)
        self.employee = employee
        self.period = period
        self.destination = destination

class DocumentFactory:
    @staticmethod
    def create_document(doc_type, number, date, content, **kwargs):
        if doc_type == "letter":
            return Letter(number, date, content, **kwargs)
        elif doc_type == "order":
            return Order(number, date, content, **kwargs)
        elif doc_type == "business_trip":
            return BusinessTrip(number, date, content, **kwargs)
        else:
            raise ValueError("Invalid document type")

# Создание документов
documents = [
    DocumentFactory.create_document("letter", "001", "2024-02-28", "Содержание письма 1",
                                    letter_type="входящее", correspondent="Корреспондент 1"),
    DocumentFactory.create_document("order", "002", "2024-02-29", "Содержание приказа 1",
                                    department="Подразделение 1", deadline="2024-03-10", executor="Исполнитель 1"),
    DocumentFactory.create_document("business_trip", "003", "2024-03-01", "Содержание распоряжения о командировке 1",
                                    employee="Сотрудник 1", period="2024-03-15 - 2024-03-20", destination="Место 1")
]

# Вывод полного перечня документов
for document in documents:
    print(f"Номер: {document.number}")
    print(f"Дата: {document.date}")
    print(f"Содержание: {document.content}")
    print()

# Вывод содержания выбранного документа по номеру
def show_document_content():
    number = entry.get()
    for document in documents:
        if document.number == number:
            print(f"Содержание документа {number}: {document.content}")
            break
    else:
        print(f"Документ с номером {number} не найден")

# Создание графического интерфейса с полем для ввода номера документа и кнопкой для вывода содержания
root = tk.Tk()
label = tk.Label(root, text="Номер документа:")
label.pack()
entry = tk.Entry(root)
entry.pack()
button = tk.Button(root, text="Показать содержание", command=show_document_content)
button.pack()
root.mainloop()
