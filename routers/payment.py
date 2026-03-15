from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery
from os import getenv
from utils.delete_last_message import safe_delete, delete_last_message
from keyboards.payment_kb import payment_method_kb
from keyboards.menu_kb import menu_kb
import logging

payment_router = Router()
PAYMENT_TOKEN = getenv("PAYMENT_TOKEN")

@payment_router.callback_query(F.data == "subscribe")
async def subscribe(call: CallbackQuery):
    await call.answer()
    await safe_delete(call.message)
    await call.message.answer("Каким способом удобней провести оплату?", reply_markup=payment_method_kb())


@payment_router.callback_query(F.data.startswith("payment_"))
async def payment_method(call: CallbackQuery, state: FSMContext):
    await call.answer()
    method_num = int(call.data.split("_")[1])
    if method_num == 1:
        await safe_delete(call.message)
        #выставляем счет
        await call.message.answer_invoice(
            title="Премиум подписка 💎",
            description="Доступ к ИИ-учителю и расширенным тестам.",
            payload="premium_sub_card",
            provider_token=PAYMENT_TOKEN,
            currency="RUB",
            prices=[
                LabeledPrice(label="Тариф Премиум", amount=49900)
            ],
            start_parameter="premium-pay"
        )

    elif method_num == 2: #пока заглушка
        await call.message.edit_text(
            "Оплата через СБП временно на техническом обслуживании. Попробуйте оплату картой (Способ 1).",
            reply_markup=payment_method_kb())


@payment_router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    # Если всё ок, отвечаем True
    logging.info('Статус оплаты: ок')
    await pre_checkout_query.answer(ok=True)


@payment_router.message(F.successful_payment) #ловит системные сообщения об оплате
async def success_payment(message: Message):
    # Тут будет логика начисления тарифа в базу данных
    # await db.set_premium(message.from_user.id)

    data = message.successful_payment
    if data.invoice_payload == "premium_sub_card":
        pass
    await message.answer(
        "🎉 Поздравляем! Оплата прошла успешно.\nВаш тариф обновлен до «Премиум».",
        reply_markup=menu_kb())