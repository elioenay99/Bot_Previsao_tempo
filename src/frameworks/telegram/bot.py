import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters, CallbackQueryHandler, ConversationHandler, CallbackContext, InlineQueryHandler
)

from src.adapters.controllers.telegram_controller import TelegramController
from src.adapters.repositories.favorites_repository import JsonFavoritesRepository
from uuid import uuid4


class TelegramBot:

    def __init__(self, telegram_token: str, controller: TelegramController):
        self.token = telegram_token
        self.controller = controller
        self.favorites_repository = JsonFavoritesRepository()
        self.logger = logging.getLogger(__name__)
    
    def start(self, update: Update, context: CallbackContext) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Previsão Atual", callback_data='current_forecast'),
                InlineKeyboardButton("Próximos 5 Dias", callback_data='extended_forecast')
            ],
            [
                InlineKeyboardButton("Favoritos", callback_data='favorites'),
                InlineKeyboardButton("Ajuda", callback_data='help')
            ]
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
/favoritar - Adiciona uma cidade aos favoritos. Uso: /favoritar <nome_da_cidade>
/desfavoritar - Remove uma cidade dos favoritos. Uso: /desfavoritar <nome_da_cidade>
/favoritos - Lista suas cidades favoritas.
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
• Favoritos - Gerencia suas cidades favoritas
• Ajuda - Mostra esta mensagem de ajuda

Você pode:
1. Clicar nos botões do menu
2. Compartilhar sua localização
3. Digite o nome de uma cidade após selecionar o tipo de previsão
4. Use /favoritar e /desfavoritar para gerenciar favoritos
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
                [
                    InlineKeyboardButton("Favoritos", callback_data='favorites'),
                    InlineKeyboardButton("Ajuda", callback_data='help')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text='Olá! Sou o Bot de Previsão do Tempo. Como posso ajudar?',
                reply_markup=reply_markup
            )
            return

        if query.data == 'favorites':
            user_id = update.effective_user.id
            favorites = self.favorites_repository.get_favorites(user_id)
            favorite_list = favorites.list_favorites()
            
            if not favorite_list:
                keyboard = [[InlineKeyboardButton("Voltar ao Menu", callback_data='start')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.edit_message_text(
                    text="Você ainda não tem cidades favoritas.\nUse /favoritar <cidade> para adicionar uma.",
                    reply_markup=reply_markup
                )
                return

            keyboard = [
                [InlineKeyboardButton("Previsão de Todas as Favoritas", callback_data='all_favorites')]
            ]
            for city in favorite_list:
                keyboard.append([
                    InlineKeyboardButton(f"Previsão para {city}", callback_data=f'fav_forecast_{city}'),
                ])
            keyboard.append([InlineKeyboardButton("Voltar ao Menu", callback_data='start')])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="Suas cidades favoritas:",
                reply_markup=reply_markup
            )
            return

        if query.data == 'all_favorites':
            user_id = update.effective_user.id
            favorites = self.favorites_repository.get_favorites(user_id)
            favorite_list = favorites.list_favorites()
            
            response = "Previsão para todas as suas cidades favoritas:\n\n"
            for city in favorite_list:
                city_forecast = self.controller.get_current_forecast_by_city(city)
                response += f"=== {city} ===\n{city_forecast}\n\n"
            
            keyboard = [[InlineKeyboardButton("Voltar aos Favoritos", callback_data='favorites')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=response, reply_markup=reply_markup)
            return

        if query.data.startswith('fav_forecast_'):
            city = query.data.replace('fav_forecast_', '')
            response = self.controller.get_current_forecast_by_city(city)
            keyboard = [[InlineKeyboardButton("Voltar aos Favoritos", callback_data='favorites')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=response, reply_markup=reply_markup)
            return

        context.user_data['forecast_type'] = query.data
        keyboard = [
            [InlineKeyboardButton("Voltar ao Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="Por favor, digite o nome de uma cidade ou compartilhe sua localização.",
            reply_markup=reply_markup
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
    
    def favorite_city(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            update.message.reply_text(
                "Por favor, forneça o nome da cidade. Exemplo: /favoritar Londres"
            )
            return
        
        city_name = ' '.join(context.args)
        user_id = update.effective_user.id
        favorites = self.favorites_repository.get_favorites(user_id)
        
        if favorites.add_favorite(city_name):
            self.favorites_repository.save_favorites(favorites)
            update.message.reply_text(f"A cidade {city_name} foi adicionada aos seus favoritos!")
        else:
            update.message.reply_text(f"A cidade {city_name} já está nos seus favoritos!")

    def unfavorite_city(self, update: Update, context: CallbackContext) -> None:
        if not context.args:
            update.message.reply_text(
                "Por favor, forneça o nome da cidade. Exemplo: /desfavoritar Londres"
            )
            return
        
        city_name = ' '.join(context.args)
        user_id = update.effective_user.id
        favorites = self.favorites_repository.get_favorites(user_id)
        
        if favorites.remove_favorite(city_name):
            self.favorites_repository.save_favorites(favorites)
            update.message.reply_text(f"A cidade {city_name} foi removida dos seus favoritos!")
        else:
            update.message.reply_text(f"A cidade {city_name} não estava nos seus favoritos!")

    def list_favorites(self, update: Update, context: CallbackContext) -> None:
        user_id = update.effective_user.id
        favorites = self.favorites_repository.get_favorites(user_id)
        favorite_list = favorites.list_favorites()
        
        if not favorite_list:
            update.message.reply_text(
                "Você ainda não tem cidades favoritas.\nUse /favoritar <cidade> para adicionar uma."
            )
            return
        
        message = "Suas cidades favoritas:\n\n"
        for city in favorite_list:
            message += f"• {city}\n"
        message += "\nUse /previsao <cidade> para ver a previsão do tempo."
        
        update.message.reply_text(message)

    def handle_text(self, update: Update, context: CallbackContext) -> None:
        forecast_type = context.user_data.get('forecast_type')
        if not forecast_type:
            return

        city_name = update.message.text
        
        if forecast_type == 'current_forecast':
            response = self.controller.get_current_forecast_by_city(city_name)
        elif forecast_type == 'extended_forecast':
            response = self.controller.get_extended_forecast_by_city(city_name)
        else:
            return

        keyboard = [
            [InlineKeyboardButton("Voltar ao Menu", callback_data='start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(response, reply_markup=reply_markup)
        context.user_data.pop('forecast_type', None)

    def run(self) -> None:
        updater = Updater(self.token, use_context=True)
        dp = updater.dispatcher
        
        # Register handlers
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("ajuda", self.help_command))
        dp.add_handler(CommandHandler("previsao", self.current_forecast, pass_args=True))
        dp.add_handler(CommandHandler("previsao_estendida", self.extended_forecast, pass_args=True))
        dp.add_handler(CommandHandler("favoritar", self.favorite_city, pass_args=True))
        dp.add_handler(CommandHandler("desfavoritar", self.unfavorite_city, pass_args=True))
        dp.add_handler(CommandHandler("favoritos", self.list_favorites))
        dp.add_handler(CallbackQueryHandler(self.button_callback))
        dp.add_handler(MessageHandler(Filters.location, self.handle_location))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text))
        dp.add_handler(InlineQueryHandler(self.inline_query))
        
        dp.add_error_handler(self.error_handler)
        
        self.logger.info("Starting bot...")
        updater.start_polling()
        updater.idle()