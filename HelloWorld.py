Конечно, я могу помочь вам с вашей лабораторной работой на языке C++. Давайте начнем с первой части.

Часть 1:

1. Задание: Напечатать заданное существительное во всех падежах.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string noun;
    std::cout << "Введите существительное: ";
    std::cin >> noun;

    std::cout << "Именительный падеж (кто? что?): " << noun << std::endl;
    std::cout << "Родительный падеж (кого? чего?): " << noun << "а" << std::endl;
    std::cout << "Дательный падеж (кому? чему?): " << noun << "у" << std::endl;
    std::cout << "Винительный падеж (кого? что?): " << noun << std::endl;
    std::cout << "Творительный падеж (кем? чем?): " << noun << "ом" << std::endl;
    std::cout << "Предложный падеж (о ком? о чём?): " << noun << "е" << std::endl;

    return 0;
}
```

В этом коде мы сначала запрашиваем у пользователя существительное, а затем выводим его во всех падежах.

2. Задание: Вычислить длину самого короткого слова в предложении из трех слов, разделенных пробелами.

```cpp
#include <iostream>
#include <string>

int main() {
    std::string sentence;
    std::cout << "Введите предложение из трех слов, разделенных пробелами: ";
    std::getline(std::cin, sentence);

    std::string word1, word2, word3;
    std::istringstream iss(sentence);
    iss >> word1 >> word2 >> word3;

    int shortestLength = std::min({word1.length(), word2.length(), word3.length()});

    std::cout << "Длина самого короткого слова: " << shortestLength << std::endl;

    return 0;
}
```

В этом коде мы сначала запрашиваем у пользователя предложение, а затем используем `std::istringstream` для разделения предложения на отдельные слова. Затем мы вычисляем длину каждого слова и находим самую короткую длину с помощью функции `std::min`. Результат выводится на экран.

Теперь перейдем ко второй части.

Часть 2:

1. Задание: Сравнить три введенные строки и вывести их по убыванию длины строки, начиная каждый вывод с новой строки. Результаты работы программы записываются в файл.

```cpp
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

int main() {
    std::string str1, str2, str3;
    std::cout << "Введите три строки: ";
    std::cin >> str1 >> str2 >> str3;

    std::ofstream outputFile("output.txt");
    if (outputFile.is_open()) {
        std::string strings[] = {str1, str2, str3};
        std::sort(strings, strings + 3, [](const std::string& a, const std::string& b) {
            return a.length() > b.length();
        });

        for (const std::string& str : strings) {
            outputFile << str << std::endl;
        }

        outputFile.close();
        std::cout << "Результаты записаны в файл output.txt." << std::endl;
    } else {
        std::cout << "Ошибка при открытии файла." << std::endl;
    }

    return 0;
}
```

В этом коде мы сначала запрашиваем у пользователя три строки, а затем сортируем их по убыванию длины с помощью функции `std::sort` и лямбда-функции в качестве компаратора. Затем мы открываем файл `output.txt` для записи и поочередно записываем каждуюстроку в отсортированном порядке, разделяя их переводом строки. Наконец, мы закрываем файл и выводим сообщение об успешной записи.

2. Задание: Изменить предыдущую программу так, чтобы строки не вводились вручную, а брались из входного файла.

```cpp
#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>

int main() {
    std::ifstream inputFile("input.txt");
    std::ofstream outputFile("output.txt");
    if (inputFile.is_open() && outputFile.is_open()) {
        std::string str1, str2, str3;
        inputFile >> str1 >> str2 >> str3;

        std::string strings[] = {str1, str2, str3};
        std::sort(strings, strings + 3, [](const std::string& a, const std::string& b) {
            return a.length() > b.length();
        });

        for (const std::string& str : strings) {
            outputFile << str << std::endl;
        }

        inputFile.close();
        outputFile.close();
        std::cout << "Результаты записаны в файл output.txt." << std::endl;
    } else {
        std::cout << "Ошибка при открытии файлов." << std::endl;
    }

    return 0;
}
```

В этой версии кода мы открываем файл `input.txt` для чтения и файл `output.txt` для записи. Затем мы считываем строки из входного файла в переменные `str1`, `str2` и `str3`. После этого процесс аналогичен предыдущей программе: сортируем строки по убыванию длины и записываем результаты в файл `output.txt`. Наконец, мы закрываем оба файла и выводим сообщение об успешной записи.

Убедитесь, что у вас есть файлы `input.txt` и `output.txt` в той же папке, где находится исполняемый файл программы, и что входной файл содержит три строки, разделенные пробелами.

Надеюсь, это поможет вам выполнить вашу лабораторную работу! Если у вас возникнут еще вопросы, не стесняйтесь задавать.
