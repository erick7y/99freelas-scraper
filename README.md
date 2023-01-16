# 99freelas-scraper
## Descrição
Um scraper que procura constantemente em períodos de tempo alternados por novos trabalhos na plataforma de freelancing https://99freelas.com.br.

## Uso
* Instale os requisitos: `pip3 install -r requirements.txt`
* Na pasta raíz do projeto, crie um arquivo chamado `telegram_bot_token.txt` e coloque o token do seu bot do Telegram lá.
* Crie outro arquivo chamado `telegram_chat_id.txt` e coloque o ID do chat do Telegram onde você deseja receber as mensagens.
* Você pode mudar as palavras-chave de pesquisa de projetos no arquivo `keywords.txt`.
* Rode o script `bot.py` usando o comando: `python3 bot.py`

## Tecnologias
* Python
* SQLite
* Beautiful Soup
