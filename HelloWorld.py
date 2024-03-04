class Component:
    def __init__(self, number, name, price):
        self.number = number
        self.name = name
        self.price = price

class Motherboard(Component):
    def __init__(self, number, name, price, socket_type, processor_count, memory_type, bus_speed):
        super().__init__(number, name, price)
        self.socket_type = socket_type
        self.processor_count = processor_count
        self.memory_type = memory_type
        self.bus_speed = bus_speed

class Processor(Component):
    def __init__(self, number, name, price, socket_type, core_count, clock_speed, technology):
        super().__init__(number, name, price)
        self.socket_type = socket_type
        self.core_count = core_count
        self.clock_speed = clock_speed
        self.technology = technology

class HardDrive(Component):
    def __init__(self, number, name, price, capacity, rotation_speed, interface_type):
        super().__init__(number, name, price)
        self.capacity = capacity
        self.rotation_speed = rotation_speed
        self.interface_type = interface_type

class ComponentFactory:
    @staticmethod
    def create_component(component_type, number, name, price, **kwargs):
        if component_type == "motherboard":
            return Motherboard(number, name, price, **kwargs)
        elif component_type == "processor":
            return Processor(number, name, price, **kwargs)
        elif component_type == "hard_drive":
            return HardDrive(number, name, price, **kwargs)
        else:
            raise ValueError("Invalid component type")

# Создание комплектующих
components = [
    ComponentFactory.create_component("motherboard", "001", "Материнская плата 1", 100.0,
                                      socket_type="Socket 1", processor_count=1,
                                      memory_type="DDR4", bus_speed="2400 MHz"),
    ComponentFactory.create_component("processor", "002", "Процессор 1", 200.0,
                                      socket_type="Socket 1", core_count=4,
                                      clock_speed="3.0 GHz", technology="14 nm"),
    ComponentFactory.create_component("hard_drive", "003", "Жесткий диск 1", 50.0,
                                      capacity="1 TB", rotation_speed="7200 RPM",
                                      interface_type="SATA")
]

# Вывод полной номенклатуры комплектующих
for component in components:
    print(f"Номер: {component.number}")
    print(f"Наименование: {component.name}")
    print(f"Цена: {component.price}")
    if isinstance(component, Motherboard):
        print(f"Тип сокета: {component.socket_type}")
        print(f"Количество процессоров: {component.processor_count}")
        print(f"Тип оперативной памяти: {component.memory_type}")
        print(f"Частота системной шины: {component.bus_speed}")
    elif isinstance(component, Processor):
        print(f"Тип сокета: {component.socket_type}")
        print(f"Количество ядер: {component.core_count}")
        print(f"Тактовая частота: {component.clock_speed}")
        print(f"Техпроцесс: {component.technology}")
    elif isinstance(component, HardDrive):
        print(f"Объем: {component.capacity}")
        print(f"Скорость вращения: {component.rotation_speed}")
        print(f"Тип интерфейса: {component.interface_type}")
    print()

# Вывод детальной информации по товару по номенклатурному номеру
def show_component_details():
    number = entry.get()
    for component in components:
        if component.number == number:
            print(f"Детальная информация по товару {number}:")
            print(f"Наименование: {component.name}")
            print(f"Цена: {component.price}")
            if isinstance(component, Motherboard):
                print(f"Тип сокета: {component.socket_type}")
                print(f"Количество процессоров: {component.processor_count}")
                print(f"Тип оперативной памяти: {component.memory_type}")
                print(f"Частота системной шины: {component.bus_speed}")
            elif isinstance(component, Processor):
                print(f"Тип сокета: {component.socket_type}")
                print(f"Количество ядер: {component.core_count}")
                print(f"Тактовая частота: {component.clock_speed}")
                print(f"Техпроцесс: {component.technology}")
            elif isinstance(component, HardDrive):
                print(f"Объем: {component.capacity}")
                print(f"Скорость вращения: {component.rotation_speed}")
                print(f"Тип интерфейса: {component.interface_type}")
            break
    else:
        print(f"Товар с номером {number} не найден")

# Создание графического интерфейса с полем для ввода номенклатурного номера и кнопкой для вывода детальной информации
root = tk.Tk()
label = tk.Label(root, text="Номенклатурный номер:")
label.pack()
entry = tk.Entry(root)
entry.pack()
button = tk.Button(root, text="Показать детальную информацию", command=show_component_details)
button.pack()
root.mainloop()
