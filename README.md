# SabiAi_BOT


# SabiAi Bot
![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen)
![Gemini API](https://img.shields.io/badge/Gemini-API-lightgrey)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)
![Status](https://img.shields.io/badge/status-Em%20Desenvolvimento-orange)
[![Licença MIT](https://img.shields.io/badge/licença-MIT-yellow)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-blue?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/elias-barbosa-367280282)

![SabiAi Bot Banner](docs/banner1.png)

> **SabiAi Bot** é um assistente pessoal inteligente que integra a API Gemini e o Telegram para ajudar você no dia a dia.  
> O bot identifica, busca, adapta e revisa respostas para fornecer informações úteis, dicas e apoio.

![Demonstração do SabiAi Bot](docs/demo.gif)

## Tabela de Conteúdos
- [Requisitos](#requisitos)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Usar](#como-usar)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Requisitos
- Python 3.10+
- Token de API do Telegram
- Chave de API do Gemini
- Pip configurado

## Tecnologias
| Tecnologia | Função |
|------------|--------|
| **Python** | Linguagem principal |
| **python-telegram-bot** | Criação do bot no Telegram |
| **Google Generative AI (Gemini)** | Geração de conteúdo inteligente |
| **asyncio** | Execução assíncrona |
| **datetime, os** | Utilitários padrão do Python |

## Instalação
1️⃣ Clone o repositório:
```bash
git clone https://github.com/Elias1800/Sabi.Ai_BOT.git
cd SabiAi_Bot
```
2️⃣ Instale as dependências:
```bash
pip install python-telegram-bot google-generativeai
```

## Configuração
Edite o arquivo principal e Agentes, e insira suas chaves:
```python
genai.configure(api_key="SUA_CHAVE_GEMINI")
TOKEN_TELEGRAM = 'SUA_CHAVE_TELEGRAM'
```
💡 **Dica:** Para segurança, considere usar variáveis de ambiente no futuro.

## Como Usar
Execute no terminal:
```bash
python bot-telegram.py
```
📌 O bot ficará aguardando mensagens no Telegram.

## Contribuição
[Veja como contribuir](https://github.com/tiagoporto/.github/blob/main/CONTRIBUTING.md).

## Licença
Este projeto está licenciado sob os termos da [MIT License](LICENSE).

