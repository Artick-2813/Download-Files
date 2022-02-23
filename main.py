from flask import Flask, render_template, request, g, redirect, send_from_directory, abort, flash
import sqlite3
from FDataBase import FDataBase
from werkzeug.utils import secure_filename
import os

DATABASE = 'DataBaseImages.db'
SECRET_KEY = '5f352379324c22463451387a0aec5d2f'
UPLOADER_FOLDER = r'C:\Users\Admin\PycharmProjects\sqlite3\SaveImages'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOADER_FOLDER'] = UPLOADER_FOLDER
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'DataBaseImages.db')))


def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
            print('База данных успешно создана!')
        db.commit()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/", methods=['POST', 'GET'])
def main():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':

        file = request.files['file']

        if file.filename == '':
            flash('Выберите,пожалуйста, файл для загрузки', category='FileNot')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            title = filename.rsplit('.', 1)[0]
            resolution = filename.rsplit('.', 1)[1]

            file.save(os.path.join(app.config['UPLOADER_FOLDER'], filename))

            res = dbase.addImage(title, resolution)

            if res:

                return render_template('LinksImages.html', pic=dbase.getPictureAnonce())
            else:
                print('Ошибка внесения в БД')
        else:
            flash('Неверное разрешение файла для загрузки!', category='FileNot')
            return redirect(request.url)

    return render_template('main.html', title='Главная')


@app.route('/uploads/<int:id_image>')
def uploads(id_image):
    db = get_db()
    dbase = FDataBase(db)

    title, resolution, id_image = dbase.getDataImage(id_image)
    title_image = title.replace('_', ' ')

    if title:

        filename = title + '.' + resolution

        return render_template('images.html', filename=filename, title_image=title_image, id_image=id_image)
    return abort(404)


@app.route('/send_img/<filename>')
def send_img(filename):

    return send_from_directory(app.config['UPLOADER_FOLDER'], filename)


@app.route('/picture')
def ShowLinksPicture():
    db = get_db()
    dbase = FDataBase(db)
    info = dbase.getPictureAnonce()

    return render_template('LinksImages.html',  pic=info)


@app.route('/remove/<int:id_image>')
def remove(id_image):
    db = get_db()
    dbase = FDataBase(db)

    title, resolution, id = dbase.getDataImage(id_image)

    filename = title + '.' + resolution

    file = fr'\SaveImages\{filename}'
    path = os.getcwd()

    all_path = path + file
    os.remove(all_path)

    dbase.removeDataImage(id_image)

    return render_template('success.html', title='Удаление файла')



create_db()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
