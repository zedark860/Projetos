from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from auto_download_undetected_chromedriver import download_undetected_chromedriver
import time
import logging
import csv
import os
import pandas as pd
import undetected_chromedriver as uc
import psutil

LOGGER.setLevel(logging.WARNING)
url = 'https://casadosdados.com.br/solucao/cnpj/pesquisa-avancada'

xpath_cnpj = '//*[@id="__nuxt"]/div/div[2]/section/div/div/div[4]/div/div/div[1]/p[2]'
xpath_razao_social = '.columns:nth-child(1) > .column:nth-child(2) > p:nth-child(2)'
xpath_nome_fantasia = '//*[@id="__nuxt"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[1]/div[3]/p[2]'
xpath_telefone = 'id("__nuxt")/DIV[1]/DIV[2]/SECTION[1]/DIV[1]/DIV[1]/DIV[4]/DIV[1]/DIV[3]/DIV[1]/P[2]/A[1]'
xpath_telefone2 = '//*[@id="__nuxt"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[3]/div[1]/p[3]/a'
xpath_email = '.column:nth-child(2) > p > a'
xpath_data_abertura = '.column > a'
xpath_situacao_cadastral = '.columns:nth-child(1) > .column:nth-child(6) > p:nth-child(2)'
xpath_capital_social = '.column:nth-child(8) > p:nth-child(2)'
xpath_cnae = '//*[@id="__nuxt"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[1]/div[9]/p[2]'
xpath_mei = '//*[@id="__nuxt"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[1]/div[10]/p[2]'
xpath_logradouro = 'id("__nuxt")/DIV[1]/DIV[2]/SECTION[1]/DIV[1]/DIV[1]/DIV[4]/DIV[1]/DIV[2]/DIV[1]/P[2]'
xpath_numero = '.columns:nth-child(2) > .column:nth-child(2) > p:nth-child(2)'
xpath_cep = 'id("__nuxt")/DIV[1]/DIV[2]/SECTION[1]/DIV[1]/DIV[1]/DIV[4]/DIV[1]/DIV[2]/DIV[4]/P[2]'
xpath_bairro = 'id("__nuxt")/DIV[1]/DIV[2]/SECTION[1]/DIV[1]/DIV[1]/DIV[4]/DIV[1]/DIV[2]/DIV[5]/P[2]'
xpath_municipio = '.column:nth-child(6) > p > a'
xpath_uf = '//*[@id="__nuxt"]/div/div[2]/section[1]/div/div/div[4]/div[1]/div[2]/div[7]/p[2]/a'


def configurar_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')

    user_dir = os.path.expanduser("~")
    webdriver_path = os.path.join(
        user_dir, 'Desktop', 'extractor_cnpj', 'chromedriver.exe')
    os.environ['PATH'] = f'{os.environ["PATH"]};{os.path.abspath(webdriver_path)}'

    # Create the Chrome driver with the configured options
    driver = uc.Chrome(options=chrome_options, executable_path=webdriver_path,
                       headless=False)

    return driver


def WaitButton(driver, tempo_maximo=30):
    botao_clicado = False

    try:
        # Aguarde até que o botão seja clicável por até 30 segundos
        botao = WebDriverWait(driver, tempo_maximo).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a.button.is-success.is-medium'))
        )

        # Adiciona um ouvinte de evento para detectar o clique do mouse
        driver.execute_script('''
            document.querySelector('a.button.is-success.is-medium').addEventListener('click', function() {
                window.buttonClicked = true;
            });
        ''')

        # Espera até que o tempo máximo seja atingido ou até que alguém clique no botão
        start_time = time.time()
        while time.time() - start_time < tempo_maximo:
            # Verifica se o botão foi clicado
            if driver.execute_script('return window.buttonClicked'):
                botao_clicado = True
                print("Começando extração...")

                time.sleep(5)
                break

            # Aguarde um curto período antes de verificar novamente
            time.sleep(1)

    except TimeoutException:
        print(
            f"Tempo máximo de espera ({tempo_maximo} segundos) atingido. A pessoa ainda tem tempo para clicar no botão.")

    return botao_clicado


