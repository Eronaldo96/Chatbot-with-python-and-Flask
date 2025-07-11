# chatbot/logic.py
import re
from config import gemini_model # Importa o modelo do config

def summarize_text(text: str) -> str:
    if len(text.split()) < 10:
        return "O texto é muito curto para gerar um resumo."
    try:
        prompt = f"Resuma o seguinte texto em até 3 frases claras e objetivas:\n\n{text}"
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Erro ao gerar resumo. Verifique o texto ou a conexão."

def safe_eval_math(expression: str) -> str:
    if not re.match(r'^[\d\s\+\-\*/\(\)\.]+$', expression):
        return "Cálculo inválido."
    try:
        return f'O resultado é {eval(expression)}.'
    except:
        return "Não consegui calcular isso."
