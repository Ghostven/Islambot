import telebot
from telebot import types
import threading
import schedule
import time

# التوكن الخاص بالبوت
TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# لتخزين المستخدمين المفعلين
subscribed_users = set()

# أذكار الصباح
morning_azkar = """
*أذكار الصباح:*
- أصبحنا وأصبح الملك لله.
- اللهم بك أصبحنا وبك أمسينا وبك نحيا وبك نموت وإليك النشور.
- رضيت بالله ربا وبالإسلام دينا وبمحمد صلى الله عليه وسلم نبيا.
- اللهم ما أصبح بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر.
"""

# أذكار المساء
evening_azkar = """
*أذكار المساء:*
- أمسينا وأمسى الملك لله.
- اللهم بك أمسينا وبك أصبحنا وبك نحيا وبك نموت وإليك المصير.
- رضيت بالله ربا وبالإسلام دينا وبمحمد صلى الله عليه وسلم نبيا.
- اللهم ما أمسى بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر.
"""

# إنشاء الأزرار الرئيسية
def create_main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton("تفعيل اذكار الصباح و المساء 🕊️"),
        types.KeyboardButton("ادعية نبوية 📜")
    )
    markup.row(
        types.KeyboardButton("تفعيل اذكار يومية 🔄"),
        types.KeyboardButton("مطور البوت 👨‍💻")
    )
    markup.row(types.KeyboardButton("مساعدة ❓"))
    return markup

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "مرحبًا! اختر أحد الخيارات أدناه:",
        reply_markup=create_main_buttons()
    )

# تفعيل/تعطيل الاشتراك بالتذكير
@bot.message_handler(func=lambda m: m.text == "تفعيل اذكار الصباح و المساء 🕊️")
def toggle_subscription(message):
    if message.chat.id in subscribed_users:
        subscribed_users.remove(message.chat.id)
        bot.send_message(
            message.chat.id,
            "❌ تم تعطيل التذكير بأذكار الصباح والمساء.",
            reply_markup=create_main_buttons()
        )
    else:
        subscribed_users.add(message.chat.id)
        bot.send_message(
            message.chat.id,
            "✅ تم تفعيل التذكير بأذكار الصباح والمساء.",
            reply_markup=create_main_buttons()
        )

# ادعية نبوية
@bot.message_handler(func=lambda m: m.text == "ادعية نبوية 📜")
def noble_duas(message):
    duas = (
        "1. اللهم اجعلنا من أهل الجنة 🏰\n"
        "2. اللهم إني أسالك الجنة وما قرب إليها من قول أو عمل 🙏\n"
        "3. اللهم ثبتنا على دينك 💪\n"
        "4. اللهم اجعلنا من الذين يستمعون القول فيتبعون أحسنه 🌟\n"
        "5. اللهم ارزقنا العلم النافع والعمل الصالح 🌱"
    )
    bot.send_message(message.chat.id, duas, reply_markup=create_main_buttons())

# تفعيل اذكار يومية (غير مربوط حاليًا)
@bot.message_handler(func=lambda m: m.text == "تفعيل اذكار يومية 🔄")
def toggle_daily(message):
    bot.send_message(
        message.chat.id,
        "الميزة غير مفعّلة حاليًا. سيتم إضافتها لاحقًا.",
        reply_markup=create_main_buttons()
    )

# مطور البوت
@bot.message_handler(func=lambda m: m.text == "مطور البوت 👨‍💻")
def show_dev(message):
    bot.send_message(message.chat.id, "~> The admin @a_4pa 🧑‍💻", reply_markup=create_main_buttons())

# مساعدة
@bot.message_handler(func=lambda m: m.text == "مساعدة ❓")
def help_message(message):
    text = (
        "اضغط على:\n"
        "- *تفعيل اذكار الصباح و المساء* لتصلك الأذكار يوميًا.\n"
        "- *ادعية نبوية* لعرض مجموعة من الأدعية.\n"
        "- *مطور البوت* لعرض المطور."
    )
    bot.send_message(message.chat.id, text, reply_markup=create_main_buttons())

# مهمة إرسال أذكار الصباح
def send_morning_azkar():
    for user_id in subscribed_users:
        try:
            bot.send_message(user_id, morning_azkar, parse_mode="Markdown")
        except:
            continue

# مهمة إرسال أذكار المساء
def send_evening_azkar():
    for user_id in subscribed_users:
        try:
            bot.send_message(user_id, evening_azkar, parse_mode="Markdown")
        except:
            continue

# جدولة المهام
schedule.every().day.at("07:00").do(send_morning_azkar)
schedule.every().day.at("13:00").do(send_evening_azkar)

# تنفيذ الجدولة في Thread منفصل
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(30)

threading.Thread(target=run_schedule, daemon=True).start()

# بدء البوت
bot.polling(none_stop=True)