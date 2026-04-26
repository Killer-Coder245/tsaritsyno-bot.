import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TOKEN = "8539489977:AAFw0hVYMS5V_1NtfDIJBIKpvDPmtEnpfoA"

# Данные о забегах (первые несколько для теста)
DATA = [
    ["25.04.2026", 38, "-", 190, 190],
    ["18.04.2026", 42, "+4", 400, 400],
    ["11.04.2026", 31, "-11", 555, 555],
]

def format_table():
    lines = ["<pre>"]
    lines.append(f"{'Дата':<12} {'Участ':<6} {'Приб':<6} {'Сумма×5':<8} {'Дубль×5':<8}")
    lines.append("-" * 50)
    for row in DATA:
        lines.append(f"{row[0]:<12} {row[1]:<6} {row[2]:<6} {row[3]:<8} {row[4]:<8}")
    lines.append("</pre>")
    return "\n".join(lines)

async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("📊 Показать таблицу", callback_data="table")]]
    await update.message.reply_text("🏃 Бот забегов Царицыно", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(format_table(), parse_mode="HTML")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
