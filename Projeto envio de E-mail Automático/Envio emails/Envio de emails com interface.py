import sys
import pandas as pd
import smtplib
import webbrowser
import json
import atexit
import os
import time
from styles import *
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout, 
    QFileDialog, 
    QMessageBox, 
    QTextEdit, 
    QDesktopWidget, 
    QCheckBox,
    )
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QIcon, QIntValidator


# Definindo variável de hora atual
hora_atual = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Define a função para escrever no log de enviados
def escrever_envio(mensagem):
    arquivo_enviados = Path('enviados.txt')
    # Cria o arquivo se ele não existir
    if not arquivo_enviados.exists():
        arquivo_enviados.touch()
        
    # Escreve os logs no arquivo
    with open("enviados.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n")
            
# Define a função para escrever no log de erros
def escrever_erro(mensagem):
    # Cria o arquivo se ele não existir
    arquivo_erros = Path('erros.txt')
    if not arquivo_erros.exists():
        arquivo_erros.touch()
            
    # Escreve os logs no arquivo
    with open("erros.txt", "a") as log_file:
        log_file.write(f"{mensagem}\n")

# Função para limpar a tela do console
def limpar_tela():
    # Verifica o sistema operacional para determinar o comando apropriado para limpar a tela, espera 2 segundos antes disso
    time.sleep(2)
    os.system('cls' if os.name == "nt" else "clear")

class EmailSenderThread(QThread):
    
    """Classe responsável pelo envio dos e-mails.

    Args:
        remetente: E-mail do remetente.
        senha: Senha do e-mail do remetente.
        destinatarios: Lista de e-mails dos destinatários.
        df_emails: DataFrame com os dados dos e-mails, incluindo o status do envio.
        assunto: Assunto do e-mail.
        titulo_html: Título do e-mail em HTML.
        mensagem_html: Mensagem do e-mail em HTML.
    """
    
    # Sinais para comunicação entre threads e atualização da interface gráfica
    update_status_signal = pyqtSignal(str)
    update_progress_signal = pyqtSignal(int)


    def __init__(self, remetente, senha, destinatarios, df_emails, assunto, titulo_html, mensagem_html, intervalo_envio):
        super().__init__()
        # Parâmetros para o envio de e-mails
        self.remetente = remetente
        self.senha = senha
        self.destinatarios = destinatarios
        self.df_emails = df_emails
        self.assunto = assunto
        self.titulo_html = titulo_html
        self.mensagem_html = mensagem_html
        self.intervalo_envio = intervalo_envio


    def run(self):
        # Utilizando a variável global hora_atual
        global hora_atual 
        
        # Configurações do servidor SMTP
        servidor_smtp = 'smtp.gmail.com'
        porta_smtp = 587

        # Corpo do e-mail em formato HTML
        corpo_email = f"""
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
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
                    color: #ffffff;
                    text-align: center;
                    padding-top: 30px;
                }}
                hr {{
                    margin: 20px;
                }}
                p {{
                    color: #ffffff;
                    text-align: center;
                }}
                .corpo_principal {{
                    background-color: #333;
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
        <body>
            <div class="corpo_principal">
            <div>
                <h1>{self.titulo_html}</h1>
                <hr/>
                <p>{self.mensagem_html}</p>
            </div>
            </div>
        </body>
        </html>
        """

        # Nome da coluna que armazenará o status do envio na planilha
        status_coluna = 'STATUS'

        # Itera sobre os destinatários para enviar os e-mails
        for i, email_destino in enumerate(self.destinatarios):

            # Configuração do e-mail
            msg = MIMEMultipart()
            corpo_mensagem = MIMEText(corpo_email, 'html')
            msg.attach(corpo_mensagem)
            msg['To'] = email_destino
            msg['Subject'] = self.assunto
            msg['From'] = self.remetente
            password = self.senha

            hora_atual = datetime.now()

            try:
                # Tenta enviar o e-mail
                with smtplib.SMTP(servidor_smtp, porta_smtp) as s:
                    s.starttls()
                    s.login(msg['From'], password)
                    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

                # Atualiza a planilha e emite sinal de sucesso
                self.df_emails.loc[self.df_emails['E-mail'] == email_destino, status_coluna] = 'SUCESSO'
                self.df_emails.to_excel('Enviar E-mails.xlsx', index=False)
                mensagem_de_envio = f'\nE-mail enviado para {email_destino} às {hora_atual.strftime("%H:%M:%S")}, com {self.intervalo_envio}s de intervalo\n'
                escrever_envio(mensagem_de_envio)
                self.update_status_signal.emit(mensagem_de_envio)
                limpar_tela()

            except Exception as e:
                # Em caso de erro, atualiza a planilha e emite sinal de erro
                self.df_emails.loc[self.df_emails['E-mail'] == email_destino, status_coluna] = 'ERRO'
                mensagem_de_erro = f'\nErro ao enviar e-mail para {email_destino} ás {hora_atual.strftime("%H:%M:%S")}: {e}\n'
                escrever_erro(mensagem_de_erro)
                print(mensagem_de_erro)
                self.df_emails.to_excel('Enviar E-mails.xlsx', index=False)
                limpar_tela()

            # Pausa por 30 segundos antes de enviar o próximo e-mail
            self.msleep(self.intervalo_envio * 1000)

            # Atualiza o progresso
            progress = int((i + 1) / len(self.destinatarios) * 100)
            self.update_progress_signal.emit(progress)


