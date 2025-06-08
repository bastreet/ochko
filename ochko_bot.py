from telegram import Update, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "7566902664:AAEp6CNE8lEpSTZ6mThIJdqMCuIauThDXRk"  # Получите у @BotFather
GAME_URL = "https://bastreet.github.io/ochko/"  # URL вашей игры на GitHub Pages

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в очко!",
        reply_markup={
            "inline_keyboard": [[
                {
                    "text": "Начать игру", 
                    "web_app": WebAppInfo(url=GAME_URL)
                }
            ]]
        }
    )

# Обработчик данных из игры
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Парсим данные из игры
        data = json.loads(update.effective_message.web_app_data.data)
        score = data.get("score", 0)
        
        # Отправляем результат
        await update.message.reply_text(
            f"🏆 Ваш результат: {score} очков!",
            reply_markup={
                "inline_keyboard": [[
                    {
                        "text": "Играть ещё раз", 
                        "web_app": WebAppInfo(url=GAME_URL)
                    }
                ]]
            }
        )
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        await update.message.reply_text("⚠️ Не удалось получить результаты игры")

# Настройка и запуск бота
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    
    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()
