from aiogram import Dispatcher, Bot, filters, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

balance = 300
orders = {}

bot = Bot(token="7283256121:AAGyDvUF2dyJeoEAIyaK0Kda1kFrSQG1-Gw")
dp = Dispatcher(bot=bot)


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    number = State()


contact_button = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Komntakt jo'natish", request_contact=True)]
], resize_keyboard=True)


worthButton = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="About me"), KeyboardButton(text="Food")],
    [KeyboardButton(text="Balance"), KeyboardButton(text="Orders")]
], resize_keyboard=True)


full = [
    [InlineKeyboardButton(text="Fill balance", callback_data="fillBal"), InlineKeyboardButton(text="Back", callback_data="back")]
]
full_balance = InlineKeyboardMarkup(inline_keyboard=full)


# =================================================================================

keyboards = [
    [KeyboardButton(text="About KFC"), KeyboardButton(text="Branches")],
    [KeyboardButton(text="Menu"), KeyboardButton(text="Back")]
]

main_button = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)

# ---------------------------------------------------------------------------

multipleChoice = [
    [KeyboardButton(text="Drinks"), KeyboardButton(text="Eats")],
    [KeyboardButton(text="Back")]
]

toEat = ReplyKeyboardMarkup(keyboard=multipleChoice, resize_keyboard=True)


multipleChoice2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Buy", callback_data="buyIt"), InlineKeyboardButton(text="Basket", callback_data="basket")],
    [InlineKeyboardButton(text="Back", callback_data="back")]

])
# ---------------------------------------------------------------------------

menus = [
    [KeyboardButton(text="Doner"), KeyboardButton(text="French fries")],
    [KeyboardButton(text="Back")]

]

main2_button = ReplyKeyboardMarkup(keyboard=menus, resize_keyboard=True)

# ---------------------------------------------------------------------------

menus2 = [
    [KeyboardButton(text="Cola"), KeyboardButton(text="Water")],
    [KeyboardButton(text="Back")]
]

order = ReplyKeyboardMarkup(keyboard=menus2, resize_keyboard=True)

# --------------------------------------------------------------------------





# --------------------------------------------------------------------------

aboutUser = [
    [KeyboardButton(text="Username"), KeyboardButton(text="ID"), KeyboardButton(text="Full name")],
    [KeyboardButton(text="Back")]

]

UserButton = ReplyKeyboardMarkup(keyboard=aboutUser, resize_keyboard=True)

orders_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"Buy All"), KeyboardButton(text="Delete All")],
    [KeyboardButton(text="Back")]
], resize_keyboard=True)

# ---------------------------------------------------------------------------

@dp.message(filters.Command("start"))
async def start(message: types.Message):
    await message.answer("Welcome to KFC!", reply_markup=worthButton)


@dp.message(filters.Command("register"))
async def register(message: types.Message, state: FSMContext):
    await state.set_state(Registration.first_name)
    await message.answer("Ism: ")

@dp.message(Registration.first_name)
async def first_name_function(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(Registration.last_name)
    await message.answer("Familya: ")

@dp.message(Registration.last_name)
async def last_name_function(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Registration.number)
    await message.answer("Number: ", reply_markup=contact_button)


# ===========================================================================

@dp.message(F.text == "Orders")
async def all_orders(message: types.Message):
    global orders
    await message.answer(f"All orders; {orders}", reply_markup=orders_button)

@dp.message(F.text == "Buy All")
async def buyAll(message: types.Message):
    global orders, balance
    total = sum(orders.values())
    await message.answer(f"Buy all (balance; ${balance - total})", reply_markup=worthButton)

@dp.message(F.text == "Delete All")
async def delAll(message: types.Message):
    global orders
    clean = orders.clear()
    await message.answer(f"Delete all", reply_markup=worthButton)



@dp.message(F.text == "Food")
async def link(message: types.Message):
    await message.answer("Choose", reply_markup=main_button)

# ===========================================================================

@dp.message(F.text == "About me")
async def about(message: types.Message):
    await message.answer("About User", reply_markup=UserButton)

@dp.message(F.text == "Full name")
async def full(message: types.Message):
    await message.answer(f"Full name: {message.from_user.full_name}")

@dp.message(F.text == "Username")
async def User(message: types.Message):
    await message.answer(f"Username: {message.from_user.username}")

@dp.message(F.text == "ID")
async def ID(message: types.Message):
    await message.answer(f"ID: {message.from_user.id}", )

# ===========================================================================

@dp.message(F.text == "Menu")
async def menu(message: types.Message):
    await message.answer_photo(photo="https://i.pinimg.com/736x/a1/d7/c9/a1d7c93465ef28ee0dd99e7d6e88494f.jpg", caption="To drink or to eat?", reply_markup=toEat)

@dp.message(F.text == "Eats")
async def Eats(message: types.Message):
    await message.answer("🥙 Doner: 4$ \n🍟 french fries: 1$", reply_markup=main2_button)

@dp.message(F.text == "Doner")
async def don_desc(message: types.Message):
    global balance
    await message.answer_photo(photo="https://e7.pngegg.com/pngimages/903/548/png-clipart-kebab-kebab.png",
                               caption=f"Your balance; ${balance}", reply_markup=multipleChoice2)

    @dp.callback_query(F.data == "buyIt")
    async def buy1(callback: types.CallbackQuery):
        global balance
        balance -= 1
        await callback.message.answer(f"Your balance; {balance}", reply_markup=worthButton)

    @dp.callback_query(F.data == "basket")
    async def basket1(callback: types.CallbackQuery):
        orders.update({"Doner": 4})
        await callback.message.answer(f"Doner added to basket", reply_markup=worthButton)


@dp.message(F.text == "French fries")
async def fre_desc(message: types.Message):
    global balance
    await message.answer_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaNPqFfVmpJPQDRWh6HVUtfEMF7A0h-ZmcE50q7sAqBtz0E8GXYw&s",
                               caption=f"Your balance; ${balance}", reply_markup=multipleChoice2)

    @dp.callback_query(F.data == "buyIt")
    async def buy2(callback: types.CallbackQuery):
        global balance
        balance -= 1
        await callback.message.answer(f"Your balance; {balance}", reply_markup=worthButton)

    @dp.callback_query(F.data == "basket")
    async def basket2(callback: types.CallbackQuery):
        orders.update({"French fries": 1})
        await callback.message.answer(f"French fries added to basket", reply_markup=worthButton)
