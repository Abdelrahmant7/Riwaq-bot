import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.exceptions import TelegramBadRequest

# ================= ضع بياناتك هنا =================
BOT_TOKEN = "8997076890:AAEbEC4Dn5iMYt0DLX9p76Hn0pnZCtA5c0o"  # التوكن بتاعك اللي ظهر في الصورة
CHANNEL_USERNAME = "@YourChannelUsername"  # يوزر قناتك مع علامة @ (مثلا @my_channel)
# ==================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# فحص اشتراك المستخدم في القناة
async def check_user_sub(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest:
        return False

# زر الاشتراك الإجباري
def get_sub_keyboard():
    channel_clean = CHANNEL_USERNAME.replace("@", "")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 اشترك في القناة أولاً", url=f"https://t.me/{channel_clean}")],
            [InlineKeyboardButton(text="✅ تحقّق من الاشتراك", callback_data="check_sub")]
        ]
    )

# القائمة الرئيسية للأقسام
def get_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 كتب علم النفس", callback_data="menu_psy")],
            [InlineKeyboardButton(text="📜 كتب التاريخ", callback_data="menu_hist")],
            [InlineKeyboardButton(text="📖 روايات وأدب", callback_data="menu_novels")]
        ]
    )

# أزرار قسم علم النفس
def get_psy_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📗 الإنسان والبحث عن المعنى", url="https://t.me/YourChannelUsername/10")],
            [InlineKeyboardButton(text="🔙 رجوع للأقسام", callback_data="back_home")]
        ]
    )

# أزرار قسم التاريخ
def get_hist_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📕 مقدمة ابن خلدون", url="https://t.me/YourChannelUsername/20")],
            [InlineKeyboardButton(text="🔙 رجوع للأقسام", callback_data="back_home")]
        ]
    )

# أزرار قسم الروايات
def get_novels_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📘 رواية أرض زيكولا", url="https://t.me/YourChannelUsername/30")],
            [InlineKeyboardButton(text="🔙 رجوع للأقسام", callback_data="back_home")]
        ]
    )

# أمر البدء /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    if await check_user_sub(message.from_user.id):
        await message.answer(
            f"أهلاً بك يا {message.from_user.first_name} في رواق الكتب 📚\nاختر القسم الذي تريده:",
            reply_markup=get_main_menu()
        )
    else:
        await message.answer(
            "⚠️ عذراً، يجب عليك الاشتراك في القناة أولاً لتفعيل البوت واستخدام المكتبة:",
            reply_markup=get_sub_keyboard()
        )

# زر التحقق بعد الاشتراك
@dp.callback_query(F.data == "check_sub")
async def verify_sub(callback: CallbackQuery):
    if await check_user_sub(callback.from_user.id):
        await callback.message.edit_text(
            "تم التحقق بنجاح! أهلاً بك في رواق الكتب 📚\nاختر القسم المطلوب:",
            reply_markup=get_main_menu()
        )
    else:
        await callback.answer("❌ أنت لم تشترك في القناة بعد! اضغط على زر القناة واشترك ثم أعد المحاولة.", show_alert=True)

# فتح الأقسام
@dp.callback_query(F.data == "menu_psy")
async def show_psy(callback: CallbackQuery):
    await callback.message.edit_text("🧠 **قسم كتب علم النفس:**\nاختر الكتاب:", reply_markup=get_psy_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "menu_hist")
async def show_hist(callback: CallbackQuery):
    await callback.message.edit_text("📜 **قسم كتب التاريخ:**\nاختر الكتاب:", reply_markup=get_hist_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "menu_novels")
async def show_novels(callback: CallbackQuery):
    await callback.message.edit_text("📖 **قسم الروايات:**\nاختر الرواية:", reply_markup=get_novels_menu(), parse_mode="Markdown")

@dp.callback_query(F.data == "back_home")
async def back_home(callback: CallbackQuery):
    await callback.message.edit_text("📚 الأقسام الرئيسية للمكتبة:", reply_markup=get_main_menu())

async def main():
    print("البوت يعمل الآن بنجاح!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())