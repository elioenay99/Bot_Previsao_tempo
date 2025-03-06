import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters, CallbackQueryHandler, ConversationHandler, CallbackContext, InlineQueryHandler
)

from src.adapters.controllers.telegram_controller import TelegramController
from uuid import uuid4


class TelegramBot:

    def __init__(self, telegram_token: str, controller: TelegramController):
        self.token = telegram_token
        self.controller = controller
        self.logger = logging.getLogger(__name__)
    
    def start(self, update: Update, context: CallbackContext) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Previsão Atual", callback_data='current_forecast'),
                InlineKeyboardButton("Próximos 5 Dias", callback_data='extended_forecast')
            ],
            [InlineKeyboardButton("Ajuda", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            'Olá! Sou o Bot de Previsão do Tempo. Como posso ajudar?',
            reply_markup=reply_markup
        )
    
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

        if query.data == 'help':
            mensagem_ajuda = """
Aqui estão os comandos disponíveis e como usá-los:

• Previsão Atual - Obtém a previsão do tempo atual para sua cidade
• Próximos 5 Dias - Obtém a previsão estendida para os próximos dias
• Ajuda - Mostra esta mensagem de ajuda

Você pode:
1. Clicar nos botões do menu
2. Compartilhar sua localização
3. Digite o nome de uma cidade após selecionar o tipo de previsão
"""
            keyboard = [
                [InlineKeyboardButton("Voltar ao Menu", callback_data='start')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=mensagem_ajuda, reply_markup=reply_markup)
            return

        if query.data == 'start':
            keyboard = [
                [
                    InlineKeyboardButton("Previsão Atual", callback_data='current_forecast'),
                    InlineKeyboardButton("Próximos 5 Dias", callback_data='extended_forecast')
                ],
                [InlineKeyboardButton("Ajuda", callback_data='help')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text='Olá! Sou o Bot de Previsão do Tempo. Como posso ajudar?',
                reply_markup=reply_markup
            )
            return

        context.user_data['forecast_type'] = query.data
        query.edit_message_text(
            text="Por favor, compartilhe sua localização ou digite o nome de uma cidade."
        )

    def handle_location(self, update: Update, context: CallbackContext) -> None:
        user_location = update.message.location
        forecast_type = context.user_data.get('forecast_type', 'current_forecast')
        
        if forecast_type == 'current_forecast':
            response = self.controller.get_current_forecast_by_location(
                user_location.latitude, user_location.longitude
            )
        elif forecast_type == 'extended_forecast':
            response = self.controller.get_extended_forecast_by_location(
                user_location.latitude, user_location.longitude
            )
        
        keyboard = [
            [InlineKeyboardButton("Voltar ao Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(response, reply_markup=reply_markup)
    
    def current_forecast(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            keyboard = [
                [
                    InlineKeyboardButton("Previsão Atual", callback_data='current_forecast'),
                    InlineKeyboardButton("Próximos 5 Dias", callback_data='extended_forecast')
                ],
                [InlineKeyboardButton("Ajuda", callback_data='help')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                "Por favor, forneça o nome da cidade. Exemplo: /previsao Londres",
                reply_markup=reply_markup
            )
            return
        
        city_name = ' '.join(context.args)
        response = self.controller.get_current_forecast_by_city(city_name)
        
        keyboard = [
            [InlineKeyboardButton("Voltar ao Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(response, reply_markup=reply_markup)
    
    def extended_forecast(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            keyboard = [
                [
                    InlineKeyboardButton("Previsão Atual", callback_data='current_forecast'),
                    InlineKeyboardButton("Próximos 5 Dias", callback_data='extended_forecast')
                ],
                [InlineKeyboardButton("Ajuda", callback_data='help')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(
                "Por favor, forneça o nome da cidade. Exemplo: /previsao_estendida Londres",
                reply_markup=reply_markup
            )
            return
        
        city_name = ' '.join(context.args)
        response = self.controller.get_extended_forecast_by_city(city_name)
        
        keyboard = [
            [InlineKeyboardButton("Voltar ao Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(response, reply_markup=reply_markup)
    
    def inline_query(self, update: Update, context: CallbackContext) -> None:
        query = update.inline_query.query
        if not query:
            return

        results = []
        try:
            # Resultado para previsão atual
            current_weather = self.controller.get_current_forecast_by_city(query)
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"Previsão Atual - {query}",
                    description="Mostrar previsão do tempo atual",
                    input_message_content=InputTextMessageContent(current_weather)
                )
            )

            # Resultado para previsão estendida
            extended_weather = self.controller.get_extended_forecast_by_city(query)
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"Previsão 5 Dias - {query}",
                    description="Mostrar previsão do tempo para 5 dias",
                    input_message_content=InputTextMessageContent(extended_weather)
                )
            )

        except Exception as e:
            self.logger.error(f"Erro na consulta inline: {str(e)}")
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="Erro",
                    description="Não foi possível obter a previsão do tempo",
                    input_message_content=InputTextMessageContent(
                        "Desculpe, não foi possível obter a previsão do tempo para esta cidade."
                    )
                )
            )

        update.inline_query.answer(results, cache_time=300)

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
        dp.add_handler(InlineQueryHandler(self.inline_query))
        
        dp.add_error_handler(self.error_handler)
        
        self.logger.info("Starting bot...")
        updater.start_polling()
        updater.idle()