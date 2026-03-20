from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.profile_kb import change_level_kb
from keyboards.theme_kb import themes_kb
from keyboards.menu_kb import menu_kb
from states.practice_state import Practice
from keyboards.tests_kb import questions_kb, answers_kb, start_level_test, level_test_answers_kb, level_test_end
from database.gspread_db import get_questions_and_answers, get_questions_and_answers_level
from states.menu_state import Menu
from states.test_level_state import TestLevel

tests_router = Router()

#выбор уровня
@tests_router.callback_query(F.data == "tests")
async def tests(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    bot_msg = await call.message.answer("Выберите уровень:", reply_markup=change_level_kb(mode_key=1))
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Practice.level)


@tests_router.message(Practice.level)
async def level_selection_for_test(message: Message, state: FSMContext):
    bot_msg = await message.answer(
        "Пожалуйста, выберите уровень с помощью кнопок ниже 👇", reply_markup=change_level_kb(mode_key=1)
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)

#выбор темы
@tests_router.callback_query(F.data.startswith("test_level_"))
async def test_level(call: CallbackQuery, state: FSMContext):
    await call.answer()
    level_num = int(call.data.split("_")[2])
    await safe_delete(call.message)
    await state.update_data(level=level_num, mode='test')
    bot_msg = await call.message.answer("Выберите тему:", reply_markup=themes_kb(mode_key=1, level=level_num, page=1))
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Practice.theme)

@tests_router.callback_query(F.data == "back_to_theme_test")
async def back_to_theme_test(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    data = await state.get_data()
    level_num = data.get("level")
    bot_msg = await call.message.answer("Выберите тему:", reply_markup=themes_kb(mode_key=1, level=level_num, page=1))
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Practice.theme)

@tests_router.message(Practice.theme)
async def theme_selection_for_test(message: Message, state: FSMContext):
    data = await state.get_data()
    level_num = data.get("level")
    bot_msg = await message.answer(
        "Пожалуйста, выберите тему с помощью кнопок ниже 👇", reply_markup=themes_kb(mode_key=1, level=level_num, page=1)
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)

#выбор вопроса
@tests_router.callback_query(F.data.startswith("test_theme_"))
async def test_theme(call: CallbackQuery, state: FSMContext):
    await call.answer()
    theme_num = int(call.data.split("_")[2]) + 1
    await safe_delete(call.message)
    await state.update_data(theme=theme_num)
    bot_msg = await call.message.answer("Выберите вопрос:", reply_markup=questions_kb(theme_num))
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Practice.question)

@tests_router.message(Practice.question)
async def question_selection_for_test(message: Message, state: FSMContext):
    data = await state.get_data()
    theme_num = data.get("theme")
    bot_msg = await message.answer(
        "Пожалуйста, выберите вопрос с помощью кнопок ниже 👇", reply_markup=questions_kb(theme_num)
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)


#вопрос с вариантами ответа
@tests_router.callback_query(F.data.startswith("question_"))
async def question(call: CallbackQuery, state: FSMContext):
    await call.answer()
    question_num = int(call.data.split("_")[1])
    await safe_delete(call.message)
    await state.update_data(question=question_num)
    question_text = get_questions_and_answers(question_num)[0]
    bot_msg = await call.message.answer(f"{question_text}\n\nВыберите вариант ответа:", reply_markup=answers_kb(question_num + 1))
    await state.update_data(last_msg_id=bot_msg.message_id)
    #await state.set_state(Practice.question)
    await state.set_state(Practice.answer)


@tests_router.message(Practice.answer)
async def answer_selection_for_test(message: Message, state: FSMContext):
    data = await state.get_data()
    question_num = data.get("question")
    question_text = get_questions_and_answers(question_num)[0]
    bot_msg = await message.answer(
        f"{question_text}\n\nПожалуйста, выберите вариант ответа с помощью кнопок ниже 👇", reply_markup=answers_kb(question_num + 1))
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id)

@tests_router.callback_query(F.data == "back_to_questions_test")
async def back_to_questions_test(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    data = await state.get_data()
    theme_num = data.get("theme")
    bot_msg = await call.message.answer("Выберите вопрос:", reply_markup=questions_kb(theme_num))
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(Practice.question)

@tests_router.callback_query(F.data.startswith("answer_"))
async def answer(call: CallbackQuery, state: FSMContext):
    answer_num = int(call.data.split("_")[1])
    await safe_delete(call.message)
    await state.update_data(answer=answer_num)
    #тут сохраняем ответ в sql и после уже очищаем
    await call.answer("Ваш ответ сохранен и дальше следующий вопрос")
    await state.clear()
    await state.set_state(Menu.menu)
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)





