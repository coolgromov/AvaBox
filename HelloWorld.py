import tkinter as tk
import xml.etree.ElementTree as ET

class Applicant:
    def __init__(self, last_name, first_name, middle_name, date_of_birth, ege_scores, desired_specialties):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.date_of_birth = date_of_birth
        self.ege_scores = ege_scores
        self.desired_specialties = desired_specialties

    def to_txt(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"Фамилия: {self.last_name}\n")
            file.write(f"Имя: {self.first_name}\n")
            file.write(f"Отчество: {self.middle_name}\n")
            file.write(f"Дата рождения: {self.date_of_birth}\n")
            file.write("Баллы за ЕГЭ:\n")
            for subject, score in self.ege_scores.items():
                file.write(f"{subject}: {score}\n")
            file.write("Желательные специальности:\n")
            for specialty in self.desired_specialties:
                file.write(f"{specialty}\n")

    def to_xml(self, file_path):
        root = ET.Element("applicant")
        last_name_elem = ET.SubElement(root, "last_name")
        last_name_elem.text = self.last_name
        first_name_elem = ET.SubElement(root, "first_name")
        first_name_elem.text = self.first_name
        middle_name_elem = ET.SubElement(root, "middle_name")
        middle_name_elem.text = self.middle_name
        date_of_birth_elem = ET.SubElement(root, "date_of_birth")
        date_of_birth_elem.text = self.date_of_birth
        ege_scores_elem = ET.SubElement(root, "ege_scores")
        for subject, score in self.ege_scores.items():
            subject_elem = ET.SubElement(ege_scores_elem, "subject")
            subject_elem.text = subject
            score_elem = ET.SubElement(ege_scores_elem, "score")
            score_elem.text = str(score)
        desired_specialties_elem = ET.SubElement(root, "desired_specialties")
        for specialty in self.desired_specialties:
            specialty_elem = ET.SubElement(desired_specialties_elem, "specialty")
            specialty_elem.text = specialty

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

def save_applicant():
    last_name = last_name_entry.get()
    first_name = first_name_entry.get()
    middle_name = middle_name_entry.get()
    date_of_birth = date_of_birth_entry.get()
    ege_scores = {
        "Математика": int(math_score_entry.get()),
        "Физика": int(physics_score_entry.get()),
        "Русский язык": int(russian_score_entry.get())
    }
    desired_specialties = [specialty_entry1.get(), specialty_entry2.get(), specialty_entry3.get()]

    applicant = Applicant(last_name, first_name, middle_name, date_of_birth, ege_scores, desired_specialties)
    applicant.to_txt("applicant.txt")
    applicant.to_xml("applicant.xml")

    # Очистка полей после сохранения
    last_name_entry.delete(0, tk.END)
    first_name_entry.delete(0, tk.END)
    middle_name_entry.delete(0, tk.END)
    date_of_birth_entry.delete(0, tk.END)
    math_score_entry.delete(0, tk.END)
    physics_score_entry.delete(0, tk.END)
    russian_score_entry.delete(0, tk.END)
    specialty_entry1.delete(0, tk.END)
    specialty_entry2.delete(0, tk.END)
    specialty_entry3.delete(0, tk.END)

# Создание графического интерфейса с помощью Tkinter
root = tk.Tk()
root.title("Ввод информации об абитуриенте")

# Форма ввода данных
last_name_label = tk.Label(root, text="Фамилия:")
last_name_entry = tk.Entry(root)
first_name_label = tk.Label(root, text="Имя:")
first_name_entry = tk.Entry(root)
middle_name_label = tk.Label(root, text="Отчество:")
middle_name_entry = tk.Entry(root)
date_of_birth_label = tk.Label(root, text="Дата рождения:")
date_of_birth_entry = tk.Entry(root)
math_score_label = tk.Label(root, text="БаллПродолжение кода:

```python
math_score_entry = tk.Entry(root)
physics_score_label = tk.Label(root, text="Балл по физике:")
physics_score_entry = tk.Entry(root)
russian_score_label = tk.Label(root, text="Балл по русскому языку:")
russian_score_entry = tk.Entry(root)
specialty_label1 = tk.Label(root, text="Желаемая специальность 1:")
specialty_entry1 = tk.Entry(root)
specialty_label2 = tk.Label(root, text="Желаемая специальность 2:")
specialty_entry2 = tk.Entry(root)
specialty_label3 = tk.Label(root, text="Желаемая специальность 3:")
specialty_entry3 = tk.Entry(root)
save_button = tk.Button(root, text="Сохранить", command=save_applicant)

last_name_label.grid(row=0, column=0)
last_name_entry.grid(row=0, column=1)
first_name_label.grid(row=1, column=0)
first_name_entry.grid(row=1, column=1)
middle_name_label.grid(row=2, column=0)
middle_name_entry.grid(row=2, column=1)
date_of_birth_label.grid(row=3, column=0)
date_of_birth_entry.grid(row=3, column=1)
math_score_label.grid(row=4, column=0)
math_score_entry.grid(row=4, column=1)
physics_score_label.grid(row=5, column=0)
physics_score_entry.grid(row=5, column=1)
russian_score_label.grid(row=6, column=0)
russian_score_entry.grid(row=6, column=1)
specialty_label1.grid(row=7, column=0)
specialty_entry1.grid(row=7, column=1)
specialty_label2.grid(row=8, column=0)
specialty_entry2.grid(row=8, column=1)
specialty_label3.grid(row=9, column=0)
specialty_entry3.grid(row=9, column=1)
save_button.grid(row=10, columnspan=2)

root.mainloop()