# ===========================================================================

@dp.message(F.text == "Drinks")
async def drinks(message: types.Message):
    await message.answer("🥤 Cola: 1$\n💧 water: 0.4$", reply_markup=order)

@dp.message(F.text == "Cola")
async def col_desc(message: types.Message):
    global balance
    await message.answer_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRvB90tV7MnV6esEKZ2tLFzs8kEfbwmrUwJDQ&s",
                               caption=f"Your balance; ${balance}", reply_markup=multipleChoice2)
    @dp.callback_query(F.data == "buyIt")
    async def buy(callback: types.CallbackQuery):
        global balance
        balance -= 1
        await callback.message.answer(f"Your balance; {balance}", reply_markup=worthButton)

    @dp.callback_query(F.data == "basket")
    async def basket(callback: types.CallbackQuery):
        orders.update({"Cola": 1})
        await callback.message.answer(f"Cola added to basket", reply_markup=worthButton)

@dp.message(F.text == "Water")
async def wat_desc(message: types.Message):
    global balance
    await message.answer_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSaNPqFfVmpJPQDRWh6HVUtfEMF7A0h-ZmcE50q7sAqBtz0E8GXYw&s",
                               caption=f"Your balance; ${balance}", reply_markup=multipleChoice2)
    @dp.callback_query(F.data == "buyIt")
    async def buy(callback: types.CallbackQuery):
        global balance
        balance -= 0.4
        await callback.message.answer(f"Your balance; {balance}", reply_markup=worthButton)

    @dp.callback_query(F.data == "basket")
    async def basket(callback: types.CallbackQuery):
        orders.update({"water": 0.4})
        await callback.message.answer(f"Water added to basket", reply_markup=worthButton)
# ===========================================================================

@dp.message(F.text == "Branches")
async def branc(message: types.Message):
    await message.answer("KFC chilonzor\nKFC chopon ota\nKFC Magic city")

@dp.message(F.text == "Back")
async def back(message: types.Message):
    await message.answer("Back", reply_markup=worthButton)

@dp.callback_query(F.data == "You completed payment")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer(
        text="you payed",
        show_alert=True

    )

@dp.message(F.text == "Balance")
async def balans(message: types.Message):
    global balance

    await message.answer(f"Your balance; ${balance}", reply_markup=full_balance)



@dp.callback_query(F.data == "fillBal")
async def Value(callback: types.CallbackQuery):
    global balance
    await callback.message.answer(f"Balance filled to {balance}")

@dp.callback_query(F.data == "back")
async def ret(callback: types.CallbackQuery):
    await callback.message.answer(f"Returning to main page", reply_markup=worthButton)
# ===========================================================================

@dp.message(F.text == "About KFC")
async def branc(message: types.Message):
    await message.answer_photo(photo="https://www.freepnglogos.com/uploads/kfc-png-logo/camera-kfc-png-logo-0.png" ,
                               caption="KFC is a global chicken restaurant brand with a rich, decades-long history of success and innovation. It all started with one cook, Colonel Harland Sanders, who created a finger lickin' good recipe more than 75 years ago—a list of 11 secret herbs and spices scratched out on the back of his kitchen door.")

# ============================================================================

@dp.message(F.text == "By card")
async def card(message: types.Message):
    await message.answer("You payed by card", reply_markup=main_button)

@dp.message(F.text == "By Cash")
async def card(message: types.Message):
    await message.answer("You payed by cash", reply_markup=main_button)

# ============================================================================


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())