import tkinter as tk
import xml.etree.ElementTree as ET
import sqlite3

class Applicant:
    def __init__(self, last_name, first_name, middle_name, birth_date, ege_scores, specialties):
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.birth_date = birth_date
        self.ege_scores = ege_scores
        self.specialties = specialties

    def save(self):
        pass

class TextApplicant(Applicant):
    def save(self):
        with open('applicant.txt', 'w') as file:
            file.write(f"Фамилия: {self.last_name}\n")
            file.write(f"Имя: {self.first_name}\n")
            file.write(f"Отчество: {self.middle_name}\n")
            file.write(f"Дата рождения: {self.birth_date}\n")
            file.write("Баллы за ЕГЭ:\n")
            for subject, score in self.ege_scores.items():
                file.write(f"{subject}: {score}\n")
            file.write("Желательные специальности:\n")
            for specialty in self.specialties:
                file.write(f"- {specialty}\n")

class XmlApplicant(Applicant):
    def save(self):
        root = ET.Element("Applicant")
        ET.SubElement(root, "LastName").text = self.last_name
        ET.SubElement(root, "FirstName").text = self.first_name
        ET.SubElement(root, "MiddleName").text = self.middle_name
        ET.SubElement(root, "BirthDate").text = self.birth_date
        ege_scores_elem = ET.SubElement(root, "EGEScores")
        for subject, score in self.ege_scores.items():
            ET.SubElement(ege_scores_elem, subject).text = str(score)
        specialties_elem = ET.SubElement(root, "Specialties")
        for specialty in self.specialties:
            ET.SubElement(specialties_elem, "Specialty").text = specialty

        tree = ET.ElementTree(root)
        tree.write("applicant.xml")

class DatabaseApplicant(Applicant):
    def save(self):
        connection = sqlite3.connect('applicants.db')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS applicants ('
                       'last_name TEXT, '
                       'first_name TEXT, '
                       'middle_name TEXT, '
                       'birth_date TEXT, '
                       'ege_scores TEXT, '
                       'specialties TEXT)')

        ege_scores_str = ', '.join([f"{subject}: {score}" for subject, score in self.ege_scores.items()])
        specialties_str = ', '.join(self.specialties)
        cursor.execute('INSERT INTO applicants VALUES (?, ?, ?, ?, ?, ?)',
                       (self.last_name, self.first_name, self.middle_name,
                        self.birth_date, ege_scores_str, specialties_str))

        connection.commit()
        connection.close()

def save_applicant(format):
    last_name = entry_last_name.get()
    first_name = entry_first_name.get()
    middle_name = entry_middle_name.get()
    birth_date = entry_birth_date.get()
    ege_scores = {
        "Subject1": entry_subject1.get(),
        "Subject2": entry_subject2.get(),
        "Subject3": entry_subject3.get()
    }
    specialties = [
        entry_specialty1.get(),
        entry_specialty2.get(),
        entry_specialty3.get()
    ]

    if format == "Text":
        applicant = TextApplicant(last_name, first_name, middle_name, birth_date, ege_scores, specialties)
    elif format == "Xml":
        applicant = XmlApplicant(last_name, first_name, middle_name, birth_date, ege_scores, specialties)
    elif format == "Database":
        applicant = DatabaseApplicant(last_name, first_name, middle_name, birth_date, ege_scores, specialties)

    applicant.save()

# Создание графического интерфейса с использованием Tkinter
window = tk.Tk()
window.title("Сохранение информации об абитуриенте")

# Создание и размещение элементов интерфейса
label_last_name = tk.Label(window, text="Фамилия:")
label_last_name.grid(row=0, column=0, sticky=tk.E)
entry_last_name = tk.Entry(window)
entry_last_name.grid(row=0, column=1)

# Аналогично создайте и разместите остальные элементы интерфейса для остальных полей (имя, отчество, дата рождения, баллы ЕГЭ, специальности)

# Создание кнопок соответствующих форматам сохранения
button_text = tk.Button(window, text="Сохранить в текстовом формате", command=lambda: save_applicant("Text"))
button_text.grid(row=7, column=0, columnspan=2)

button_xml = tk.Button(window, text="Сохранить в формате XML", command=lambda: save_applicant("Xml"))
button_xml.grid(row=8, column=0, columnspan=2)

button_db = tk.Button(window, text="Сохранить в базе данных", command=lambda: save_applicant("Database"))
button_db.grid(row=9, column=0, columnspan=2)

window.mainloop()
