from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


app = Flask(__name__)
app.config.from_object('config')


bot = ChatBot('DEX ChatBot')

conversa = ['Turnos do Curso de sistemas de informação','Sistemas de Informação -> Turno: Noite - Horário AB (18h35min às 20h15min) Horário CD (20h35min às 22h15min) ' ]
bot.set_trainer(ListTrainer)
#trainer = ChatterBotCorpusTrainer(bot)

#trainer.train("chatterbot.corpus.dex.greetings")
#for files in os.listdir('./chatterbot_corpus1/'):
#    data=open('./chatterbot_corpus1/'+files,'r').readlines()
#    bot.train(data)

bot.train(conversa)

@app.route("/home/")
@app.route("/")
def index():
    return render_template('home.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    resposta = bot.get_response(userText)
    if((resposta.confidence) > 0.75):
        return str(resposta)
    else:
        pergunta = [userText]
        bot.train(pergunta)
        return str('Sua mensagem me ajudará a aprender, mas por enquanto não tenho uma resposta')
if __name__ == "__main__":
    app.run()
#bot.get_response(userText)
#host='::',debug=True
