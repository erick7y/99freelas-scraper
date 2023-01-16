import requests
import sqlite3
from time import sleep
from random import randint
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent

user_agent_rotator = UserAgent(limit=1000)

def random_user_agent():
  return user_agent_rotator.get_random_user_agent()

'''
Criando a tabela no banco de dados se ela ainda não existe.
'''
conn = sqlite3.connect('already_extracted.sqlite3')

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS already_extracted (project_id integer NOT NULL)
''')

conn.commit()

def project_is_already_extracted(project_id):
  cur.execute( '''
    SELECT * FROM already_extracted WHERE project_id = %d;
  ''' % (int(project_id)) )

  result = cur.fetchall()

  if len(result) == 0:
    return False
  return True

def insert_project_into_table_of_already_extracted_projects(project_id):
  cur.execute( '''
    INSERT INTO already_extracted (project_id) VALUES (%d);
  ''' % (int(project_id)) )

  conn.commit()

'''
Pega o token do bot do Telegram.
'''
with open('telegram_bot_token.txt', 'r') as telegram_bot_token_file:
  telegram_bot_token = telegram_bot_token_file.read().strip()

'''
Pega o ID da sala do Telegram.
'''
with open('telegram_chat_id.txt', 'r') as telegram_chat_id_file:
  telegram_chat_id = telegram_chat_id_file.read().strip()

def send_telegram_message(project_obj):
  
  text = '%s\n\n*%s*\n\n%s' % (project_obj['url'], project_obj['title'], project_obj['description'])
  
  requests.get(f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={text}&disable_web_page_preview=true&parse_mode=markdown')

if __name__ == '__main__':
  while True:
    
    headers = {
      'User-Agent': random_user_agent()
    }
    response = requests.get('https://www.99freelas.com.br/projects?q=python', headers=headers)
    
    if response.status_code != 200:
      print(response.text)
      exit()
    
    html_doc = response.text
    
    soup = BeautifulSoup(html_doc, features='lxml')
    
    for project in soup.find_all(class_='result-item'):
      project_id = project.get('data-id')
      
      if not project_is_already_extracted(project_id):
        insert_project_into_table_of_already_extracted_projects(project_id)
        
        '''
        Pega as informações do projeto para enviar por mensagem no Telegram.
        '''
        project_obj = {
          'url': 'https://www.99freelas.com.br' + project.find_all(class_='title')[0].find_all('a')[0].get('href'),
          'title': project.find_all(class_='title')[0].find_all('a')[0].text,
          'description': project.find_all(class_='description')[0].text.strip()
        }
        
        send_telegram_message(project_obj)
    
    sleep(randint(900, 1800)) # espera entre 15 e 30 minutos antes de fazer
                              # uma nova requisição para buscar por novos
                              # trabalhos.
