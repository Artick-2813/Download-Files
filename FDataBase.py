import sqlite3


class FDataBase:
    def __init__(self, db):
        self.db = db
        self.cur = db.cursor()

    def addImage(self, title, resolution, name_file, datetime):
        try:
            self.cur.execute(""" INSERT INTO image VALUES(NULL, ?, ?, ?, ?)""", (title, resolution, datetime,
                                                                                 name_file))
            self.db.commit()
            print('Данные успешно добавлены в БД')

        except sqlite3.Error as e:
            print('Ошибка отправки данных в БД', str(e))
            return False

        return True

    def getDataImage(self, id_img):
        try:
            self.cur.execute(f""" SELECT title, resolution, id FROM image WHERE id = {id_img} LIMIT 1 
""")
            res = self.cur.fetchone()

            if res:
                return res['title'], res['resolution'], res['id']

        except sqlite3.Error as e:
            print('Название не отправлено', str(e))

        return (False, False)

    def getPictureAnonce(self):
        try:
            self.cur.execute(""" SELECT id, title, resolution, name_file, datetime FROM image ORDER BY datetime DESC 
            """)
            res = self.cur.fetchall()

            if res:
                return res

        except sqlite3.Error as e:
            print('Ошибка загрузки картины из БД', str(e))

        return []

    def getIdImage(self):
        try:
            self.cur.execute(""" SELECT id FROM image """)
            res = self.cur.fetchall()

            if res:
                for elem in res:
                    return elem
        except sqlite3.Error as e:
            print('Ошибка загрузки картины из БД', str(e))

        return []

    def removeDataImage(self, id):
        try:
            self.cur.execute(f""" DELETE from image WHERE id = {id} """)
            self.db.commit()
            self.cur.close()

            print(f'Запись удалена из БД')
            return True

        except sqlite3.Error as e:
            print('Ошибка загрузки картины из БД', str(e))

            return False


