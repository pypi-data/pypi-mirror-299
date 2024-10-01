# spider_ai

SpiderAI هي مكتبة تسمح للمستخدمين بإجراء استفسارات والحصول على إجابات باستخدام القدرات الذكية لـ OpenAI.

## البدء

قبل أن تستطيع استخدام SpiderAI، يجب عليك الحصول على مفتاح API من OpenAI.

### المتطلبات

- Python 3
- حساب OpenAI (للحصول على مفتاح API)

### التنصيب

يمكنك تنصيب SpiderAI باستخدام pip:


pip install spider_ai

## استخدام SpiderAI

### الاستخدام العام

للبدء باستخدام SpiderAI للحصول على إجابات لاستفساراتك، اتبع الكود التالي:
مثال 

python
from spider_ai import SpiderAI

openaiapikey = "YOUROPENAIAPI_KEY"

ai = SpiderAI(openaiapikey)

user_query = input("Please enter your question: ")

response = ai.query(user_query)

print("Response:", response)

### استخدام SpiderAI في بوتات Telegram

لتمكين بوت Telegram من استخدام SpiderAI، يمكنك استخدام الكود التالي:

python
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from spider_ai import SpiderAIBot

openaiapikey = "YOUROPENAIAPI_KEY"
telegrambottoken = "YOURTELEGRAMBOT_TOKEN"

aibot = SpiderAIBot(openaiapi_key)

def ask_question(update, context):
    user_input = update.message.text.split('/ask ',1)[1]
    
    response = aibot.generateresponse(user_input)
    
    update.message.reply_text(response)

def start(update, context):
    update.message.reply_text("Welcome! Send /ask followed by your question.")

def main():
    updater = Updater(telegrambottoken, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.addhandler(MessageHandler(Filters.command & Filters.regex('^/ask '), askquestion))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()

## مساهمة

نرحب بكل مساهماتكم! سواء كانت عبارة عن تقديم ميزات جديدة، تحسينات، أو إصلاح الأخطاء.

## الدعم
spiderXR