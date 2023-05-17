from processor.dataprocessor_service import DataProcessorService
from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

place_holder = '''
                <form method="post">
                    <label>Введите имя игрока или название команды:</label>
                    <input type="text" name="text" value="{}">
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
        
        return index_html.format('', '')
    return place_holder.format('', '')


if __name__ == '__main__':
    service = DataProcessorService(datasource="FIFA-21 Complete.csv", db_connection_url="sqlite:///main.db")
    #service.run_service() # Запуск обработки данных
    app.run() # Запуск Flask приложения