def extrair_dados():
    elementos_p = driver.find_elements(By.CSS_SELECTOR, '.box p')
    dados_temporarios = []

    for elemento in elementos_p:
        strongs = elemento.find_elements(By.TAG_NAME, 'strong')
        if len(strongs) >= 2:
            numero_cnpj = ''.join(c for c in strongs[0].text if c.isdigit())
            razao_social = strongs[1].text.strip().replace(
                ' ', '-').replace(',', '')
            dado = f'{razao_social}-{numero_cnpj}'
            dados_temporarios.append(dado)

    return dados_temporarios

# Função para clicar no botão da próxima página


def clicar_proxima_pagina():
    try:
        botao_proxima_pagina = driver.find_element(
            By.CSS_SELECTOR, '.pagination-link.pagination-next.pagination-next')

        if botao_proxima_pagina and 'is-disabled' not in botao_proxima_pagina.get_attribute('class'):
            botao_proxima_pagina.click()
            return True
    except Exception as e:
        print(f'Erro ao clicar na próxima página: {e}')

    print('Botão de próxima página não encontrado ou desabilitado.')
    return False


def extrair_dados_de_todas_as_paginas():
    while True:
        dados_da_pagina = extrair_dados()

        if dados_da_pagina:
            dados_armazenados.extend(dados_da_pagina)
            pode_prosseguir = clicar_proxima_pagina()

            if not pode_prosseguir:
                print('Extração de dados concluída.')
                break
        else:
            print('Não há mais dados para extrair.')
            break


def pegar_informacoes():
    razao_social = nome_fantasia = cnpj = telefone = telefone2 = email = data_abertura = situacao_cadastral = capital_social = cnae = mei = logradouro = numero = cep = bairro = municipio = uf = ''

    try:
        razao_social = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, xpath_razao_social)))
    except TimeoutException:
        razao_social = None

    try:
        nome_fantasia = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_nome_fantasia)))
    except TimeoutException:
        nome_fantasia = None

    try:
        cnpj = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_cnpj)))
    except TimeoutException:
        cnpj = None

    try:
        telefone = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_telefone)))
    except TimeoutException:
        telefone = None

    try:
        telefone2 = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_telefone2)))
    except TimeoutException:
        telefone2 = None

    try:
        email = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, xpath_email)))
    except TimeoutException:
        email = None

    try:
        data_abertura = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, xpath_data_abertura)))
    except TimeoutException:
        data_abertura = None

    try:
        situacao_cadastral = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, xpath_situacao_cadastral)))
    except TimeoutException:
        situacao_cadastral = None

    try:
        capital_social = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, xpath_capital_social)))
    except TimeoutException:
        capital_social = None

    try:
        cnae = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_cnae)))
    except TimeoutException:
        cnae = None

    try:
        mei = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_mei)))
    except TimeoutException:
        mei = None

    try:
        logradouro = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_logradouro)))
    except TimeoutException:
        logradouro = None

    try:
        numero = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, xpath_numero)))
    except TimeoutException:
        numero = None

    try:
        cep = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_cep)))
    except TimeoutException:
        cep = None

    try:
        bairro = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_bairro)))
    except TimeoutException:
        bairro = None

    try:
        municipio = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, xpath_municipio)))
    except TimeoutException:
        municipio = None

    try:
        uf = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath_uf)))
    except TimeoutException:
        uf = None

    return razao_social, nome_fantasia, cnpj, telefone, telefone2, email, data_abertura, situacao_cadastral, capital_social, cnae, mei, logradouro, numero, cep, bairro, municipio, uf


