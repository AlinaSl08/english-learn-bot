from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.theme_db import get_topics_and_theory


themes = ['Object Pronouns', 'Possessive Adjectives', 'Present Continuous Exercises', 'Present Simple Form',
'Verb To Be Exercises - Use Of Is, Am, Are', 'Was Were Exercises', 'Subject Pronouns',
'A, an, the exercises - Articles in English', 'Countable and Uncountable Nouns Exercises – A, some, any',
'Adverbs of Frequency Exercises – Grammar Practice and Examples', 'There is & There are Exercises – Grammar Practice and Examples',
'Conjunctions: And, but, or, so, because', 'Have Has Exercises', 'Singular and Plural Nouns', 'Tricky Plurals & Exceptions',
'Future Tense – Will', 'Future Tense – Be Going To & Present Continuous ', 'Present Continuous для будущего',
'Past Continuous', 'Когда использовать Past Continuous', 'Past Simple – Форма и правила', 'Past Simple – Отрицания и вопросы',
'Present Simple – Форма и использование', 'Present Continuous – Форма и использование', 'Used To Exercises',
'Relative Pronouns', 'Possessive Pronouns', 'Prepositions of Movement', 'Comparative Adjectives', 'Superlative Adjectives',
'Irregular and Common Adjectives', 'Past Perfect Tense', 'Present Perfect', 'Сравнение Present Perfect и Past Simple',
'Present Perfect Simple vs Present Perfect Continuous', 'Present Perfect Tense', 'Understanding Question Tags',
'Reported Speech – Part 1: What It Is and How It Changes', 'Reported Speech – Part 2: Reporting Verbs and Special Cases',
'Active and Passive Voice – Part 1: What They Are and Examples', 'Active and Passive Voice – Part 2: How to Form and Tips',
'Future Continuous Tense – Form and Use', 'Future Perfect Tense – Form and Use', 'Modal Verbs',
'Participle Clauses – Types and Forms', 'Participle Clauses – Use, Tips and Mistakes', 'Passive Voice – Form and Examples',
'Passive Voice – Use, Active vs Passive, and Tips', 'Defining Relative Clauses – What They Are', 'Defining vs Non-defining Relative Clauses',
'Using "Wish" About the Present and Past', 'Using "Wish" About the Future']


def levels_kb():
    kb = InlineKeyboardBuilder()
    levels = ['Уровень A1', 'Уровень A2', 'Уровень B1', 'Уровень B2']
    for i in range(1, 5):
        kb.button(text=f'Уровень {levels[i - 1]}', callback_data=f'level_{i}')
    kb.button(text='⬅️ Назад', callback_data='cancel_menu')
    kb.button(text='Сдать тест на уровень', callback_data='test_level')
    count = 5
    if count <= 4:
        kb.adjust(1)
    elif count <= 10:
        kb.adjust(2)
    else:
        kb.adjust(3)
    return kb.as_markup()

def themes_kb(mode_key=1, level=1, page=1):
    kb = InlineKeyboardBuilder()
    modes = {1: 'test', 2: 'theory'}
    mode = modes[mode_key]
    if page == 1:
        levels = {1: [0, 7], 2: [15, 22], 3: [28, 35], 4: [41, 47]}
    else:
        levels = {1: [7, 15], 2: [22, 28], 3: [35, 41], 4: [47, 52]}
    for i in range(levels[level][0], levels[level][1]):
        topic  = themes[i]
        if mode == 'theory': #тут добавить проставление галочек(если в sql не 0, то галка есть)
            kb.button(text=topic, callback_data=f'theme_{i}')
        else: #тут добавить проставление галочек(если в sql не 0, то галка есть)
            kb.button(text=topic, callback_data=f'test_theme_{i}')
    if page == 1:
        #kb.button(text=' ', callback_data='cap')
        kb.button(text='>', callback_data='next_theme')
    else:
        kb.button(text='<', callback_data='last_theme')
        #kb.button(text=' ', callback_data='cap')
    if mode == 'theory':
        kb.button(text='⬅️ Назад', callback_data='theme')
    else:
        kb.button(text='⬅️ Назад', callback_data='tests')
    kb.adjust(1)
    return kb.as_markup()



def theory_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='✅ Выучено', callback_data='learned') #сделать изначально без галки, при нажатии чтобы была галка, (если в sql есть, то галка, если нет то вернет null)
    kb.button(text='⬅️ Назад', callback_data='back_to_themes')
    kb.button(text='📝 Перейти к тестам', callback_data='go_to_tests') #сделать переход к тестам по определенной теме
    kb.button(text='⬅️ Вернуться в меню', callback_data='cancel_menu')
    kb.adjust(2, 2)
    return kb.as_markup()
