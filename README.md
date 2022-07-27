# Асинхронный парсер HeadHunter через публичный API

### Описание
Мои первые начинания в asyncio и aiohttp на примере создания парсера https://hh.ru с использованием публичного API.
Скрипт пробегается по языкам программирования, заданных в списке `PROGRAMMING_LANGUAGES` и считает среднюю 
зарплату программистов по каждому. Результат возвращается в виде словаря словарей.

### Запуск
Использовал Python 3.8. Для запуска установите зависимости из файла
```console
$ pip install -r requirements.txt
```
и запустите скрипт
```console
$ python async_parse_hh.py
```
### Пример вывода
```console
{'C++': {'average_salary': 169918,
         'vacancies_found': 1033,
         'vacancies_processed': 341},
 'Go': {'average_salary': 205834,
        'vacancies_found': 529,
        'vacancies_processed': 152},
 'Java': {'average_salary': 185330,
          'vacancies_found': 1798,
          'vacancies_processed': 356},
 'JavaScript': {'average_salary': 166110,
                'vacancies_found': 2572,
                'vacancies_processed': 797},
 'Python': {'average_salary': 172585,
            'vacancies_found': 1717,
            'vacancies_processed': 475},
 'Ruby': {'average_salary': 193092,
          'vacancies_found': 126,
          'vacancies_processed': 43},
 'Rust': {'average_salary': 131457,
          'vacancies_found': 46,
          'vacancies_processed': 24}}
```