# Configuração do WebDriver
with configurar_driver() as driver:
    driver.get(url)

    # Aguarde até que o botão seja clicado ou tempo máximo atingido
    botao_clicado = WaitButton(driver)

    if botao_clicado:
        # Continue com o restante do seu código
        dados_armazenados = []
        if not dados_armazenados:
            dados_armazenados = []

        extrair_dados_de_todas_as_paginas()

        with open('dados.csv', 'w', newline='') as csvfile:
            fieldnames = ['empresa']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for dado in dados_armazenados:
                row_dict = {'empresa': dado}
                writer.writerow(row_dict)
    else:
        print("Botão não foi clicado.")

# Feche o navegador
driver.quit()

# Leia os dados do arquivo CSV
df = pd.read_csv('dados.csv')

# Configuração do novo WebDriver
driver = configurar_driver()

url_base = 'https://casadosdados.com.br/solucao/cnpj/'

dados_armazenados_planilha = []

for i, row in df.iterrows():
    item = row['empresa']

    url_completa = url_base + item

    driver.get(url_completa)

    try:
        # Verifique se os elementos estão presentes na página
        razao_social, nome_fantasia, cnpj, telefone, telefone2, email, data_abertura, situacao_cadastral, capital_social, cnae, mei, logradouro, numero, cep, bairro, municipio, uf = pegar_informacoes()

        # Adiciona as informações à lista
        dados_armazenados_planilha.append({
            'Razão Social': str(razao_social.text) if razao_social else '',
            'Nome Fantasia': str(nome_fantasia.text) if nome_fantasia else '',
            'CNPJ': str(cnpj.text) if cnpj else '',
            'Telefone': str(telefone.text) if telefone else '',
            'Telefone 2': str(telefone2.text) if telefone2 else '',
            'E-Mail': str(email.text) if email else '',
            'Data Abertura': str(data_abertura.text) if data_abertura else '',
            'Situação Cadastral': str(situacao_cadastral.text) if situacao_cadastral else '',
            'Capital Social': str(capital_social.text) if capital_social else '',
            'CNAE': str(cnae.text) if cnae else '',
            'MEI': str(mei.text) if mei else '',
            'Logradouro': str(logradouro.text) if logradouro else '',
            'Número': str(numero.text) if numero else '',
            'CEP': str(cep.text) if cep else '',
            'Bairro': str(bairro.text) if bairro else '',
            'Município': str(municipio.text) if municipio else '',
            'UF': str(uf.text) if uf else ''
        })

    except Exception as e:
        print(f"Erro ao extrair informações da URL {url_completa}: {e}")
        dados_armazenados_planilha.append({
            'Razão Social': '',
            'Nome Fantasia': '',
            'CNPJ': '',
            'Telefone': '',
            'Telefone 2': '',
            'E-Mail': '',
            'Data Abertura': '',
            'Situação Cadastral': '',
            'Capital Social': '',
            'CNAE': '',
            'MEI': '',
            'Logradouro': '',
            'Número': '',
            'CEP': '',
            'Bairro': '',
            'Município': '',
            'UF': ''
        })

driver.quit()
# Encerre todos os processos do Google Chrome
for process in psutil.process_iter(['pid', 'name']):
    if 'chrome' in process.info['name'].lower():
        try:
            psutil.Process(process.info['pid']).terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

time.sleep(2)

if dados_armazenados_planilha is not None:
    df_informacoes = pd.DataFrame(dados_armazenados_planilha, columns=[
        'Razão Social',
        'Nome Fantasia',
        'CNPJ',
        'Telefone',
        'Telefone 2',
        'E-Mail',
        'Data Abertura',
        'Situação Cadastral',
        'Capital Social',
        'CNAE',
        'MEI',
        'Logradouro',
        'Número',
        'CEP',
        'Bairro',
        'Município',
        'UF'
    ])

else:
    print("Os dados armazenados estão vazios ou None. Verifique a extração de dados.")

df_informacoes.to_excel('Extração CNPJ.xlsx', index=False)
