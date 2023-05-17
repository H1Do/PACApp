from typing import List

from .connector import StoreConnector
from pandas import DataFrame, Series
from datetime import datetime

"""
    В данном модуле реализуется API (Application Programming Interface)
    для взаимодействия с БД с помощью объектов-коннекторов.
    
    ВАЖНО! Методы должны быть названы таким образом, чтобы по названию
    можно было понять выполняемые действия.
"""

def select_all_from_source_files(connector: StoreConnector) -> List[tuple]:
    """ Вывод списка обработанных файлов с сортировкой по дате в порядке убывания (DESCENDING) """
    query = f'SELECT * FROM source_files ORDER BY processed DESC'
    result = connector.execute(query).fetchall()
    return result

def select_by_name(connector: StoreConnector, name):
    row = connector.execute('''SELECT * FROM processed_data WHERE name=?''', (name,)).fetchall()
    return row

def select_by_team(connector: StoreConnector, team):
    row = connector.execute('''SELECT * FROM processed_data WHERE team=?''', (team,)).fetchall()
    return row


def insert_into_source_files(connector: StoreConnector, filename: str):
    """ Вставка в таблицу обработанных файлов """
    now = datetime.now()        # текущая дата и время
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")   # преобразуем дату в формат SQL, например, '2022-11-15 22:03:16'
    query = f'INSERT INTO source_files (filename, processed) VALUES (\'{filename}\', \'{date_time}\')'
    result = connector.execute(query)
    return result


def insert_rows_into_processed_data(connector: StoreConnector, dataframe: DataFrame):
    """ Вставка строк из DataFrame в БД с привязкой данных к последнему обработанному файлу (по дате) """
    rows = dataframe.to_dict('records')
    files_list = select_all_from_source_files(connector)    # получаем список обработанных файлов
    # т.к. строка БД после выполнения SELECT возвращается в виде объекта tuple, например:
    # row = (1, 'seeds_dataset.csv', '2022-11-15 22:03:16'),
    # то значение соответствующей колонки можно получить по индексу, например id = row[0]
    last_file_id = files_list[0][0]  # получаем индекс последней записи из таблицы с файлами
    if len(files_list) > 0:
        for row in rows:
            connector.execute("""INSERT INTO processed_data (id, name, nationality, position, overall, age, hits, potential, team, source_files)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (row['player_id'], row['name'], row['nationality'], row['position'], row['overall'], row['age'], row['hits'], row['potential'], row['team'], last_file_id))
    else:
        print('File records not found. Data inserting was canceled.')

def insert(connector: StoreConnector, name, nationality, position, overall, age, hits, potential, team):
    connector.execute('''INSERT INTO processed_data
                 (name, nationality, position, overall, age, hits, potential, team)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (name, nationality, position, overall, age, hits, potential, team))
    connector.close()

def select_all(connector: StoreConnector):
    rows = connector.execute('''SELECT * FROM processed_data''').fetchall()
    connector.close()
    return rows

def update(connector: StoreConnector, id, nationality, position, overall, age, hits, potential, team):
    connector.execute('''UPDATE processed_data SET nationality=?, position=?, overall=?, age=?, hits=?, potential=?, team=? WHERE id=?''',
               (nationality, position, overall, age, hits, potential, team, id))
    connector.close()

def delete(connector: StoreConnector, name):
    connector.execute('''DELETE FROM processed_data WHERE name=?''', (name,))
    connector.close()