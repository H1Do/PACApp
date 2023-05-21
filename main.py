from processor.dataprocessor_service import DataProcessorService
from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

place_holder = '''
                <head>
                <title>Поиск игроков FIFA-2021</title>
                <style>
                    table {
                        width: 100%;
                        margin-bottom: 20px;
                        border: 5px solid #fff;
                        border-top: 5px solid #fff;
                        border-bottom: 3px solid #fff;
                        border-collapse: collapse; 
                        outline: 3px solid #ffd300;
                        font-size: 15px;
                        background: #fff!important;
                    }
                    table th {
                        font-weight: bold;
                        padding: 7px;
                        background: #ffd300;
                        border: none;
                        text-align: left;
                        font-size: 15px;
                        border-top: 3px solid #fff;
                        border-bottom: 3px solid #ffd300;
                    }
                    table td {
                        padding: 7px;
                        border: none;
                        border-top: 3px solid #fff;
                        border-bottom: 3px solid #fff;
                        font-size: 15px;
                    }
                    table tbody tr:nth-child(even){
                        background: #f8f8f8!important;
                    }
                    label {
                        text-align: left;
                        font-size: 30px;
                        border-top: 3px solid #fff;
                        border-bottom: 3px solid #ffd300;
                    }
                    input[type = "text"] {
                        font-size: 30px;
                        width: 300px;
                        height: 40px;
                    }
                    input[type = "submit"] {
                        height: 40px;
                        font-size: 30px;
                        width: 120px;
                        text-align: center;
                        background-color: rgb( 43, 153, 91 );
                    }
                </style>
                </head>
                <form method="post">
                    <label>Введите имя игрока или название команды:</label>
                    <input type="text" name="text" value="">
                    <input type="submit" value="Найти">
                </form>
                '''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']

        list_of_player = service.find_player(text)

        df = pd.DataFrame(list_of_player, columns=['id игрока', 'Имя', 'Национальность', 'Игровая позиция', 'Общая оценка', 'Возраст', 'Кол-во голов', 'Потенциал', 'Команда', '№ файла'])
        
        result_html = df.to_html()

        index_html = place_holder + result_html
        
        return index_html
    return place_holder


if __name__ == '__main__':
    service = DataProcessorService(datasource="FIFA-21 Complete.csv", db_connection_url="sqlite:///main.db")
    #service.run_service() # Запуск обработки данных
    app.run() # Запуск Flask приложения