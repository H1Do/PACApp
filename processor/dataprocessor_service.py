from pandas import DataFrame

from .dataprocessor_factory import DataProcessorFactory
from repository.connectorfactory import SQLStoreConnectorFactory       # подключаем фабрику коннекторов БД
from repository.sql_api import *                                       # подключаем API для работы с БД

"""
    В данном модуле реализуется класс с основной бизнес-логикой приложения. 
    Обычно такие модули / классы имеют в названии слово "Service".
"""


class DataProcessorService:

    def __init__(self, datasource: str, db_connection_url: str):
        self.datasource = datasource
        self.db_connection_url = db_connection_url
        # Инициализируем в конструкторе фабрику DataProcessor
        self.processor_fabric = DataProcessorFactory()

    """
        ВАЖНО! Обратите внимание, что метод run_service использует только методы базового абстрактного класса DataProcessor
        и, таким образом, будет выполняться для любого типа обработчика данных (CSV или TXT), что позволяет в дальнейшем 
        расширять приложение, просто добавляя другие классы обработчиков, которые, например, работают с базой данных или
        сетевым хранилищем файлов (например, FTP-сервером).
    """

    def run_service(self):
        """ Метод, который запускает сервис обработки данных  """
        processor = self.processor_fabric.get_processor(self.datasource)        # Инициализируем обработчик
        if processor is not None:
            processor.run()
            processor.print_result()
        else:
            print('Nothing to run')
        # после завершения обработки, запускаем необходимые методы для работы с БД
        self.save_to_database(processor.result)

    def save_to_database(self, result: DataFrame) -> None:
        """ Сохранение данных в БД """
        db_connector = None
        if result is not None:
            try:
                db_connector = SQLStoreConnectorFactory().get_connector(self.db_connection_url)  # инициализируем соединение
                db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)
                insert_into_source_files(db_connector, self.datasource)  # сохраняем в БД информацию о новом файле с набором данных
                print(select_all_from_source_files(db_connector))  # вывод списка всех обработанных файлов
                insert_rows_into_processed_data(db_connector, result)  # записываем в БД результат обработки набора данных
            except Exception as e:
                print(e)
            finally:
                if db_connector is not None:
                    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
                    db_connector.close()            # Завершаем работу с БД

    def find_player(self, name_of_player_or_team):
        db_connector = None
        row_player = []
        row_team = []

        if name_of_player_or_team is not None:
            try:
                db_connector = SQLStoreConnectorFactory().get_connector(self.db_connection_url)  # инициализируем соединение
                db_connector.start_transaction()  # начинаем выполнение запросов (открываем транзакцию)

                row_player = select_by_name(db_connector, name_of_player_or_team)
                name_of_player_or_team += ' '
                row_team = select_by_team(db_connector, name_of_player_or_team)

                print(row_player)
                print(row_team)
            except Exception as e:
                print(e)
            finally:
                if db_connector is not None:
                    db_connector.end_transaction()  # завершаем выполнение запросов (закрываем транзакцию)
                    db_connector.close()            # Завершаем работу с БД
                    if (len(row_team)):
                        return row_team
                    elif (len(row_player)):
                        return row_player
                    else:
                        return None
