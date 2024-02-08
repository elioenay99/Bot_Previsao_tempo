from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from functions import logger, handle_location, previsao, previsao_estendida
from Chaves import CHAVE_BOT_TELEGRAM as TELEGRAM_TOKEN


def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Previsão Comum", callback_data='previsao_comum')],
        [InlineKeyboardButton("Previsão Estendida", callback_data='previsao_estendida')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Escolha o tipo de previsão:', reply_markup=reply_markup)


def ajuda(update, context):
    mensagem_ajuda = """
Aqui estão os comandos disponíveis e como usá-los:
/start - Inicia o bot e exibe opções para previsão comum ou estendida.
/previsao - Obtém a previsão do tempo para a sua localização. Uso: /previsao <nome_da_cidade>
/previsao_estendida - Obtém a previsão do tempo estendida para a sua localização. Uso: /previsao_estendida <nome_da_cidade>
/ajuda - Mostra esta mensagem de ajuda.

Você também pode compartilhar sua localização diretamente com o bot para receber a previsão do tempo.
"""
    update.message.reply_text(mensagem_ajuda)


def button(update, context):
    query = update.callback_query
    query.answer()
    context.user_data['previsao_tipo'] = query.data
    query.edit_message_text(text="Por favor, compartilhe sua localização.")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.location, handle_location))
    dp.add_handler(CommandHandler("ajuda", ajuda))
    dp.add_handler(CommandHandler("previsao", previsao, pass_args=True))
    dp.add_handler(CommandHandler("previsao_estendida", previsao_estendida, pass_args=True))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
