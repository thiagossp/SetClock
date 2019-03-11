import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import configparser

# load config file
cfg = configparser.ConfigParser()
cfg.read('conf.ini')

usernameStr = 'primmesf'
passwordStr = 'x'

def loadLink(linkText):
    link = None
    attempts = 0
    while not link:
        try:
            link = browser.find_element_by_link_text(linkText)
            link.click()
            return True
        except NoSuchElementException:
            attempts += 1
            if attempts == 3: return False
            time.sleep(1)

def loadLogin():
    element = None
    attempts = 0
    while not element:
        try:
            element = browser.find_element_by_id('lblLogin')
            element.send_keys(usernameStr)
            element = browser.find_element_by_id('lblPass')
            element.send_keys(passwordStr)
            return(True)
        except NoSuchElementException:
            attempts += 1
            if attempts == 3: return (False)
            if loadLink('Voltar'): continue
            if loadLink('Sair'): continue

def setClock(address, name):
    try:
        browser.get(address)
        if browser.title == 'Henry Web Server':
            if loadLogin():
                loadLink('Entrar')
                loadLink('Relógio')
                loadLink('Sincronizar data e hora com o computador')
                loadLink('Salvar')
                loadLink('Sair')
                fileContent.append(str(now.today()) + ': ' + address + ' ('+ name + ') Atualizado com sucesso.\n')
            else: raise Exception('Falha ao logar')
        else: raise Exception('Falha ao acessar o endereço')
    except NoSuchElementException:
        fileContent.append(str(now.today()) + ': ' + address + ' ('+ name + ') Erro desconhecido.\n')
        print('Erro: ' + address)
    except Exception as error:
        fileContent.append(str(now.today()) + ': ' + address + ' ('+ name + ') ' + repr(error) + '\n')

browser = webdriver.Chrome()
now = datetime.now()
file = open('setClock.log', 'r')
fileContent = file.readlines()
fileContent.append(str(now.today()) + ' Script started \n')

for section in cfg.sections():
    for option in cfg.options(section):
        setClock(cfg.get(section, option), section)

fileContent.append(str(now.today()) + ' Script finished \n')
file = open('setClock.log', 'w')
file.writelines(fileContent)
file.close()
browser.quit()