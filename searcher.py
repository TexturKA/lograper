import os
import datetime
from types import FunctionType


class Log:
    def __init__(self, full_log_name: str):
        self.name = full_log_name
        self.short_name = full_log_name.split("-")[-1][:-4] if full_log_name else None
        self.data = list()


class LogSearcher:
    def __init__(self, path_log_folder, logs_to_search, path_out=r"./res", debug_msg=print):
        """
        Поиск ключевых слов в логах.\n
        :param str path_log_folder: путь до папки с логами
        :param str or tuple or list logs_to_search: логи для поиска
        :param path_out: путь для сохранения данных поиска
        """
        self.path_log_folder = path_log_folder
        self.path_out = path_out
        self.logs_to_search = logs_to_search
        self.debug_msg = debug_msg
        self.logs = list()

        self.__normalize_logs_to_tuple()
        self.fill_logs()

    def run(self, substr_to_search, do_func=lambda line, substr: line.split(substr)[1].strip()):
        """
        Запускает процесс поиска подстроки в логах.\n
        :param str or tuple substr_to_search: подстрока, которая должна быть найдена;
        :param function do_func: функция для обработки строки поиска (по умолчанию
            возвращает то, что после строки поиска), принимает аргументы:
                @line: строка;
                @substr: подстрока для поиска в строке.
        """
        self.debug_msg(f"\tSearching substr in logs:")
        if not isinstance(substr_to_search, (str, tuple, list)):
            raise TypeError("substr_to_search expected types: str | tuple | list")
        if not isinstance(do_func, FunctionType):
            raise TypeError("do_func expected type: function")
        for log in self.logs:
            self.debug_msg(f"\tread \"{log.short_name}\"... ")
            with open(f"{self.path_log_folder}/{log.name}", "r", encoding="utf-8") as file:
                for line in file:
                    if isinstance(substr_to_search, str):
                        if substr_to_search in line:
                            result = do_func(line, substr_to_search)
                            self.debug_msg(f"\t\tfound \"{result}\" \"{substr_to_search}\" in \"{log.short_name}\"")
                            log.data.append(result)
                    else:
                        for substr in substr_to_search:
                            if substr in line:
                                result = do_func(line, substr)
                                self.debug_msg(f"\t\tfound \"{result}\" \"{substr}\" in \"{log.short_name}\"")
                                log.data.append(result)

    def save(self, path_out=None):
        """
        Сохраняет результат поиска по указанному пути.\n
        :param path_out: путь для сохранения данных поиска
        """
        if path_out is None:
            path_out = self.path_out
        if not self.logs:
            raise TypeError("Can't save logs. Logs is empty")
        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ".csv"
        self.debug_msg(f"Saving logs in {file_name}... ", end="")
        with open(f"{path_out}/{file_name}", "w", encoding="utf-8") as file:
            for log in self.logs:
                if log.data:
                    file.write(log.short_name + "\t" + "\t".join(log.data) + "\n")
        self.debug_msg("Done!")

    def fill_logs(self):
        """ Заполнение списка логов для поиска """
        if not os.path.exists(self.path_out):
            os.mkdir(self.path_out)

        self.debug_msg("Reading logs to search... ", end="")
        search_logs = list()
        for line in self.logs_to_search:
            search_logs.append(line.strip())
        self.debug_msg(f"{len(search_logs)} logs read")

        self.debug_msg("Reading logs for search... ", end="")
        log_list = os.listdir(self.path_log_folder)
        self.debug_msg(f"{len(log_list)} logs read")

        self.debug_msg("Searching logs to search in logs for search:")
        for file_name in log_list:
            log = Log(file_name)
            if log.short_name in search_logs:
                self.debug_msg(f"\tfound \"{log.short_name}\"")
                self.logs.append(log)
        self.debug_msg(f"{len(self.logs)}/{len(log_list)} logs read")

    def __normalize_logs_to_tuple(self):
        if isinstance(self.logs_to_search, str):
            self.logs_to_search = (self.logs_to_search,)
        elif isinstance(self.logs_to_search, (tuple, list)):
            tuple(self.logs_to_search)
        else:
            raise TypeError("logs_to_search expected str | tuple | list")


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
