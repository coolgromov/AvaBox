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

# Пример использования

# Создание экземпляра абитуриента
applicant = Applicant(
    last_name="Иванов",
    first_name="Иван",
    middle_name="Иванович",
    date_of_birth="01.01.2000",
    ege_scores={"Математика": 80, "Физика": 90, "Русский язык": 70},
    desired_specialties=["Информатика", "Физика", "Математика"]
)

# Сохранение информации об абитуриенте в формате txt
applicant.to_txt("applicant.txt")

# Сохранение информации об абитуриенте в формате xml
applicant.to_xml("applicant.xml")
