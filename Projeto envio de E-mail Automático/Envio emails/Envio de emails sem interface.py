import pandas as pd
import smtplib
import time
import os
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def ler_emails(planilha_path):
        # Lê os e-mails da planilha Excel
        df_emails = pd.read_excel(planilha_path)
        if 'E-mail' in df_emails.columns:
            tamanho_antes = len(df_emails)

            # Remove duplicatas mantendo apenas a primeira ocorrência
            df_sem_duplicatas = df_emails.drop_duplicates(
                subset=['E-mail'], keep='first')

            tamanho_depois = len(df_sem_duplicatas)

            if tamanho_antes != tamanho_depois:
                print(f"\nE-mails duplicados foram removidos! Agora são: {tamanho_depois}\n")
            else:
                emails = df_emails['E-mail'].tolist()
                print('\nNão há E-mails duplicados na planilha!\n')
                return emails, df_emails

            # Salva a planilha sem duplicatas
            df_sem_duplicatas.to_excel('Enviar E-mails.xlsx', index=False)

            # Retorna a lista de e-mails e o dataframe
            return df_sem_duplicatas['E-mail'].tolist(), df_sem_duplicatas
        else:
            emails = df_emails['E-mail'].tolist()
            print('\nNão há E-mails duplicados na planilha!\n')
            # Retorna a lista de e-mails e o dataframe
            return emails, df_emails
        

def escrever_envio(mensagem):
    arquivo_enviados = Path('enviados.txt')
    # Cria o arquivo se ele não existir
    if not arquivo_enviados.exists():
        arquivo_enviados.touch()
        
    # Escreve os logs no arquivo
    with open("enviados.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n")
            
            
def escrever_erro(mensagem):
    # Cria o arquivo se ele não existir
    arquivo_erros = Path('erros.txt')
    if not arquivo_erros.exists():
        arquivo_erros.touch()
            
    # Escreve os logs no arquivo
    with open("erros.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n")
        
        
def limpar_tela():
    # Verifica o sistema operacional para determinar o comando apropriado para limpar a tela, espera 3 segundos antes disso
    time.sleep(3)
    os.system('cls' if os.name == "nt" else "clear")


def enviar_email(destinatarios, planilha_path):
    # Configurações para o servidor SMTP do Gmail
    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587
    
    # Configurando email do remetente e senha
    email_remetente = 'fin.envios.3@gmail.com'
    senha = 'zljt edek hejb ohjv'
    
    titulo_html = 'teste'
    assunto = 'testando amigo'
    mensagem_html = 'teste opa'

    # Configuração inicial da mensagem comum a todos os e-mails
    corpo_email = f"""
<head>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                    width: 100%;
                }}
                h1 {{
                    color: #131A1D;
                    text-align: center;
                    padding-top: 30px;
                }}
                hr {{
                    margin: 20px;
                }}
                p {{
                    color: #131A1D;
                    text-align: justify;
                    font-size: 16px;
                }}
                button {{
                    all: unset;
                    width: 120px;
                    height: 50px;
                    background-color: #03738C;
                    border-radius: 10px;
                    text-align: center;
                    margin: auto;
                }}
                a {{
                    color: white;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 18px;
                }}
                .corpo_principal {{
                    background-color: #DFEDF2;
                    max-width: 500px; /* Largura máxima para controle de layout */
                    width: 90%; /* Definindo a largura em porcentagem para ser responsiva */
                    margin: 0 auto; /* Centralizar o elemento */
                    height: 500px; /* Altura fixa ou pode ser ajustada dinamicamente conforme necessário */
                    display: flex;
                    flex-direction: column;
                    padding: 10px;
                    border-radius: 10px;
                    justify-content: space-between;
                    box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.651);
                }}
            </style>
        </head>
            <div class="corpo_principal">
                <center>
                    <div>
                        <h1>{titulo_html}</h1>
                        <hr/>
                        <p>{mensagem_html}</p>
                    </div>
                </center>
            </div>
    """
    
    df_emails = pd.read_excel(planilha_path)
    status_coluna = 'STATUS'

    for i, email_destino in enumerate(destinatarios):
        # Cria uma nova mensagem para cada e-mail
        msg = MIMEMultipart()
        
        # Adiciona o corpo do e-mail
        corpo_mensagem = MIMEText(corpo_email, 'html')
        msg.attach(corpo_mensagem)

        # Configura o destinatário atual
        msg['To'] = email_destino
        msg['Subject'] = assunto  # Assunto do email
        msg['From'] = email_remetente # Substitua pelo seu endereço de e-mail do Outlook
        password = senha  # Substitua pela sua senha ou pela senha de aplicativo

        hora_atual = datetime.now()

        try:
            # Inicia a conexão SMTP e envia o e-mail
            with smtplib.SMTP(servidor_smtp, porta_smtp) as s:
                s.starttls()
                # Login Credentials for sending the mail
                s.login(msg['From'], password)
                s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            
            # Atualiza o status para 'SUCESSO'    
            df_emails.loc[df_emails['E-mail'] == email_destino, status_coluna] = 'SUCESSO'
            df_emails.to_excel('Enviar E-mails.xlsx', index=False)
            
            mensagem_de_envio = f'\nE-mail enviado para {email_destino} às {hora_atual.strftime("%H:%M:%S")}, com 30s de intervalo\n'
            escrever_envio(mensagem_de_envio)
            
            limpar_tela()
            
            print(mensagem_de_envio + f'\nEnviados: {i+1}')
            
        except Exception as e:
            # Se ocorrer um erro, imprima a mensagem de erro e atualize o status para 'ERRO'
            df_emails.loc[df_emails['E-mail'] == email_destino, status_coluna] = 'ERRO'
            df_emails.to_excel('Enviar E-mails.xlsx', index=False)
            
            mensagem_de_erro = f'\nErro ao enviar e-mail para {email_destino} ás {hora_atual.strftime("%H:%M:%S")}: {e}\n'
            escrever_erro(mensagem_de_erro)
            
            limpar_tela()
            
            print(mensagem_de_erro)
            
    time.sleep(30)

# Caminho da planilha com os e-mails
planilha_path = Path('Enviar E-mails.xlsx')

# Lê os e-mails da planilha
destinatarios, _ = ler_emails(planilha_path)

print('Iniciando envio de e-mails!')

# Envia e-mails para os destinatários
enviar_email(destinatarios, planilha_path)

print('Todos os e-mails enviados com sucesso!')