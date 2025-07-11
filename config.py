# config.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a API do Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# Configura e treina o ChatterBot
bot = ChatBot(
    'DEX ChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        {'import_path': 'chatterbot.logic.BestMatch', 'default_response': 'Não entendi bem...', 'maximum_similarity_threshold': 0.90}
    ]
)

trainer = ListTrainer(bot)
basic_conversation = [
    'Oi', 'Olá! Como vai você?',
    'Tudo bem?', 'Estou ótimo! E você?',
    'Qual é seu nome?', 'Meu nome é DEX.',
    'Quem te criou?', 'Fui criado por um desenvolvedor chamado Eronaldo!',
    'Obrigado', 'De nada!'
]
trainer.train(basic_conversation)
