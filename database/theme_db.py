import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('english-project-489515-72e378e63ef0.json', scope)

client = gspread.authorize(creds)

sheet = client.open("English Bot").sheet1

def get_topics_and_theory():
    data = sheet.get_all_records()  # Получаем все записи
    topics = []
    theories = []

    for row in data:
        topics.append(row['Тема'])  # Извлекаем темы
        theories.append(row['Теория'])  # Извлекаем теорию

    return topics, theories

# Пример использования
topics, theories = get_topics_and_theory()
print("Темы:", topics)
print("Теории:", theories)