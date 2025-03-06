import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters, CallbackQueryHandler, ConversationHandler, CallbackContext
)

from src.adapters.controllers.telegram_controller import TelegramController


class TelegramBot:

    def __init__(self, telegram_token: str, controller: TelegramController):
        self.token = telegram_token
        self.controller = controller
        self.logger = logging.getLogger(__name__)
    
    def start(self, update: Update, context: CallbackContext) -> None:
        keyboard = [
            [InlineKeyboardButton("Previsão Comum", callback_data='previsao_comum')],
            [InlineKeyboardButton("Previsão Estendida", callback_data='previsao_estendida')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Escolha o tipo de previsão:', reply_markup=reply_markup)
    
    def help_command(self, update: Update, context: CallbackContext) -> None:
        mensagem_ajuda = """
Aqui estão os comandos disponíveis e como usá-los:
/start - Inicia o bot e exibe opções para previsão comum ou estendida.
/previsao - Obtém a previsão do tempo para a sua localização. Uso: /previsao <nome_da_cidade>
/previsao_estendida - Obtém a previsão do tempo estendida para a sua localização. Uso: /previsao_estendida <nome_da_cidade>
/ajuda - Mostra esta mensagem de ajuda.

Você também pode compartilhar sua localização diretamente com o bot para receber a previsão do tempo.
"""
        update.message.reply_text(mensagem_ajuda)

    def button_callback(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        context.user_data['forecast_type'] = query.data

        query.edit_message_text(text="Por favor, compartilhe sua localização ou digite o nome de uma cidade.")

    def handle_location(self, update: Update, context: CallbackContext) -> None:
        user_location = update.message.location
        forecast_type = context.user_data.get('forecast_type', 'previsao_comum')
        
        if forecast_type == 'previsao_comum':
            response = self.controller.get_current_forecast_by_location(
                user_location.latitude, user_location.longitude
            )
        else:
            response = self.controller.get_extended_forecast_by_location(
                user_location.latitude, user_location.longitude
            )
        
        update.message.reply_text(response)
    
    def current_forecast(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            update.message.reply_text("Por favor, forneça o nome da cidade. Exemplo: /previsao Londres")
            return
        
        city_name = ' '.join(context.args)
        response = self.controller.get_current_forecast_by_city(city_name)
        update.message.reply_text(response)
    
    def extended_forecast(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            update.message.reply_text("Por favor, forneça o nome da cidade. Exemplo: /previsao_estendida Londres")
            return
        
        city_name = ' '.join(context.args)
        response = self.controller.get_extended_forecast_by_city(city_name)
        update.message.reply_text(response)
    
    def error_handler(self, update: Update, context: CallbackContext) -> None:
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)
    
    def run(self) -> None:
        updater = Updater(self.token, use_context=True)
        dp = updater.dispatcher
        
        # Register handlers
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("ajuda", self.help_command))
        dp.add_handler(CommandHandler("previsao", self.current_forecast, pass_args=True))
        dp.add_handler(CommandHandler("previsao_estendida", self.extended_forecast, pass_args=True))
        dp.add_handler(CallbackQueryHandler(self.button_callback))
        dp.add_handler(MessageHandler(Filters.location, self.handle_location))
        
        dp.add_error_handler(self.error_handler)
        
        self.logger.info("Starting bot...")
        updater.start_polling()
        updater.idle()