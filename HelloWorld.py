def main():
    applicant = None

    # Создание объекта абитуриента с помощью фабрики
    applicant_factory = ApplicantFactory()

    format_type = input("Введите тип формата (text/xml/database): ")

    if format_type == "text":
        applicant = applicant_factory.create_applicant("text", "Иванов", "Иван", "Иванович", "2000-01-01", [90, 85, 95], ["Специальность 1", "Специальность 2", "Специальность 3"])
    elif format_type == "xml":
        applicant = applicant_factory.create_applicant("xml", "Иванов", "Иван", "Иванович", "2000-01-01", [90, 85, 95], ["Специальность 1", "Специальность 2", "Специальность 3"])
    elif format_type == "database":
        applicant = applicant_factory.create_applicant("database", "Иванов", "Иван", "Иванович", "2000-01-01", [90, 85, 95], ["Специальность 1", "Специальность 2", "Специальность 3"])

    if applicant:
        print("Информация об абитуриенте:")
        print(f"Фамилия: {applicant.last_name}")
        print(f"Имя: {applicant.first_name}")
        print(f"Отчество: {applicant.middle_name}")
        print(f"Дата рождения: {applicant.date_of_birth}")
        print(f"Оценки: {applicant.grades}")
        print(f"Специальности: {applicant.specialties}")
    else:
        print("Некорректный тип формата.")


if __name__ == "__main__":
    main()
