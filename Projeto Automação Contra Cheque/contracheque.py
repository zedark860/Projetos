# Adicione as bibliotecas necessárias para a automação web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import pyautogui
import glob
import datetime

url_site = 'https://assinarweb.com.br/arweb/login'

login = ''
senha = ''
# Obtém o diretório do usuário da máquina atual
user_directory = os.path.expanduser("~")
# Cria o caminho completo para o diretório de PDFs
diretorio_pdf = os.path.join(user_directory, 'Desktop', 'ContraCheque', 'PDF')
arquivos_pdf = glob.glob(os.path.join(diretorio_pdf, '*.pdf'))
arquivos = os.listdir(diretorio_pdf)


def ler_planilha(planilha_path, coluna_nome):
    try:
        if planilha_path:
            df = pd.read_excel(planilha_path, engine="openpyxl",
                               converters={coluna_nome: str})
            if not df.empty:
                if coluna_nome in df.columns:
                    return df[[coluna_nome]].dropna(subset=[coluna_nome])
                else:
                    raise Exception(
                        f'A coluna "{coluna_nome}" não existe na planilha.')
            else:
                raise Exception("A planilha está vazia.")
        else:
            raise FileNotFoundError("Arquivo da planilha não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao ler planilha: {str(e)}")


def encontrar_pdf(nome):
    # Obtém o diretório do usuário da máquina atual
    user_directory = os.path.expanduser("~")

    diretorio_pdfs = os.path.join(
        user_directory, 'Desktop', 'ContraCheque', 'PDF')
    nome = f"{nome}"
    extensao = '.pdf'

    caminho_completo = os.path.join(diretorio_pdfs, f"{nome}{extensao}")

    print("Arquivo PDF sendo procurado:", caminho_completo)

    if os.path.exists(caminho_completo):
        return caminho_completo
    else:
        return None


# Exemplo de uso
try:
    # Obtém o diretório do usuário da máquina atual
    user_directory = os.path.expanduser("~")

    # Cria o caminho completo para a planilha
    planilha_path = os.path.join(
        user_directory, 'Desktop', 'ContraCheque', 'Funcionários2024.xlsx')
    coluna_nome = 'NOME'

    if not os.path.exists(planilha_path):
        raise FileNotFoundError(
            f"Arquivo da planilha não encontrado: {planilha_path}")

    df_contatos = ler_planilha(planilha_path, coluna_nome)

    # Agora você tem um DataFrame contendo as colunas 'NOME' e 'ARQUIVOS' sem valores nulos
    print(df_contatos)
except Exception as e:
    print(f"Erro: {str(e)}")

# Define a função para escrever no log


def escrever_log(mensagem):
    with open("enviados.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n")


def escrever_erro(mensagem):
    with open("erros.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n")


def enviar_contracheques(login, senha, contatos):
    # Configurações do WebDriver do Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')

    # Configuração do caminho do driver do Chrome
    user_dir = os.path.expanduser("~")
    webdriver_path = os.path.join(
        user_dir, 'Desktop', 'ContraCheque', 'chrome', 'chromedriver.exe')

    # Adicione o caminho do driver ao PATH
    os.environ['PATH'] = f'{os.environ["PATH"]};{os.path.abspath(webdriver_path)}'

    quantidade = 0

    # Itera sobre os colaboradores ativos e realiza a automação no site
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url_site)

        # Realiza o login apenas uma vez fora do loop
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.NAME, 'nome'))).send_keys(str(login))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.NAME, 'password'))).send_keys(str(senha))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
            (By.NAME, 'nome'))).send_keys(Keys.RETURN)

        # Itera sobre os colaboradores ativos e realiza a automação no site
        for _, row in contatos.iterrows():
            nome_colaborador = row["NOME"]
            print(f"Processando: {nome_colaborador}")

            # Clique no primeiro botão
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'm-widget4__ext')))
            element.click()

            # Clique no segundo botão
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="m_wizard_form_step_1"]/div/div[2]/div[2]/label/span[1]/span/span')))
            element.click()

            time.sleep(5)

            # Abre a tela de seleção de arquivo no navegador
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, 'mDropzoneEnvelope')))
            element.click()

            # Encontra o caminho do arquivo PDF usando a função encontrar_pdf
            caminho_pdf = encontrar_pdf(nome_colaborador)

            print(f"Caminho do PDF para {nome_colaborador}: {caminho_pdf}")

            time.sleep(5)

            if caminho_pdf:
                try:
                    # Clique na caixa de diálogo para torná-la ativa
                    pyautogui.FAILSAFE = False

                    # Digite o caminho completo do arquivo usando pyautogui
                    pyautogui.write(caminho_pdf)

                    # Pressione Enter para confirmar a seleção
                    pyautogui.press('enter')

                    time.sleep(5)

                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="m_form"]/div[2]/div/div/div[2]/a[2]/span'))).click()

                    time.sleep(5)

                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="m_wizard_form_step_2"]/div/button[2]'))).click()

                    time.sleep(5)

                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="tblBuscarParticipantes_filter"]/label/input'))).click()

                    time.sleep(5)

                    # Clique no campo de filtro
                    search_input = driver.find_element(
                        By.XPATH, '//*[@id="tblBuscarParticipantes_filter"]/label/input')
                    search_input.click()

                    # ira o nome na caixa de texto
                    search_input.send_keys(nome_colaborador)

                    # Pressiona Enter para executar a pesquisa
                    search_input.send_keys(Keys.RETURN)

                    # Aguarde a página carregar (ajuste conforme necessário)
                    time.sleep(5)

                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="tblBuscarParticipantes"]/tbody/tr/td[5]/a'))).click()
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="adicionarNovo"]/div[1]/div[13]/button'))).click()
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="m_form"]/div[2]/div/div/div[2]/a[2]'))).click()

                    time.sleep(5)

                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="participant_list"]/div/div/div/div[3]/label[1]'))).click()
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="salvar"]'))).click()
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[5]/div/div[3]/button[1]'))).click()

                    quantidade += 1

                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[8]/div/div[3]/button[1]'))).click()

                    time.sleep(5)

                    data = datetime.datetime.now()
                    data_formatada = data.strftime('%H:%M:%S %d/%m/%y')

                    escrever_log(
                        f"Mensagem Contra Cheque enviado para {nome_colaborador} às {data_formatada}")

                    print(
                        f"Mensagem Contra Cheque enviado para {nome_colaborador} às {data_formatada}")

                except Exception as ex:
                    dataError = datetime.datetime.now()
                    dataError_formatada = dataError.strftime(
                        '%H:%M:%S %d/%m/%y')
                    # Em caso de outras exceções, escreve no log
                    escrever_erro(
                        f"ERRO: {str(ex)} durante o processamento do arquivo {nome_colaborador} às {dataError_formatada}")

                    print(
                        f"ERRO: {str(ex)} durante o processamento do arquivo {nome_colaborador} às {dataError_formatada}")
                    
                    continue
    driver.quit()        

# Chamada da função com os novos valores de login e senha
enviar_contracheques(login, senha, df_contatos)
