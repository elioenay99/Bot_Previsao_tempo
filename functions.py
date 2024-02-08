import requests
import datetime
import logging
from cachetools import TTLCache
from functools import wraps
from Dicionario import traduzir_condicao
from Chaves import CHAVE as OPENWEATHER_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

cache_tempo = TTLCache(maxsize=100, ttl=600)  # 100 entradas, TTL = 10 minutos


def cached(cache):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = str(args) + str(kwargs)  # Gera uma chave simples baseada nos argumentos
            if cache_key in cache:
                logger.info(f"Resposta recuperada do cache para {func.__name__} com chave {cache_key}")
                return cache[cache_key]
            else:
                result = func(*args, **kwargs)
                cache[cache_key] = result
                logger.info(f"Nova chamada à API realizada por {func.__name__}")
                return result

        return wrapper

    return decorator


def obter_resposta_previsao_cidade(url, estendida=False):
    logger.info(f"Buscando dados para URL: {url}")  # Log antes de fazer a chamada à API
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            if estendida:
                mensagem = "Previsão para os próximos dias:\n"
                for item in dados['list'][::8]:  # A cada 8 itens para aproximadamente cada dia
                    data = datetime.datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%d/%m")
                    temperatura = item['main']['temp']
                    descricao, emoji = traduzir_condicao(item['weather'][0]['description'])
                    mensagem += f"{data}: {temperatura}°C, {descricao} {emoji}\n"
                logger.info("Dados obtidos com sucesso da API.")
                return mensagem
            else:  # Previsão comum
                temperatura = dados['main']['temp']
                descricao, emoji = traduzir_condicao(dados['weather'][0]['description'])
                logger.info("Dados obtidos com sucesso da API.")
                return f"Temperatura: {temperatura}°C\nCondição: {descricao} {emoji}"
        else:
            logger.error("Erro ao obter a previsão do tempo da API.")
            return "Erro ao obter a previsão do tempo."
    except Exception as e:
        logger.error(f"Erro ao buscar a previsão do tempo: {e}")
        return "Houve um erro ao buscar a previsão do tempo."


@cached(cache_tempo)
def buscar_previsao_comum_por_nome(cidade):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={OPENWEATHER_TOKEN}&units=metric"
    return obter_resposta_previsao(url)


@cached(cache_tempo)
def buscar_previsao_estendida_por_nome(cidade):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={OPENWEATHER_TOKEN}&units=metric"
    return obter_resposta_previsao(url, estendida=True)


def handle_location(update, context):
    user_location = update.message.location
    tipo_previsao = context.user_data.get('previsao_tipo', 'previsao_comum')

    if tipo_previsao == 'previsao_comum':
        resposta = buscar_previsao_comum(user_location.latitude, user_location.longitude)
    else:
        resposta = buscar_previsao_estendida(user_location.latitude, user_location.longitude)

    update.message.reply_text(resposta)


def previsao(update, context):
    # Assume que o usuário digita o nome da cidade após o comando
    if context.args:
        cidade = ' '.join(context.args)
        resposta = buscar_previsao_comum_por_nome(cidade)
    else:
        update.message.reply_text("Por favor, forneça o nome da cidade. Exemplo: /previsao Londres")
    update.message.reply_text(resposta)


def previsao_estendida(update, context):
    if context.args:
        cidade = ' '.join(context.args)
        resposta = buscar_previsao_estendida_por_nome(cidade)
    else:
        update.message.reply_text("Por favor, forneça o nome da cidade. Exemplo: /previsao_estendida Londres")
    update.message.reply_text(resposta)


@cached(cache_tempo)
def buscar_previsao_comum(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_TOKEN}&units=metric"
    return obter_resposta_previsao_cidade(url)


@cached(cache_tempo)
def buscar_previsao_estendida(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPENWEATHER_TOKEN}&units=metric"
    return obter_resposta_previsao_cidade(url, estendida=True)


def obter_resposta_previsao(url, estendida=False):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            if estendida:
                mensagem = "Previsão para os próximos dias:\n"
                for item in dados['list'][::8]:  # A cada 8 itens (aprox. a cada dia)
                    data = datetime.datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S").strftime("%d/%m")
                    temperatura = item['main']['temp']
                    descricao, emoji = traduzir_condicao(item['weather'][0]['description'])
                    mensagem += f"{data}: {temperatura}°C, {descricao} {emoji}\n"
                return mensagem
            else:  # Previsão comum
                temperatura = dados['main']['temp']
                descricao, emoji = traduzir_condicao(dados['weather'][0]['description'])
                return f"Temperatura: {temperatura}°C\nCondição: {descricao} {emoji}"
        else:
            return "Erro ao obter a previsão do tempo."
    except Exception as e:
        logger.error(f"Erro ao buscar a previsão do tempo: {e}")
        return "Houve um erro ao buscar a previsão do tempo."
