import os
import sys
import traceback

# ========== ПЕРЕХВАТ ОШИБОК ДЛЯ ЛОГОВ ==========
try:
    print("🚀 Запуск бота...")
    
    import json
    import asyncio
    import threading
    from datetime import datetime
    from flask import Flask, request
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
    
    print("✅ Все модули успешно импортированы")
    
    # ========== КОНФИГУРАЦИЯ ==========
    TOKEN = "8539489977:AAFCgiAz7M9CH7yssMkdBo0BLH1310Tiuo0"
    print(f"✅ Токен загружен (длина: {len(TOKEN)} символов)")
    
    DATA_FILE = "races_data.json"
    
    # ========== ЗАГРУЗКА ДАННЫХ ==========
    def load_data():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        # Начальные данные (все забеги с 2022 по 25.04.2026)
        return [
            [2022, 7, 30, 49], [2022, 8, 6, 37], [2022, 8, 13, 40], [2022, 8, 20, 45],
            [2022, 8, 27, 78], [2022, 9, 3, 50], [2022, 9, 10, 41], [2022, 9, 17, 31],
            [2022, 9, 24, 10], [2022, 10, 1, 33], [2022, 10, 8, 43], [2022, 10, 15, 34],
            [2022, 10, 22, 54], [2022, 10, 29, 56], [2022, 11, 5, 38], [2022, 11, 12, 57],
            [2022, 11, 19, 30], [2022, 11, 26, 29], [2022, 12, 3, 20], [2022, 12, 10, 26],
            [2022, 12, 17, 19], [2022, 12, 24, 13], [2022, 12, 31, 16],
            [2023, 1, 7, 11], [2023, 1, 14, 37], [2023, 1, 21, 26], [2023, 1, 28, 18],
            [2023, 2, 4, 16], [2023, 2, 11, 21], [2023, 2, 18, 25], [2023, 2, 25, 25],
            [2023, 3, 4, 49], [2023, 3, 11, 37], [2023, 3, 18, 36], [2023, 3, 25, 47],
            [2023, 4, 1, 32], [2023, 4, 8, 51], [2023, 4, 15, 42], [2023, 4, 22, 42],
            [2023, 4, 29, 23], [2023, 5, 6, 40], [2023, 5, 13, 52], [2023, 5, 20, 32],
            [2023, 5, 27, 82], [2023, 6, 3, 27], [2023, 6, 10, 44], [2023, 6, 17, 47],
            [2023, 6, 24, 47], [2023, 7, 1, 44], [2023, 7, 8, 39], [2023, 7, 15, 32],
            [2023, 7, 22, 42], [2023, 7, 29, 29], [2023, 8, 5, 34], [2023, 8, 12, 42],
            [2023, 8, 19, 45], [2023, 8, 26, 95], [2023, 9, 2, 49], [2023, 9, 9, 46],
            [2023, 9, 16, 57], [2023, 9, 23, 56], [2023, 9, 30, 54], [2023, 10, 7, 23],
            [2023, 10, 14, 33], [2023, 10, 21, 40], [2023, 10, 28, 43], [2023, 11, 4, 46],
            [2023, 11, 11, 39], [2023, 11, 18, 30], [2023, 11, 25, 20], [2023, 12, 2, 27],
            [2023, 12, 9, 13], [2023, 12, 16, 22], [2023, 12, 23, 29], [2023, 12, 30, 21],
            [2024, 1, 1, 14], [2024, 1, 6, 17], [2024, 1, 13, 22], [2024, 1, 20, 36],
            [2024, 1, 27, 27], [2024, 2, 3, 21], [2024, 2, 10, 13], [2024, 2, 17, 29],
            [2024, 2, 24, 16], [2024, 3, 2, 31], [2024, 3, 9, 43], [2024, 3, 16, 41],
            [2024, 3, 30, 41], [2024, 4, 6, 30], [2024, 4, 13, 36], [2024, 4, 20, 52],
            [2024, 4, 27, 22], [2024, 5, 4, 32], [2024, 5, 11, 20], [2024, 5, 18, 43],
            [2024, 5, 25, 38], [2024, 6, 1, 55], [2024, 6, 8, 51], [2024, 6, 15, 35],
            [2024, 6, 22, 50], [2024, 6, 29, 34], [2024, 7, 6, 34], [2024, 7, 13, 22],
            [2024, 7, 20, 35], [2024, 7, 27, 23], [2024, 8, 3, 17], [2024, 8, 10, 27],
            [2024, 8, 17, 39], [2024, 8, 24, 46], [2024, 8, 31, 98], [2024, 9, 7, 57],
            [2024, 9, 14, 48], [2024, 9, 21, 43], [2024, 9, 28, 22], [2024, 10, 5, 24],
            [2024, 10, 12, 21], [2024, 10, 19, 32], [2024, 10, 26, 40], [2024, 11, 2, 23],
            [2024, 11, 9, 43], [2024, 11, 16, 40], [2024, 11, 23, 21], [2024, 11, 30, 27],
            [2024, 12, 7, 42], [2024, 12, 14, 43], [2024, 12, 21, 36], [2024, 12, 28, 26],
            [2025, 1, 1, 32], [2025, 1, 4, 23], [2025, 1, 11, 37], [2025, 1, 18, 41],
            [2025, 1, 25, 32], [2025, 2, 1, 42], [2025, 2, 8, 29], [2025, 2, 15, 28],
            [2025, 2, 22, 30], [2025, 3, 1, 24], [2025, 3, 8, 47], [2025, 3, 15, 83],
            [2025, 3, 22, 30], [2025, 3, 29, 40], [2025, 4, 5, 44], [2025, 4, 12, 32],
            [2025, 4, 19, 45], [2025, 4, 26, 41], [2025, 5, 3, 29], [2025, 5, 10, 30],
            [2025, 5, 17, 40], [2025, 5, 24, 39], [2025, 5, 31, 56], [2025, 6, 7, 70],
            [2025, 6, 14, 24], [2025, 6, 21, 35], [2025, 6, 28, 43], [2025, 7, 5, 31],
            [2025, 7, 12, 27], [2025, 7, 19, 39], [2025, 7, 26, 38], [2025, 8, 2, 26],
            [2025, 8, 9, 43], [2025, 8, 16, 23], [2025, 8, 23, 21], [2025, 8, 30, 77],
            [2025, 9, 6, 33], [2025, 9, 13, 39], [2025, 9, 20, 23], [2025, 9, 27, 45],
            [2025, 10, 4, 49], [2025, 10, 11, 40], [2025, 10, 18, 33], [2025, 10, 25, 39],
            [2025, 11, 1, 20], [2025, 11, 8, 45], [2025, 11, 15, 39], [2025, 11, 22, 39],
            [2025, 11, 29, 57], [2025, 12, 6, 57], [2025, 12, 13, 37], [2025, 12, 20, 46],
            [2025, 12, 27, 61], [2026, 1, 3, 37], [2026, 1, 10, 41], [2026, 1, 17, 49],
            [2026, 1, 24, 21], [2026, 1, 31, 26], [2026, 2, 7, 19], [2026, 2, 14, 21],
            [2026, 2, 21, 32], [2026, 2, 28, 43], [2026, 3, 7, 40], [2026, 3, 14, 60],
            [2026, 3, 21, 43], [2026, 3, 28, 44], [2026, 4, 4, 43], [2026, 4, 11, 31],
            [2026, 4, 18, 42], [2026, 4, 25, 38]
        ]
    
    def save_data(data):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    raw_data = load_data()
    print(f"✅ Загружено {len(raw_data)} записей о забегах")
    
    # ========== ПОСТРОЕНИЕ ТАБЛИЦЫ ==========
    def build_table():
        rows = []
        current_year = None
        year_sum = 0
        prev_count = None
        
        for year, month, day, count in sorted(raw_data, key=lambda x: (x[0], x[1], x[2])):
            date_str = f"{day:02d}.{month:02d}.{year}"
            if year != current_year:
                current_year = year
                year_sum = 0
                prev_count = None
            
            if prev_count is None:
                diff = "-"
            else:
                diff = count - prev_count
            
            year_sum += count
            sum_x5 = year_sum * 5
            rows.append([date_str, count, diff, sum_x5, sum_x5])
            prev_count = count
        
        return rows
    
    def format_table(rows, year_filter=None):
        lines = ["<pre>"]
        header = f"{'Дата':<12} {'Участ':<6} {'Приб':<6} {'Сумма×5':<8} {'Дубль×5':<8}"
        lines.append(header)
        lines.append("-" * len(header))
        
        for row in rows:
            date_str, count, diff, sum1, sum2 = row
            year = int(date_str.split('.')[-1])
            if year_filter and year != year_filter:
                continue
            diff_str = f"{diff:+d}" if isinstance(diff, int) else diff
            lines.append(f"{date_str:<12} {count:<6} {diff_str:<6} {sum1:<8} {sum2:<8}")
        
        lines.append("</pre>")
        text = "\n".join(lines)
        if len(text) > 4000:
            text = text[:3900] + "\n... (обрезано)</pre>"
        return text
    
    # ========== ИНИЦИАЛИЗАЦИЯ БОТА ==========
    app_bot = None
    flask_app = Flask(__name__)
    
    async def start(update: Update, context):
        keyboard = [
            [InlineKeyboardButton("📊 Вся таблица", callback_data="show_all")],
            [InlineKeyboardButton("📅 За год", callback_data="show_year")],
            [InlineKeyboardButton("➕ Добавить забег", callback_data="add_run")],
        ]
        await update.message.reply_text(
            "🏃 Забеги в Царицыно\nДанные с 2022 года\n\n"
            "📌 В столбце 'Сумма×5' и 'Дубль×5' — количество участников, умноженное на 5",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def button_handler(update: Update, context):
        query = update.callback_query
        await query.answer()
        if query.data == "show_all":
            await query.edit_message_text(format_table(build_table()), parse_mode="HTML")
        elif query.data == "show_year":
            years = sorted(set(row[0].split('.')[-1] for row in build_table()))
            keyboard = [[InlineKeyboardButton(str(y), callback_data=f"year_{y}")] for y in years]
            await query.edit_message_text("Выберите год:", reply_markup=InlineKeyboardMarkup(keyboard))
        elif query.data.startswith("year_"):
            year = int(query.data.split("_")[1])
            await query.edit_message_text(format_table(build_table(), year_filter=year), parse_mode="HTML")
        elif query.data == "add_run":
            await query.edit_message_text("Используйте команду /add для добавления записи")
    
    # Добавление записи
    YEAR, MONTH, DAY, COUNT_STATE = range(4)
    
    async def add_start(update: Update, context):
        await update.message.reply_text("Введите **год** (например: 2026):")
        return YEAR
    
    async def add_year(update: Update, context):
        context.user_data['year'] = int(update.message.text)
        await update.message.reply_text("Введите **месяц** (число от 1 до 12):")
        return MONTH
    
    async def add_month(update: Update, context):
        context.user_data['month'] = int(update.message.text)
        await update.message.reply_text("Введите **день** (суббота):")
        return DAY
    
    async def add_day(update: Update, context):
        context.user_data['day'] = int(update.message.text)
        await update.message.reply_text("Введите **количество участников**:")
        return COUNT_STATE
    
    async def add_count(update: Update, context):
        year = context.user_data['year']
        month = context.user_data['month']
        day = context.user_data['day']
        count = int(update.message.text)
        raw_data.append([year, month, day, count])
        raw_data.sort(key=lambda x: (x[0], x[1], x[2]))
        save_data(raw_data)
        await update.message.reply_text(f"✅ Добавлено: {day:02d}.{month:02d}.{year} — {count} участников")
        return ConversationHandler.END
    
    async def cancel(update: Update, context):
        await update.message.reply_text("❌ Добавление отменено")
        return ConversationHandler.END
    
    # Flask вебхуки
    @flask_app.route(f'/{TOKEN}', methods=['POST'])
    async def webhook():
        update = Update.de_json(request.get_json(force=True), app_bot.bot)
        await app_bot.process_update(update)
        return 'ok'
    
    @flask_app.route('/')
    def home():
        return "Бот для учёта забегов в Царицыно работает! 🏃"
    
    def setup_webhook():
        render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if render_hostname:
            webhook_url = f"https://{render_hostname}/{TOKEN}"
            print(f"🔗 Установка вебхука: {webhook_url}")
            app_bot.bot.set_webhook(webhook_url)
        else:
            print("⚠️ RENDER_EXTERNAL_HOSTNAME не найден, вебхук не установлен")
    
    def main():
        global app_bot
        print("🔄 Создание приложения...")
        app_bot = Application.builder().token(TOKEN).build()
        
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CallbackQueryHandler(button_handler))
        
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("add", add_start)],
            states={
                YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_year)],
                MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_month)],
                DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_day)],
                COUNT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_count)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        app_bot.add_handler(conv_handler)
        
        # Запуск Flask в отдельном потоке
        port = int(os.environ.get('PORT', 8080))
        print(f"🚀 Запуск Flask на порту {port}")
        threading.Thread(target=lambda: flask_app.run(host='0.0.0.0', port=port, debug=False)).start()
        
        # Установка вебхука
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(setup_webhook())
            loop.close()
        except Exception as e:
            print(f"⚠️ Ошибка при установке вебхука: {e}")
            print("Бот продолжает работу...")
        
        print("✅ Бот успешно запущен и готов к работе!")
    
    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
    print("❌ ПОДРОБНОСТИ:")
    traceback.print_exc()
    sys.exit(1)