class EmailSenderApp(QWidget):
    
    """Classe principal da aplicação.

    Responsavel por gerenciar a interface gráfica e o envio dos e-mails.
    """
    
    def __init__(self):
        """Inicializa a interface gráfica.

        Define o título, a posição e o layout da janela.
        Cria e configura os widgets da interface gráfica.
        """
        
        super().__init__()

        self.init_ui(styleMain)
        
        # Garante que o arquivo de credenciais exista
        self.verificar_arquivo_credenciais()
        
        # Carrega as credenciais salvas, se houver
        email_salvo, senha_salva = self.carregar_credenciais()
        self.email_remetente_edit.setText(email_salvo)
        self.senha_edit.setText(senha_salva)
          
        # Conectar o evento de fechamento ao método que salva as credenciais
        atexit.register(self.salvar_credenciais_on_exit)


    def init_ui(self, styleMain):
        # Define o título da janela
        self.setWindowTitle('Enviar E-mails')
        # Define o estilo CSS da janela
        self.setStyleSheet(styleMain)
        # Desabilita o o botão de maximizar a tela
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # Define o tamanho da janela
        self.setGeometry(100, 100, 400, 300)

        self.email_remetente_label = QLabel('E-mail Remetente: (Utilize um email do Google)')  # Cria um rótulo para o campo de e-mail
        self.email_remetente_edit = QLineEdit()  # Cria um campo de entrada para o e-mail

        self.senha_label = QLabel('Senha:')  # Cria um rótulo para o campo de senha
        self.senha_edit = QLineEdit()  # Cria um campo de entrada para a senha
        self.senha_edit.setEchoMode(QLineEdit.Password)  # Configura o campo de senha para ocultar a entrada

        self.show_password_button = QCheckBox('Mostrar Senha')  # Cria um botão de seleção para mostrar a senha
        self.show_password_button.stateChanged.connect(self.toggle_echo_mode)  # Conecta o botão de seleção a uma função para alternar a visibilidade da senha

        self.planilha_path_label = QLabel('Escolha a Planilha:')  # Cria um rótulo para o campo de caminho da planilha
        self.planilha_path_edit = QLineEdit()  # Cria um campo de entrada para o caminho da planilha
        self.planilha_path_edit.setReadOnly(True)  # Configura o campo de caminho da planilha para ser somente leitura
        self.planilha_path_edit.setPlaceholderText('.xlsx')  # Define um texto de espaço reservado para o campo de caminho da planilha

        self.choose_planilha_button = QPushButton('Escolher')  # Cria um botão para escolher a planilha
        self.baixar_planilha = QPushButton('Baixar Planilha Base')  # Cria um botão para baixar a planilha base
        self.baixar_planilha.clicked.connect(self.baixar_planilha_base)  # Conecta o botão de download a uma função para baixar a planilha base

        self.numero_envios_label = QLabel('Número de Envios:')  # Cria um rótulo para o campo de número de envios
        self.numero_envios_edit = QLineEdit()  # Cria um campo de entrada para o número de envios
        self.numero_envios_edit.setMaxLength(3)  # Define o comprimento máximo do campo de número de envios
        self.numero_envios_edit.setValidator(QIntValidator())  # Define um validador para permitir apenas números inteiros
        self.numero_envios_edit.setPlaceholderText('Nº')  # Define um texto de espaço reservado para o campo de número de envios

        self.intervalo_envio_label = QLabel('Intervalo entre Envios (segundos):')  # Cria um rótulo para o campo de intervalo entre envios
        self.intervalo_envio_edit = QLineEdit()  # Cria um campo de entrada para o intervalo entre envios
        self.intervalo_envio_edit.setPlaceholderText('30')  # Define um texto de espaço reservado para o campo de intervalo entre envios
        self.intervalo_envio_edit.setValidator(QIntValidator(30, 9999))  # Define um validador para permitir apenas números inteiros maiores ou iguais a 30

        self.assunto_label = QLabel('Assunto:')  # Cria um rótulo para o campo de assunto
        self.assunto_edit = QLineEdit()  # Cria um campo de entrada para o assunto
        self.assunto_edit.setPlaceholderText('Assunto do E-mail')  # Define um texto de espaço reservado para o campo de assunto

        self.titulo_html_label = QLabel('Título:')  # Cria um rótulo para o campo de título
        self.titulo_html_edit = QLineEdit()  # Cria um campo de entrada para o título
        self.titulo_html_edit.setPlaceholderText('Título do E-mail')  # Define um texto de espaço reservado para o campo de título

        self.mensagem_html_label = QLabel('Mensagem:')  # Cria um rótulo para o campo de mensagem
        self.mensagem_html_edit = QTextEdit()  # Cria um campo de entrada para a mensagem
        self.mensagem_html_edit.setPlaceholderText('Mensagem principal do E-mail')  # Define um texto de espaço reservado para o campo de mensagem

        self.iniciar_button = QPushButton('Iniciar Envio')  # Cria um botão para iniciar o envio
        self.iniciar_button.setStyleSheet(f'background-color: {cor_azul_escuro}')  # Define o estilo do botão de início

        # Layout
        layout = QVBoxLayout()  # Cria um layout vertical
        layout.addWidget(self.email_remetente_label)  # Adiciona o rótulo de e-mail ao layout
        layout.addWidget(self.email_remetente_edit)  # Adiciona o campo de e-mail ao layout

        layout.addWidget(self.senha_label)  # Adiciona o rótulo de senha ao layout
        layout.addWidget(self.senha_edit)  # Adiciona o campo de senha ao layout

        layout.addWidget(self.show_password_button)  # Adiciona o botão de seleção de mostrar senha ao layout

        layout.addWidget(self.planilha_path_label)  # Adiciona o rótulo de caminho da planilha ao layout
        layout.addWidget(self.planilha_path_edit)  # Adiciona o campo de caminho da planilha ao layout
        layout.addWidget(self.choose_planilha_button)  # Adiciona o botão de escolha da planilha ao layout
        layout.addWidget(self.baixar_planilha)  # Adiciona o botão de download da planilha ao layout

        layout.addWidget(self.numero_envios_label)  # Adiciona o rótulo de número de envios ao layout
        layout.addWidget(self.numero_envios_edit)  # Adiciona o campo de número de envios ao layout

        # Adiciona widgets relacionados ao intervalo entre envios ao layout
        layout.addWidget(self.intervalo_envio_label)
        layout.addWidget(self.intervalo_envio_edit)

        layout.addWidget(self.assunto_label)  # Adiciona o rótulo de assunto ao layout
        layout.addWidget(self.assunto_edit)  # Adiciona o campo de assunto ao layout

        layout.addWidget(self.titulo_html_label)  # Adiciona o rótulo de título ao layout
        layout.addWidget(self.titulo_html_edit)  # Adiciona o campo de título ao layout

        layout.addWidget(self.mensagem_html_label)  # Adiciona o rótulo de mensagem ao layout
        layout.addWidget(self.mensagem_html_edit)  # Adiciona o campo de mensagem ao layout

        layout.addWidget(self.iniciar_button)  # Adiciona o botão de início ao layout

        self.setLayout(layout)

        # Conectar sinais a slots
        self.choose_planilha_button.clicked.connect(self.choose_planilha)
        self.iniciar_button.clicked.connect(self.iniciar_envio)

        self.show()
        
        self.center_window()
        
        
    def center_window(self):
        # Obtém a geometria da tela principal
        screen = QDesktopWidget().screenGeometry()

        # Obtém a geometria da própria janela
        window = self.geometry()

        # Calcula a posição x e y para centralizar a janela
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # Define a posição da janela para centralizá-la
        self.move(x, y)
    
    def toggle_echo_mode(self, state):
        # Alterna entre mostrar ou ocultar caracteres na entrada de senha com base no estado da caixa de seleção
        if state == Qt.Checked:
            # Se a caixa de seleção estiver marcada, mostra os caracteres
            self.senha_edit.setEchoMode(QLineEdit.Normal)
        else:
            # Se a caixa de seleção não estiver marcada, oculta os caracteres
            self.senha_edit.setEchoMode(QLineEdit.Password)
    
    
    def iniciar_envio(self):
        # Verificar se todos os campos estão preenchidos
        if not self.campos_preenchidos():
            return
        
        # Utilizando a variável global hora_atual
        global hora_atual 
        
        hora_atual = datetime.now()
        
        print(f'Iniciando envio de e-mails às {hora_atual.strftime("%H:%M:%S")}')
            
        QMessageBox.information(self, 'Envio Iniciado', 'Começando envio de e-mails')

        self.set_widgets_enabled(False)

        planilha_path = Path(self.planilha_path_edit.text())
        numero_envios = int(self.numero_envios_edit.text())
        # Obtenha o intervalo entre envios do campo de entrada e defina 30 como padrão
        intervalo_envio = int(self.intervalo_envio_edit.text() or '30')
        assunto = self.assunto_edit.text()
        titulo_html = self.titulo_html_edit.text()
        mensagem_html = self.mensagem_html_edit.toPlainText()
        remetente = self.email_remetente_edit.text()
        senha = self.senha_edit.text()

        # Verifica se o intervalo de envio é menor que 30 segundos
        if intervalo_envio < 30:
            QMessageBox.warning(self, 'Valor Inválido', 'O intervalo entre envios deve ser no mínimo 30 segundos.')
            self.set_widgets_enabled(True)
            return

        # Substitui quebras de linha por <br> no HTML da mensagem
        mensagem_html = mensagem_html.replace('\n', '<br>')

        destinatarios, df_emails = self.ler_emails(planilha_path)

        self.email_sender_thread = EmailSenderThread(remetente, senha, destinatarios, df_emails, assunto, titulo_html, mensagem_html, intervalo_envio)
        self.email_sender_thread.update_status_signal.connect(self.atualizar_status)
        self.email_sender_thread.update_progress_signal.connect(self.atualizar_progresso)
        
        # Configura um temporizador para iniciar o envio após o intervalo definido
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.email_sender_thread.start)
        
        # Inicia o envio imediatamente
        self.email_sender_thread.start()

    
    def closeEvent(self, event):
        # Chamado quando o aplicativo é fechado
        self.salvar_credenciais_on_exit()
        event.accept()


    def campos_preenchidos(self):
        # Lista de campos a serem verificados
        campos = [
            ('E-mail Remetente', self.email_remetente_edit.text()),
            ('Senha', self.senha_edit.text()),
            ('Caminho da Planilha', self.planilha_path_edit.text()),
            ('Número de Envios', self.numero_envios_edit.text()),
            ('Assunto', self.assunto_edit.text()),
            ('Título', self.titulo_html_edit.text()),
            ('Mensagem', self.mensagem_html_edit.toPlainText())
        ]

        # Itera sobre os campos
        for nome_campo, valor_campo in campos:
            if not valor_campo:
                # Exibe uma mensagem de erro se algum campo estiver vazio
                QMessageBox.warning(self, f'{nome_campo} Vazio', f'Por favor, preencha o campo {nome_campo}.')
                return False
        
        # Verifica se os campos de e-mail e senha estão preenchidos
        if not self.email_remetente_edit.text() or not self.senha_edit.text():
            # Retorna False e exibe uma mensagem de erro se algum campo estiver vazio
            QMessageBox.warning(self, 'Campos Vazios', 'Por favor, preencha o e-mail remetente e a senha.')
            return False

        # Verifica se o e-mail inserido é válido (contém '@' e '.com')
        if '@' not in self.email_remetente_edit.text() or '.com' not in self.email_remetente_edit.text():
            # Retorna False e exibe uma mensagem de erro se o e-mail for inválido
            QMessageBox.warning(self, 'E-mail Inválido', 'Por favor, digite um e-mail válido.')
            return False

        # Retorna True se todos os campos estiverem preenchidos corretamente
        return True


    def atualizar_status(self, status):
        # Imprime o status atual
        print(status)


    def atualizar_progresso(self, progresso):
        # Utilizando a variável global hora_atual
        global hora_atual 
        
        # Atualiza e imprime o progresso atual
        print(f'Progresso: {progresso}%')
        
        hora_atual = datetime.now()

        # Se o progresso for 100%, imprime uma mensagem de conclusão
        if progresso == 100:
            limpar_tela()
            # Exibe uma mensagem de informação indicando que todos os e-mails foram enviados
            print(f'\nEnvio de e-mails concluído às {hora_atual.strftime("%H:%M:%S")}!\n')

            QMessageBox.information(self, 'Envio Concluído', 'Todos os e-mails foram enviados com sucesso!')

            # Desconecta o temporizador quando o envio é concluído
            self.timer.timeout.disconnect(self.email_sender_thread.start)

            # Desconecta o temporizador e habilita os widgets
            self.set_widgets_enabled(True)


    def set_widgets_enabled(self, enabled):
        # Desabilita ou habilita os widgets com base no parâmetro 'enabled'
        lista_desabilitar_ou_habilitar = [
        self.email_remetente_edit,
        self.baixar_planilha,
        self.senha_edit,
        self.show_password_button,
        self.planilha_path_edit,
        self.choose_planilha_button,
        self.numero_envios_edit,
        self.assunto_edit,
        self.titulo_html_edit,
        self.iniciar_button,
        self.mensagem_html_edit,
        self.intervalo_envio_edit,
        ]
        
        for index, item in enumerate(lista_desabilitar_ou_habilitar):
            item.setEnabled(enabled)
            
        
    def choose_planilha(self):
        # Abre um diálogo para escolher a planilha
        planilha_path, _ = QFileDialog.getOpenFileName(self, 'Escolher Planilha', '', 'Excel Files (*.xlsx *.xls)')
        if planilha_path:
            self.planilha_path_edit.setText(planilha_path)


    def ler_emails(self, planilha_path):
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
       
        
    def baixar_planilha_base(self):
        # Abre o Google para baixar a planilha base através do link de download direto
        webbrowser.open(
            "https://www.dropbox.com/scl/fi/86uil93uepe3sssd7yxm8/Enviar-E-mails.xlsx?rlkey=inogq1zqcm3xjame930yksm75&dl=1"
        )
       
        
    def verificar_arquivo_credenciais(self):
        # Verifica se o arquivo de credenciais existe, senão, cria um novo
        path_credenciais = Path(resource_path('credenciais.json'))
        if not path_credenciais.exists():
            path_credenciais.touch()    
        
        
    def salvar_credenciais(self, email, senha):
        # Salva as credenciais fornecidas em um arquivo json
        credenciais = {'email': email, 'senha': senha}
        with open(resource_path('credenciais.json'), 'w') as arquivo:
            json.dump(credenciais, arquivo)
        
            
    def salvar_credenciais_on_exit(self):
        # Salva as credenciais quando o aplicativo é fechado
        self.salvar_credenciais(self.email_remetente_edit.text(), self.senha_edit.text())
        
        
    def carregar_credenciais(self):
        try:
            # Tenta abrir o arquivo 'credenciais.json' no modo de leitura
            with open(resource_path('credenciais.json'), 'r') as arquivo:
                # Carrega as credenciais do arquivo json
                credenciais = json.load(arquivo)
                # Retorna o e-mail e a senha armazenados nas credenciais
                return credenciais.get('email', ''), credenciais.get('senha', '')
            
        # Se o arquivo não for encontrado ou se houver um erro ao decodificar o json
        except FileNotFoundError:
            print("Arquivo 'credenciais.json' não encontrado.")
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON 'credenciais.json'. Verifique se o formato do arquivo está correto.")
        except Exception as e:
            print(f"Erro ao carregar as credenciais: {e}")
            
        # retorna uma string vazia para o e-mail e a senha
        return '', ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Crie um ícone usando o caminho para o seu arquivo de ícone
    app_icon = QIcon(str(resource_path("icon.ico")))
    
    # Defina o ícone da aplicação
    app.setWindowIcon(app_icon)
    
    # Cria uma instância da janela de login (LoginWindow)
    main_window = EmailSenderApp()
    # Define o ícone da janela como o ícone da aplicação
    main_window.setWindowIcon(app_icon)
    # Exibe a janela de login
    main_window.show()
    
    sys.exit(app.exec_())