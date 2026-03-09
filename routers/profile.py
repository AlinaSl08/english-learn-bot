from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.profile_kb import profile_kb, subscription_kb, payment_method_kb, settings_kb, reset_confirm_kb, change_level_kb
from keyboards.menu_kb import menu_kb
from states.menu_state import Menu

profile_router = Router()

@profile_router.callback_query(F.data == "profile")
async def profile(call: CallbackQuery):
    await safe_delete(call.message)
    await call.message.answer("Рады видеть тебя в профиле! 👋"
                              "\n\nТвой текущий уровень — 1. Ты отлично справляешься! "
                              "Чтобы открыть больше возможностей, загляни в раздел подписки."
                              "\n\nИспользуй кнопки ниже для навигации:", reply_markup=profile_kb())
    await call.answer()

#--СТАТИСТИКА--
@profile_router.callback_query(F.data == "statistics")
async def statistics(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await call.message.answer("Прогресс выполненных тем\тестов. \n\nСлабые темы:🔒")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()



#--ПОДПИСКА--
@profile_router.callback_query(F.data == "subscription")
async def subscription(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await call.message.answer("Ваш тариф: Базовый\nПодписка: не активирована\nБаланс: 100руб\n\n"
                              "Тарифы:\nБазовый\nВключает в себя:...\nПремиум\nВключает в себя:...", reply_markup=subscription_kb())
    await call.answer()

@profile_router.callback_query(F.data == "subscribe")
async def subscribe(call: CallbackQuery):
    await safe_delete(call.message)
    await call.message.answer("Каким способом удобней провести оплату?", reply_markup=payment_method_kb())
    await call.answer()

@profile_router.callback_query(F.data.startswith("payment_"))
async def payment_method(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    method_num = int(call.data.split("_")[1])
    await call.message.answer(f"Вы выбрали способ оплаты {method_num}")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()

@profile_router.callback_query(F.data == "back_to_profile")
async def back(call: CallbackQuery):
    await safe_delete(call.message)
    await call.answer("Возвращаемся назад...")
    await call.message.answer("\n\nТвой текущий уровень — 1. Ты отлично справляешься! "
                              "Чтобы открыть больше возможностей, загляни в раздел подписки."
                              "\n\nИспользуй кнопки ниже для навигации:", reply_markup=profile_kb())
    await call.answer()



#--НАСТРОЙКИ--
@profile_router.callback_query(F.data == "settings")
async def settings(call: CallbackQuery):
    await safe_delete(call.message)
    await call.message.answer("Ваш уровень сейчас 1."
                              "\nВы можете изменить его пройдя тест или закончив изучение тем и тестов для предыдущих уровней",
                              reply_markup=settings_kb())
    await call.answer()

@profile_router.callback_query(F.data == "reset_test_results")
async def reset_test_results(call: CallbackQuery ):
    await safe_delete(call.message)
    await call.message.answer("⚠️ Вы уверены, что хотите удалить результаты всех тестов? Восстановить данные не получится",
                              reply_markup=reset_confirm_kb())
    await call.answer()

@profile_router.callback_query(F.data.startswith("reset_"))
async def reset_confirm(call: CallbackQuery, state: FSMContext):
    confirm = call.data.split("_")[1]
    if confirm == "yes":
        await call.message.answer("Результаты тестов были очищены!")
    else:
        await call.message.answer("Очистка отменена!")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()

@profile_router.callback_query(F.data == "change_level")
async def change_level(call: CallbackQuery):
    await safe_delete(call.message)
    await call.message.answer("Вы можете изменить уровень на предыдущий или пройти тест, чтобы открыть доступ к уровням выше", reply_markup=change_level_kb(mode_key=2))
    await call.answer()

@profile_router.callback_query(F.data.startswith("level_selected_"))
async def level_selected(call: CallbackQuery, state: FSMContext):
    num_level = int(call.data.split("_")[2])
    await safe_delete(call.message)
    await call.message.answer(f"Ваш уровень изменен на {num_level}")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()



@profile_router.callback_query(F.data == "back_to_settings")
async def back_to_settings(call: CallbackQuery):
    await safe_delete(call.message)
    await call.answer("Возвращаемся назад...")
    await call.message.answer("Ваш уровень сейчас 1."
                              "\nВы можете изменить его пройдя тест или закончив изучение тем и тестов для предыдущих уровней",
                              reply_markup=settings_kb())
    await call.answer()

#--ВЕРНУТЬСЯ В МЕНЮ--
@profile_router.callback_query(F.data == "cancel_menu")
async def cancel_menu(call: CallbackQuery, state: FSMContext):
    await safe_delete(call.message)
    await state.clear()
    await call.answer("Возвращаемся в меню...")
    bot_msg = await call.message.answer("Выберите действие:", reply_markup=menu_kb())
    await state.set_state(Menu.menu)
    await state.update_data(last_msg_id=bot_msg.message_id)
    await call.answer()