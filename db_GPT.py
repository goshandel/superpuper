import sqlite3


class Database_gpt:
    def __init__(self):
        self.connect = sqlite3.connect('gpt.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS gpt 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT,
                        nickname TEXT,
                        qestion TEXT,
                        answer TEXT,
                        )""")
        self.connect.commit()

    def check_user_exists(self, id, user_name, nickname):
        self.cursor.execute("""SELECT id, user_name, nickname FROM gpt
                             WHERE id = ?
                             OR user_name = ?
                             OR nickname = ?""",
                            (id, user_name, nickname))
        data = self.cursor.fetchone()
        return data is not None

    def add_user(self, id, user_name, nickname):
        self.cursor.execute("INSERT INTO gpt VALUES(?,?,?,?,?);",
                            (id, user_name, nickname, '', ''))
        self.connect.commit()

    def close(self):
        self.connect.close()

class Getting_qestion:
    def __init__(self):
        self.connect = sqlite3.connect('gpt.db')
        self.cursor = self.connect.cursor()

    def super(self, qestion, id):
        self.cursor.execute("UPDATE gpt SET qestion = ? WHERE id = ?",
                            (qestion, id))
        self.connect.commit()

    def close(self):
        self.connect.close()

class Getting_answer:
    def __init__(self):
        self.connect = sqlite3.connect('gpt.db')
        self.cursor = self.connect.cursor()

    def wow(self, answer, id):
        self.cursor.execute("UPDATE gpt SET answer = ? WHERE id = ?",
                            (answer, id))
        self.connect.commit()

    def close(self):
        self.connect.close()

class Send_answer:
    def __init__(self):
        self.connect = sqlite3.connect('gpt.db')
        self.cursor = self.connect.cursor()

    def bugaga(self, user_id):
        self.cursor.execute("SELECT answer FROM gpt WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.connect.close()