#тест на уровень пользователя, начало
@tests_router.callback_query(F.data == "test_level")
async def general_level_test(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    await state.clear()
    bot_msg = await call.message.answer("Этот тест поможет точно определить ваш уровень английского! 📈\n\n"
                                        "<b>Маленький совет:</b> старайтесь отвечать самостоятельно. "
                                        "Это важно, чтобы программа обучения идеально подошла под ваши знания и помогла прогрессировать быстрее.🚀\n\n"
                                        "Good luck! Желаю удачи! ✨", reply_markup=start_level_test(), parse_mode="HTML")
    await state.update_data(last_msg_id=bot_msg.message_id, question_num=1)
    await state.set_state(TestLevel.question0)

@tests_router.message(TestLevel.question0)
async def level_selection(message: Message, state: FSMContext):
    bot_msg = await message.answer(
        "Пожалуйста, выберите действие с помощью кнопок ниже 👇", reply_markup=start_level_test()
    )
    data = await state.get_data()
    last_msg_id = data.get("last_msg_id")
    await delete_last_message(last_msg_id, message)
    await state.update_data(last_msg_id=bot_msg.message_id, question_num=1)


@tests_router.callback_query(F.data == "questions_go")
async def questions_go(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    data = await state.get_data()
    question_num = data.get("question_num")
    question = get_questions_and_answers_level(question_num - 1)[0]
    bot_msg = await call.message.answer(f"Вопрос №{question_num}:\n\n{question}", reply_markup=level_test_answers_kb(question_num))
    await state.update_data(last_msg_id=bot_msg.message_id)
    await state.set_state(TestLevel.question0)

@tests_router.callback_query(F.data.startswith("testlevel_answer_"))
async def level_answers(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    answer_num = int(call.data.split('_')[2])
    new_question_num = int(call.data.split('_')[4])
    if new_question_num == 11:
        #тут сравниваем ответ пользователя с sql и если тру записываем чтобы потом вывести кол-во правильных ответов
        points = 0
        if 0 <= points <= 3:
            level = 'Уровень A1 (Beginner)'
            explanation = 'Повторите личные местоимения и Present Simple.'
        elif 4 <= points <= 6:
            level = 'Уровень A2 (Elementary)'
            explanation = 'Закрепите разницу между Past Simple и Present Perfect.'
        elif 7 <= points <= 8:
            level = 'Уровень B1 (Intermediate)'
            explanation = 'Обратите внимание на длительные времена и пассивный залог.'
        else:
            level = 'Уровень B2 (Upper-Intermediate)'
            explanation = 'Вы отлично владеете сложными оборотами и сослагательным наклонением!'
        bot_msg = await call.message.answer(f"Тест завершен! ✅\nВаш уровень: {level}.\nБаллов за тест: {points}/10\n\n💡 {explanation}",
                                            reply_markup=level_test_end())
        await state.update_data(last_msg_id=bot_msg.message_id)
        await state.set_state(TestLevel.question_completed)

    else:
        question = get_questions_and_answers_level(new_question_num - 1)[0]
        bot_msg = await call.message.answer(f"Вопрос №{new_question_num}:\n\n{question}", reply_markup=level_test_answers_kb(new_question_num))
        await state.update_data(last_msg_id=bot_msg.message_id, question_num=new_question_num)
        state_num = f'question{new_question_num - 1}'
        question_state = getattr(TestLevel, state_num)
        await state.set_state(question_state)
        current_state = await state.get_state()
        print(f"Вы ответили на вопрос из состояния: {current_state}")


@tests_router.message(
    StateFilter(
         TestLevel.question0, TestLevel.question1, TestLevel.question2,
        TestLevel.question3, TestLevel.question4, TestLevel.question5,
        TestLevel.question6, TestLevel.question7, TestLevel.question8,
        TestLevel.question9, TestLevel.question10, TestLevel.question_completed
    )
)
async def universal_question_handler(message: Message, state: FSMContext):
    #Получаем текущее состояние, чтобы понять, на каком мы вопросе
    current_state = await state.get_state()
    print(f"Вы ответили на вопрос из состояния: {current_state}")
    data = await state.get_data()
    question_num = data.get("question_num")
    if current_state != TestLevel.question_completed:
        question = get_questions_and_answers_level(question_num - 1)[0]
        bot_msg = await message.answer(
            f"Вопрос №{question_num}:\n\n{question}\n\nПожалуйста, выберите действие с помощью кнопок ниже 👇",
            reply_markup=level_test_answers_kb(question_num))
        last_msg_id = data.get("last_msg_id")
        await delete_last_message(last_msg_id, message)
        await state.update_data(last_msg_id=bot_msg.message_id, question_num=1)
    else:
        bot_msg = await message.answer(
            "Пожалуйста, выберите действие с помощью кнопок ниже 👇",
            reply_markup=level_test_end())
        last_msg_id = data.get("last_msg_id")
        await delete_last_message(last_msg_id, message)
        await state.update_data(last_msg_id=bot_msg.message_id)
