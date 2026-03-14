import gspread_asyncio
from google.oauth2.service_account import Credentials
import os


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

cache = {"theories": [],
    "words": [], "words_card": []}


async def update_cache():
    client = await agcm.authorize()
    spreadsheet = await client.open("English Bot")

    # Лист 1
    sheet1 = await spreadsheet.get_worksheet(0)
    data1 = await sheet1.get_all_records()
    cache["theories"] = [row['Теория'] for row in data1]

    # Лист 2
    sheet2 = await spreadsheet.worksheet('Карточки слов')
    data2 = await sheet2.get_all_records()
    cache["words"] = [row['Слова'] for row in data2]
    cache["words_card"] = [row['Карточка слова'] for row in data2]
    print("Кеш успешно обновлен!")



def get_topics_and_theory(topic_idx):
    try:
        theory = cache["theories"][topic_idx]
        return theory
    except (IndexError, KeyError):
        return ["Теория не найдена"]



def get_words_and_card_words(topic_idx):
    try:
        word = cache["words"][topic_idx] #брать, если не используется
        word_card = cache["words_card"][topic_idx]
        return [word, word_card]
    except (IndexError, KeyError):
        return ["Слово не найдено", "Карточка слова не найдена"]