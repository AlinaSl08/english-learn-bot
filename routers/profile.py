from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.profile_kb import profile_kb, settings_kb, reset_confirm_kb, change_level_kb
from keyboards.menu_kb import menu_kb
from keyboards.payment_kb import subscription_kb
from states.menu_state import Menu

profile_router = Router()

@profile_router.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    await call.answer()
    await safe_delete(call.message)
    # берем уровень из sql, допилить
    await call.message.answer("Рады видеть тебя в профиле! 👋"
                              "\n\nТвой текущий уровень — A1. Ты отлично справляешься! ✨"
                              "Чтобы открыть больше возможностей, загляни в раздел подписки. 💎"
                              "\n\nИспользуй кнопки ниже для навигации 👇:", reply_markup=profile_kb())


#--СТАТИСТИКА--
@profile_router.callback_query(F.data == "statistics")
async def statistics(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    await call.message.answer("Прогресс выполненных тем\тестов. \n\nСлабые темы:🔒")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)




#--ПОДПИСКА--
@profile_router.callback_query(F.data == "subscription")
async def subscription(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    #тариф и баланс берем из sql
    await call.message.answer("Ваш тариф: Базовый 📦\nПодписка: не активирована 🔒\nБаланс: 0руб 💰\n\n"
                              "🚀 Тарифы:\n\n📦 Базовый — отличный старт для ежедневной практики:"
                              "\n\n• 100 карточек со словами для твоего словаря."
                              "\n• Тесты (по 2 вопроса на тему) для закрепления."
                              "\n• 10 токенов для общения с ИИ."
                              "\n• Доступ к ИИ-учителю по ключевым темам."
                              "\n\n💎 Премиум — полный безлимит и быстрый результат:"
                              "\n\n• Все фишки Базового, но в тройном объеме (300 карточек!)."
                              "\n• Углубленные тесты: по 5 вопросов на каждую тему."
                              "\n• Абсолютный безлимит общения с ИИ."
                              "\n• Твой личный ИИ-учитель всегда под рукой: и в конкретных темах, и в свободном чате.", reply_markup=subscription_kb())





@profile_router.callback_query(F.data == "back_to_profile")
async def back(call: CallbackQuery):
    await call.answer()
    await safe_delete(call.message)
    await call.answer("Возвращаемся назад...")
    # берем уровень из sql, допилить
    await call.message.answer("\n\nТвой текущий уровень — A1. Ты отлично справляешься! ✨"
                              "Чтобы открыть больше возможностей, загляни в раздел подписки. 💎"
                              "\n\nИспользуй кнопки ниже для навигации 👇:", reply_markup=profile_kb())




#--НАСТРОЙКИ--
@profile_router.callback_query(F.data == "settings")
async def settings(call: CallbackQuery):
    await call.answer()
    await safe_delete(call.message)
    # берем уровень из sql, допилить
    await call.message.answer("Ваш уровень сейчас A1."
                              "\nВы можете изменить его пройдя тест или закончив изучение тем и тестов для предыдущих уровней",
                              reply_markup=settings_kb())


@profile_router.callback_query(F.data == "reset_test_results")
async def reset_test_results(call: CallbackQuery ):
    await call.answer()
    await safe_delete(call.message)
    await call.message.answer("⚠️ Вы уверены, что хотите удалить результаты всех тестов? Восстановить данные не получится",
                              reply_markup=reset_confirm_kb())


@profile_router.callback_query(F.data.startswith("reset_"))
async def reset_confirm(call: CallbackQuery, state: FSMContext):
    await call.answer()
    confirm = call.data.split("_")[1]
    if confirm == "yes":
        await call.message.answer("Результаты тестов были очищены!")
    else:
        await call.message.answer("Очистка отменена!")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)


@profile_router.callback_query(F.data == "change_level")
async def change_level(call: CallbackQuery):
    await call.answer()
    await safe_delete(call.message)
    await call.message.answer("Вы можете изменить уровень на предыдущий или пройти тест, чтобы открыть доступ к уровням выше", reply_markup=change_level_kb(mode_key=2))


@profile_router.callback_query(F.data.startswith("level_selected_"))
async def level_selected(call: CallbackQuery, state: FSMContext):
    await call.answer()
    num_level = int(call.data.split("_")[2])
    await safe_delete(call.message)
    await call.message.answer(f"Ваш уровень изменен на {num_level}")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)




@profile_router.callback_query(F.data == "back_to_settings")
async def back_to_settings(call: CallbackQuery):
    await call.answer()
    await safe_delete(call.message)
    #берем уровень из sql, допилить
    await call.answer("Возвращаемся назад...")
    await call.message.answer("Ваш уровень сейчас A1."
                              "\nВы можете изменить его пройдя тест или закончив изучение тем и тестов для предыдущих уровней",
                              reply_markup=settings_kb())


#--ВЕРНУТЬСЯ В МЕНЮ--
@profile_router.callback_query(F.data == "cancel_menu")
async def cancel_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await safe_delete(call.message)
    await state.clear()
    await call.answer("Возвращаемся в меню...")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.set_state(Menu.menu)
    await state.update_data(last_msg_id=bot_msg.message_id)
