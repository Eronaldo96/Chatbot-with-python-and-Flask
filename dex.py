from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import logging
import re

app = Flask(__name__)

user_memory = {}

bot = ChatBot(
    'DEX ChatBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'Não entendi bem. Pode reformular?',
            'maximum_similarity_threshold': 0.85
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'  # Habilita cálculos
        }
    ]
)

logging.basicConfig(level=logging.WARNING)

def train_bot():
    trainer = ListTrainer(bot)
    basic_conversation = [
        'Oi', 'Olá! Como vai você?',
        'Tudo bem?', 'Sim, estou bem! E você?',
        'Qual é seu nome?', 'Meu nome é DEX.',
        'Quem te criou?', 'Fui criado por um desenvolvedor chamado Eronaldo!',
        'Você sabe matemática?', 'Sim! Me pergunte uma conta matemática.',
        'Obrigado', 'De nada! Estou aqui para ajudar.'
    ]
    trainer.train(basic_conversation)

train_bot()

@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')

@app.route("/get", methods=['GET'])
def get_bot_response():
    user_text = request.args.get('msg').strip().lower()

    if 'meu nome é' in user_text:
        nome = user_text.replace('meu nome é', '').strip().title()
        user_memory['nome'] = nome
        return jsonify({'response': f'Entendido! Seu nome é {nome}.', 'learned': True})
    
    if 'qual é o meu nome' in user_text:
        if 'nome' in user_memory:
            return jsonify({'response': f'Seu nome é {user_memory["nome"]}!', 'learned': False})
        return jsonify({'response': 'Ainda não sei seu nome. Pode me dizer?', 'learned': False})

    if re.match(r'^\d+(\s*[\+\-\*/]\s*\d+)+$', user_text):
        try:
            result = eval(user_text)
            return jsonify({'response': f'O resultado é {result}.', 'learned': False})
        except:
            return jsonify({'response': 'Não consegui calcular isso. Tente algo mais simples.', 'learned': False})

    if user_text in ['como você está?', 'tudo bem?', 'como vai?', 'como vai você?']:
        return jsonify({'response': 'Estou bem! Obrigado por perguntar.', 'learned': False})

    try:
        response = bot.get_response(user_text)
        if response.confidence < 0.5:
            return jsonify({'response': 'Não entendi bem. Pode reformular?', 'learned': False})
        return jsonify({'response': str(response), 'learned': False})
    except Exception as e:
        return jsonify({'response': 'Ocorreu um erro ao processar sua mensagem.', 'learned': False})

if __name__ == "__main__":
    app.run()
