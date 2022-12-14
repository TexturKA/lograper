### Для чего этот проект:
Скрипт для поиска информации в выбранных логах из общего пула.

### Технологии:
- Python 3.10

### Как запустить проект:
Консольный проект, все данные задаются в `if __name__ == '__main__'`:
При инициализации LogSearcher передать параметры
- путь до папки с логами
- логи для поиска
- _(optional)_ путь для сохранения данных поиска

После, для запуска процесса поиска подстроки нужно вызвать метод `run`, который
принимает аргументы:
- подстрока, которая должна быть найдена
- _(optional)_ callback функция для обработки строки поиска (по умолчанию возвращает то, что
после строки поиска), функция принимает аргументы:
  - @line: строка;
  - @substr: подстрока для поиска в строке.

### Пример кода:    

```python
if __name__ == '__main__':
    # Пример имени лога, попадающий под критерий поиска: "0000001-log_example_name1.log"
    search = LogSearcher(
        r"D:\work\log_example_path",
        ["log_example_name1",
         "log_example_name2",
         "log_example_name3",
         "log_example_name4"
         ],
    )
    search.run("transfer to: ")
    search.save()
```
