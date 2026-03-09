import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'english-project-489515-72e378e63ef0.json')

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

spreadsheet = client.open("English Bot")
sheet1 = spreadsheet.get_worksheet(0)

data1 = sheet1.get_all_records()

CACHED_TOPICS = [row['Тема'] for row in data1]
CACHED_THEORIES = [row['Теория'] for row in data1]


sheet2 = spreadsheet.worksheet('Карточки слов')
data2 = sheet2.get_all_records()
CACHED_WORDS = [row['Слова'] for row in data2]
CACHED_TRANSLATIONS = [row['Карточка слова'] for row in data2]

def get_topics_and_theory(topic_idx):
    try:
        theory = CACHED_THEORIES[topic_idx]
        topic = CACHED_TOPICS[topic_idx]
        return [theory, topic]
    except IndexError:
        return ["Теория не найдена", "Тема не найдена"]


def get_words_and_card_words(word_idx):
    try:
        word = CACHED_WORDS[word_idx]
        card_word = CACHED_TRANSLATIONS[word_idx]
        return [word, card_word]
    except IndexError:
        return ["Слово не найдено", "Карточка не найдена"]

