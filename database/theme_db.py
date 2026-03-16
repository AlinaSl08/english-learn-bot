import gspread_asyncio
from google.oauth2.service_account import Credentials
import os
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'english-project-489515-72e378e63ef0.json')

def get_creds():
    # Тот же путь к JSON, что и был
    creds = Credentials.from_service_account_file(json_path)
    scoped = creds.with_scopes([
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ])
    return scoped

agcm = gspread_asyncio.AsyncioGspreadClientManager(get_creds)

cache = {"theories": [], "topics": [],
    "words": [], "words_card": []}


async def update_cache():
    client = await agcm.authorize()
    spreadsheet = await client.open("English Bot")

    # Лист 1
    sheet1 = await spreadsheet.get_worksheet(0)
    data1 = await sheet1.get_all_records()
    cache["theories"] = [row['Теория'] for row in data1]
    cache["topics"] = [row['Тема'] for row in data1]
    # Лист 2
    sheet2 = await spreadsheet.worksheet('Карточки слов')
    data2 = await sheet2.get_all_records()
    cache["words"] = [row['Слова'] for row in data2]
    cache["words_card"] = [row['Карточка слова'] for row in data2]
    # Лист 3
    sheet3 = await spreadsheet.worksheet('Практика')
    data3 = await sheet3.get_all_records()
    cache["questions"] = [row['Вопрос'] for row in data3]
    cache["answers"] = [row['Варианты ответов'] for row in data3]
    cache["explanation_of_errors"] = [row['Пояснение к ошибкам'] for row in data3]
    # Лист 4
    sheet4 = await spreadsheet.worksheet('Тест на уровень')
    data4 = await sheet4.get_all_records()
    cache["questions_level"] = [row['Вопрос'] for row in data4]
    cache["answers_level"] = [row['Варианты ответов'] for row in data4]
    cache["explanation_of_errors_level"] = [row['Пояснение к ошибкам'] for row in data4]
    logging.info("Кеш успешно обновлен!")




def get_topics_and_theory(topic_idx):
    try:
        theory = cache["theories"][topic_idx]
        topic = cache["topics"][topic_idx]
        return [theory, topic]
    except (IndexError, KeyError):
        return ["Теория не найдена", "Тема не найдена"]


def get_questions_and_answers(topic_idx):
    try:
        question = cache["questions"][topic_idx]
        answer = cache["answers"][topic_idx]
        explanation_of_errors = cache["explanation_of_errors"][topic_idx]
        return [question, answer, explanation_of_errors]
    except (IndexError, KeyError):
        return ["Вопрос не найден", "Ответ не найден"]

def get_words_and_card_words(topic_idx):
    try:
        word = cache["words"][topic_idx]
        word_card = cache["words_card"][topic_idx]
        return [word, word_card]
    except (IndexError, KeyError):
        return ["Слово не найдено", "Карточка слова не найдена"]

def get_questions_and_answers_level(topic_idx):
    try:
        question_level = cache["questions_level"][topic_idx]
        answer_level = cache["answers_level"][topic_idx]
        explanation_of_errors_level = cache["explanation_of_errors_level"][topic_idx]
        return [question_level, answer_level, explanation_of_errors_level]
    except (IndexError, KeyError):
        return ["Вопрос не найден", "Ответ не найден"]