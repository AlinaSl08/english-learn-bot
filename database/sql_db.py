import mysql.connector
import os
from dotenv import load_dotenv
from database.gspread_db import cache

load_dotenv('../.env')
PASSWORD = os.getenv("PASSWORD_DB")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")


class Database:
    def __init__(self, db_host, db_user, password, port):
        self.db_config = {
            'host': db_host,
            'user': db_user,
            'password': password,
            'port': port}
        self.__conn = None


    def connect_db(self):
        try:
            self.__conn = mysql.connector.connect(**self.db_config)
            print("Подключение успешно!")
            return self.__conn
        except Exception as e:
            print("Подключение не удалось! Ошибка:", e)
            return None

    def sync_sql_to_db(self):
        if not self.connect_db():
            return
        cursor = self.__conn.cursor()

        def safe_int(value):
            try:
                return int(str(value).strip())
            except (ValueError, TypeError):
                return 0

        try:
            if cache["sql_answers"]:
                cleaned_answers = [(str(ans).strip(),) for ans in cache["sql_answers"] if ans]
                sql_ans = "INSERT IGNORE INTO answers_test (answer) VALUES (%s)"
                cursor.executemany(sql_ans, cleaned_answers)

            if cache["sql_questions"]:
                cleaned_questions = []
                for row in cache["sql_questions"]:
                    if len(row) >= 2:
                        text = str(row[0])
                        level_id = safe_int(row[1])
                        cleaned_questions.append((text, level_id))
                sql = "INSERT IGNORE INTO questions (question, level_id) VALUES (%s, %s)"
                # cache["sql_questions"] уже содержит список списков [['Текст', '1'], ...]
                cursor.executemany(sql, cleaned_questions)

            if cache["sql_topics"]:
                cleaned_topics = []
                for row in cache["sql_topics"]:
                    if len(row) >= 2:
                        name = str(row[0])
                        level_id = safe_int(row[1])
                        cleaned_topics.append((name, level_id))
                sql_top = "INSERT IGNORE INTO topics_progress (topic, level_id) VALUES (%s, %s)"
                cursor.executemany(sql_top, cleaned_topics)
            if cache["sql_relations"]:
                cleaned_relations = []
                for row in cache["sql_relations"]:
                    q_id = safe_int(row[0])
                    a_id = safe_int(row[1])
                    is_correct = 1 if str(row[2]).upper() == 'TRUE' else 0
                    cleaned_relations.append((q_id, a_id, is_correct))
                sql_rel = "INSERT IGNORE INTO correct_answers_to_tests (question_id, answer_id, is_correct) VALUES (%s, %s, %s)"
                cursor.executemany(sql_rel, cleaned_relations)
            self.__conn.commit()
            print("Данные успешно синхронизированы (числа обработаны)!")
        except Exception as e:
            print(f"Ошибка при синхронизации: {e}")
            self.__conn.rollback()
        finally:
            cursor.close()
            self.__conn.close()



    # отключаемся от бд
    def close_conn(self):
        self.__conn.close()


database = Database(DB_HOST, DB_USER, PASSWORD,3306)