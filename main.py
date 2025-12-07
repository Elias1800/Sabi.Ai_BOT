from telegram import Update, constants
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import asyncio
import os

# CONFIGURAÇÕES 
GEMINI_API_KEY = "AIzaSyA0OYv2V4V1zud8Z0YWqlye-d0IYzeHtTk"
TOKEN_TELEGRAM = "7654266195:AAGYNmiIglcTHP_prxkf4VL46s3QqQLIOm0"

genai.configure(api_key=GEMINI_API_KEY)

# CONFIGURAÇÃO DO MODELO GEMINI
INSTRUCOES_SISTEMA = """
Você é o Sabi.Ai, um assistente virtual pessoal para Telegram, útil, carismático e eficiente.
Use um tom natural, fluido, levemente informal, mas educado. Use emojis moderadamente.

SUAS RESPONSABILIDADES:
1. Identificar a intenção do usuário (dúvida, conversa, pesquisa, ajuda).
2. Se o usuário pedir informações atuais (notícias, clima, cotações, fatos recentes), USE A FERRAMENTA DE BUSCA DO GOOGLE.
3. Se for conversa, responda com empatia e mantenha o contexto.
4. Formatação: O Telegram suporta Markdown. Use negrito (ex: **texto**) para destaques. Evite # para títulos, use negrito e quebras de linha.

IMPORTANTE:
- Não diga "Vou pesquisar para você". Apenas pesquise e entregue a resposta.
- Seja objetivo.
"""

# Configurações de segurança
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    system_instruction=INSTRUCOES_SISTEMA,
    safety_settings=safety_settings
)

# MEMÓRIA DO BOT
# Dicionário para guardar o histórico de conversa de cada usuário
user_sessions = {}

def get_chat_session(user_id):
    """Recupera a sessão do usuário ou cria uma nova se não existir."""
    if user_id not in user_sessions:
        user_sessions[user_id] = model.start_chat(history=[])
    return user_sessions[user_id]


# FUNÇÕES DO TELEGRAM

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    # Limpa a memória se o usuário der /start novamente
    user_id = update.effective_user.id
    if user_id in user_sessions:
        del user_sessions[user_id]
        
    await update.message.reply_text(
        f"""Olá, {user_first_name} 👋
Eu sou o **Sabi.Ai**, seu assistente pessoal inteligente.

Estou aqui para:
● Tirar dúvidas e pesquisar na web
● Organizar ideias 
● Conversar e dar dicas 

Como posso te ajudar hoje?"""
    )

async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    entrada_do_usuario = update.message.text
    user_id = update.effective_user.id

    # Verificação básica
    if not entrada_do_usuario or len(entrada_do_usuario.strip()) < 1:
        await update.message.reply_text("Não entendi. Pode repetir?")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)

    try:
        # 1. Pega a sessão exclusiva desse usuário
        chat_session = get_chat_session(user_id)

        # 2. Envia para o Gemini (usando thread separada para não travar o bot)
        response = await asyncio.to_thread(chat_session.send_message, entrada_do_usuario)

        # 3. Responde ao usuário
        await update.message.reply_text(response.text, parse_mode="Markdown")

    except Exception as e:
        print(f"Erro no processamento (User {user_id}): {e}")
        # Se der erro de sessão, reinicia a sessão
        if user_id in user_sessions:
            del user_sessions[user_id]
        
        await update.message.reply_text("Tive um pequeno problema técnico. Tente perguntar novamente!")

# INICIALIZAÇÃO 
if __name__ == '__main__':
    # Cria o bot
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

    # Adiciona os comandos
    app.add_handler(CommandHandler("start", start))
    
    # Adiciona o handler de mensagens de texto 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_mensagem))

    print("Sabi.Ai iniciado com sucesso! 🚀")
    
    # Roda o bot 
    app.run_polling()