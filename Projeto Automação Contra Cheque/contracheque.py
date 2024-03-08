# Adicione as bibliotecas necessárias para a automação web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
import pandas as pd
import os
import pyautogui
import glob
import datetime

url_site = 'https://assinarweb.com.br/arweb/login'

login = ''
senha = ''
diretorio_pdf = os.getcwd()
diretorio_pdf = diretorio_pdf + r'\PDF'
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
    nome = nome.strip() # Remover espaços extras no início e no final do nome
    extensao = '.pdf'

    caminho_completo = os.path.join(diretorio_pdf, f"{nome}{extensao}")

    print("\nArquivo PDF sendo procurado:", caminho_completo)

    if os.path.exists(caminho_completo):
        return caminho_completo
    else:
        return None


# Define a função para escrever no log
def escrever_log(mensagem):
    arquivo_enviados = Path('enviados.txt')
    # Cria o arquivo se ele não existir
    if not arquivo_enviados.exists():
        arquivo_enviados.touch()
        
    # Escreve os logs no arquivo
    with open("enviados.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n")


def escrever_erro(mensagem):
    arquivo_erros = Path('erros.txt')
    # Cria o arquivo se ele não existir
    if not arquivo_erros.exists():
        arquivo_erros.touch()
            
    # Escreve os logs no arquivo
    with open("erros.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n") 


