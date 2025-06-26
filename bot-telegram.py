from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from datetime import date
import asyncio
import os
from Agentes import agente_revisor, agente_adaptador, agente_buscador, agente_identificador
import google.generativeai as genai

genai.configure(api_key="") #CHAVE DA API DO GEMINI

# API
TOKEN_TELEGRAM = '' # CHAVE DA API DO TELEGRAM

# Função que responde ao comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""Olá, {update.effective_user.first_name} 👋  
Eu sou o 𝗦𝗮𝗯𝗶.𝗔𝗶, seu assistente pessoal inteligente.  

Estou aqui para te ajudar com o que for preciso:  

● Tirar dúvidas  
● Encontrar informações  
● Organizar sua rotina  
● Dar dicas  
● Ouvir você  
● Ou até trazer um momento de leveza no dia.

É só me dizer o que você precisa e eu te ajudo a resolver!  
"""
    )

# Mensagem do usuário comum
async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    entrada_do_usuario = update.message.text
    data_de_hoje = date.today().strftime("%d/%m/%Y")

    # Verificação de entrada vazia ou muito curta
    if not entrada_do_usuario or len(entrada_do_usuario.strip()) < 3:
        await update.message.reply_text("Por favor, envie uma pergunta ou solicitação mais clara! 😊")
        return

    await update.message.reply_text("🔄 Processando sua solicitação, um momento...")

    try:
        topico = await agente_identificador(entrada_do_usuario)
        pesquisa = await agente_buscador(topico, data_de_hoje)
        adaptado = await agente_adaptador(topico, pesquisa)
        resposta_final = await agente_revisor(topico, adaptado)

        await update.message.reply_text(resposta_final)

    except Exception as e:
        # Tratamento de exceções para evitar travamentos
        print("Erro durante o processamento:", e)
        await update.message.reply_text("⚠️ Ocorreu um erro ao processar sua solicitação. Tente novamente em instantes!")

# Inicializa o bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_mensagem))

    print("Bot iniciado...")
    app.run_polling()