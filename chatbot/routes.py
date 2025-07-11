# chatbot/routes.py
import re
from flask import Flask, render_template, request, jsonify
from config import bot # Importa o bot do config
from chatbot.logic import summarize_text, safe_eval_math # Importa a lógica

app = Flask(__name__, template_folder='../templates', static_folder='../static')

user_memory = {}

def process_user_message(user_text: str) -> str:
    if user_text.startswith('resumir texto:'):
        text = user_text.replace('resumir texto:', '').strip()
        return summarize_text(text) if text else "Forneça o texto a ser resumido."

    if 'meu nome é' in user_text:
        name = user_text.split('meu nome é')[1].strip().title()
        user_memory['name'] = name
        return f'Entendido, {name}!'

    if user_text == 'qual é o meu nome':
        return f'Seu nome é {user_memory.get("name", "quem?")}!'

    if re.match(r'^[\d\s\+\-\*/\(\)\.]+$', user_text):
        return safe_eval_math(user_text)

    response = bot.get_response(user_text)
    return str(response)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg', '').strip().lower()
    if not user_text:
        return jsonify({'response': 'Diga algo.'})
    
    response = process_user_message(user_text)
    return jsonify({'response': response})