def enviar_contracheques(login, senha, contatos):
    # Configurações do WebDriver do Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')

    # Configuração do caminho do driver do Chrome
    webdriver_path = './chrome/chromedriver.exe'

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
        for _ , row in contatos.iterrows():
            nome_colaborador = row["NOME"]
            print(f"\nProcessando: {nome_colaborador}")

            try:
                time.sleep(3)
                
                # Clique no botão Novo Documento
                element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div[1]/div[2]/div[1]/div[1]/a/div')))
                element.click()
                
                time.sleep(3)

                # Clique no botão Assinatura Digital
                element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="m_wizard_form_step_1"]/div/div[2]/div[2]/label')))
                element.click()
                
                time.sleep(3)

                # Abre a tela de seleção de arquivo no navegador
                element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="mDropzoneEnvelope"]')))
                element.click()
                
                time.sleep(3)

                # Encontra o caminho do arquivo PDF usando a função encontrar_pdf
                caminho_pdf = encontrar_pdf(nome_colaborador)

                print(f"\nCaminho do PDF para {nome_colaborador}: {caminho_pdf}")

                if caminho_pdf:
                        # Clique na caixa de diálogo para torná-la ativa
                        pyautogui.FAILSAFE = False

                        # Adicione um atraso de 3 segundos antes de escrever
                        time.sleep(3)

                        # Digite o caminho completo do arquivo usando pyautogui
                        pyautogui.write(caminho_pdf)

                        # Pressione Enter para confirmar a seleção
                        pyautogui.press('enter')

                        # Aguarde alguns segundos para o processo de seleção ser concluído
                        time.sleep(3)

                        # Clica no Botão Avançar
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="m_form"]/div[2]/div/div/div[2]/a[2]'))).click()

                        time.sleep(3)
                        
                        # Clica no botão Buscar Participante Cadastrado
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="m_wizard_form_step_2"]/div/button[2]'))).click()
                        
                        time.sleep(5)
                        
                        # Clica no botão Pesquisar
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="tblBuscarParticipantes_filter"]/label/input'))).click()
                        
                        time.sleep(3)
                        
                        # Pega o campo de filtro e armazena em uma variável
                        search_input = driver.find_element(
                            By.XPATH, '//*[@id="tblBuscarParticipantes_filter"]/label/input')
                        search_input.click()

                        # insere o nome na caixa de texto
                        search_input.send_keys(nome_colaborador)

                        # Pressiona Enter para executar a pesquisa
                        search_input.send_keys(Keys.RETURN)

                        # Aguarde a página carregar (ajuste conforme necessário)
                        time.sleep(3)
                        
                        # Pega o primeiro nome encontrado na coluna
                        nome_encontrado = WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="tblBuscarParticipantes"]/tbody/tr/td[2]'))).text
                        
                        time.sleep(3)
                        
                        # Verifica se o nome encontrado na tabela é diferente do nome do colaborador
                        if nome_encontrado.strip() != nome_colaborador:
                            print(f"\nO nome encontrado ({nome_encontrado}) é diferente do nome do colaborador ({nome_colaborador}). Pulando para o próximo colaborador.")
                            
                            # Clica no botão para fechar a tela de opção que está na frente da principal
                            WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                                        (By.XPATH, 'id("addParticipante")/DIV[1]/DIV[1]/DIV[1]/BUTTON[1]'))).click()
                            
                            time.sleep(3)
                            
                            # Clica na imagem da página e volta para página inicial
                            WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                                        (By.XPATH, '//*[@id="m_header"]/div[1]/div/div/div[1]/div/div[1]/a/img'))).click()
                            
                            time.sleep(3)
                            
                            continue
                        
                        # Clica no botão de ação
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, 'id("tblBuscarParticipantes")/TBODY[1]/TR[1]/TD[5]/A[1]'))).click()
                        
                        time.sleep(3)
                        
                        # Clica no botão adicionar
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, 'id("adicionarNovo")/DIV[1]/DIV[13]/BUTTON[1]'))).click()
                        
                        time.sleep(3)
                        
                        # Clica no botão avançar
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="m_form"]/div[2]/div/div/div[2]/a[2]'))).click()

                        time.sleep(5)

                        # Clica no botão de colocar assinatura no arquivo
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="participant_list"]/div/div/div/div[3]/label[1]/span'))).click()
                        
                        time.sleep(3)
                        
                        # Clica em salvar o arquivo
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="salvar"]'))).click()

                        time.sleep(5)
                        
                        # Clica em publicar o arquivo
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '/html/body/div[5]/div/div[3]/button[1]'))).click()

                        time.sleep(5)

                        quantidade += 1

                        # Clica na imagem da página e volta para página inicial
                        WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="m_header"]/div[1]/div/div/div[1]/div/div[1]/a/img'))).click()

                        data = datetime.datetime.now()
                        data_formatada = data.strftime('%H:%M:%S %d/%m/%y')

                        escrever_log(
                            str(f"Mensagem Contra Cheque enviado para {nome_colaborador} às {data_formatada}"))
                        
                else:
                    # Se o arquivo não foi encontrado, escreva no log de erros e continue para o próximo colaborador
                    dataError = datetime.datetime.now()
                    dataError_formatada = dataError.strftime('%H:%M:%S %d/%m/%y')
                    escrever_erro(
                        str(f"ERRO: Arquivo não encontrado para {nome_colaborador} às {dataError_formatada}"))
                    
                    # Se ocorrer um erro, feche a janela de seleção de arquivo
                    pyautogui.hotkey('esc')
                    
                    time.sleep(3)
                    
                    # Clica na imagem da página e volta para página inicial
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="m_header"]/div[1]/div/div/div[1]/div/div[1]/a/img'))).click()
                    
                    time.sleep(3)
                    
                    # Continue para o próximo colaborador mesmo em caso de erro
                    continue
        
            except Exception as e:
                # Em caso de outras exceções, escreve no log
                dataError = datetime.datetime.now()
                dataError_formatada = dataError.strftime(
                        '%H:%M:%S %d/%m/%y')
                escrever_erro(
                    str(f"ERRO ao Processar: durante o processamento do arquivo {nome_colaborador} às {dataError_formatada}"))
                
                # Clica na imagem da página e volta para página inicial
                WebDriverWait(driver, 15).until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="m_header"]/div[1]/div/div/div[1]/div/div[1]/a/img'))).click()
                
                time.sleep(3)
                
                # Continue para o próximo colaborador mesmo em caso de erro
                continue


# Exemplo de uso
try:
    planilha_path = './Gestão de Funcionários 2023.xlsx'
    coluna_nome = 'NOME'

    if not os.path.exists(planilha_path):
        raise FileNotFoundError(
            f"Arquivo da planilha não encontrado: {planilha_path}")

    df_contatos = ler_planilha(planilha_path, coluna_nome)

    # Agora você tem um DataFrame contendo as colunas 'NOME' e 'ARQUIVOS' sem valores nulos
    print(df_contatos)
except Exception as e:
    print(f"Erro: {str(e)}")

# Chamada da função com os novos valores de login e senha
enviar_contracheques(login, senha, df_contatos)

print("\nContracheques enviados!!!\n")