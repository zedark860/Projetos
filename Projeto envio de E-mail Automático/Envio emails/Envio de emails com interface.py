import sys
import pandas as pd
import smtplib
import webbrowser
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
    QCheckBox
    )
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIntValidator
from pathlib import Path

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
    envio_interrompido_signal = pyqtSignal(bool)

    def __init__(self, remetente, senha, destinatarios, df_emails, assunto, titulo_html, mensagem_html):
        super().__init__()
        # Parâmetros para o envio de e-mails
        self.remetente = remetente
        self.senha = senha
        self.destinatarios = destinatarios
        self.df_emails = df_emails
        self.assunto = assunto
        self.titulo_html = titulo_html
        self.mensagem_html = mensagem_html

    def run(self):
        # Configurações do servidor SMTP
        servidor_smtp = 'smtp.office365.com'
        porta_smtp = 587

        # Corpo do e-mail em formato HTML
        corpo_email = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <h1>{self.titulo_html}</h1>
            <p>{self.mensagem_html}</p>
        </body>
        </html>
        """

        # Nome da coluna que armazenará o status do envio na planilha
        status_coluna = 'STATUS'

        # Itera sobre os destinatários para enviar os e-mails
        for i, email_destino in enumerate(self.destinatarios):
            # Verifica se o envio foi interrompido
            if self.envio_interrompido_signal.emit(False):  # Verifica se o envio foi interrompido
                self.update_status_signal.emit('Envio interrompido pelo usuário.')
                break

            # Configuração do e-mail
            msg = MIMEMultipart()
            corpo_mensagem = MIMEText(corpo_email, 'html')
            msg.attach(corpo_mensagem)
            msg['To'] = email_destino
            msg['Subject'] = self.assunto
            msg['From'] = self.remetente
            password = self.senha

            try:
                # Tenta enviar o e-mail
                with smtplib.SMTP(servidor_smtp, porta_smtp) as s:
                    s.starttls()
                    s.login(msg['From'], password)
                    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

                # Atualiza a planilha e emite sinal de sucesso
                self.df_emails.loc[self.df_emails['E-mail'] == email_destino, status_coluna] = 'SUCESSO'
                self.df_emails.to_excel('Enviar E-mails.xlsx', index=False)
                self.update_status_signal.emit(f'E-mail enviado para {email_destino}')

            except Exception as e:
                # Em caso de erro, atualiza a planilha e emite sinal de erro
                self.df_emails.loc[self.df_emails['E-mail'] == email_destino, status_coluna] = 'ERRO'
                self.df_emails.to_excel('Enviar E-mails.xlsx', index=False)
                self.update_status_signal.emit(f'Erro ao enviar e-mail para {email_destino}: {e}')

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

        self.envio_interrompido = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Enviar E-mails App')
        self.setGeometry(100, 100, 400, 300)

        # Campos e widgets
        self.email_remetente_label = QLabel('E-mail Remetente: (Utilize um email do outlook)')
        self.email_remetente_edit = QLineEdit()

        self.senha_label = QLabel('Senha:')
        self.senha_edit = QLineEdit()
        self.senha_edit.setEchoMode(QLineEdit.Password)
        
        self.show_password_button = QCheckBox('Mostrar Senha')
        self.show_password_button.stateChanged.connect(self.toggle_echo_mode)

        self.planilha_path_label = QLabel('Escolha a Planilha:')
        self.planilha_path_edit = QLineEdit()
        self.planilha_path_edit.setReadOnly(True)
        
        self.choose_planilha_button = QPushButton('Escolher')
        self.baixar_planilha = QPushButton('Baixar Planilha Base')
        self.baixar_planilha.clicked.connect(self.baixar_planilha_base)

        self.numero_envios_label = QLabel('Número de Envios:')
        self.numero_envios_edit = QLineEdit()
        self.numero_envios_edit.setMaxLength(3)
        self.numero_envios_edit.setValidator(QIntValidator())

        self.assunto_label = QLabel('Assunto:')
        self.assunto_edit = QLineEdit()

        self.titulo_html_label = QLabel('Título HTML (h1):')
        self.titulo_html_edit = QLineEdit()

        self.mensagem_html_label = QLabel('Mensagem HTML (p):')
        self.mensagem_html_edit = QTextEdit()

        self.iniciar_button = QPushButton('Iniciar Envio')
        self.parar_button = QPushButton('Parar Envio')
        self.parar_button.clicked.connect(self.confirmar_parada_envio)
        self.parar_button.setEnabled(False)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.email_remetente_label)
        layout.addWidget(self.email_remetente_edit)

        layout.addWidget(self.senha_label)
        layout.addWidget(self.senha_edit)
        
        layout.addWidget(self.show_password_button)

        layout.addWidget(self.planilha_path_label)
        layout.addWidget(self.planilha_path_edit)
        layout.addWidget(self.choose_planilha_button)
        layout.addWidget(self.baixar_planilha)

        layout.addWidget(self.numero_envios_label)
        layout.addWidget(self.numero_envios_edit)

        layout.addWidget(self.assunto_label)
        layout.addWidget(self.assunto_edit)

        layout.addWidget(self.titulo_html_label)
        layout.addWidget(self.titulo_html_edit)

        layout.addWidget(self.mensagem_html_label)
        layout.addWidget(self.mensagem_html_edit)

        layout.addWidget(self.iniciar_button)
        layout.addWidget(self.parar_button)

        self.setLayout(layout)

        # Conectar sinais a slots
        self.choose_planilha_button.clicked.connect(self.choose_planilha)
        self.iniciar_button.clicked.connect(self.iniciar_envio)
        self.parar_button.clicked.connect(self.parar_envio)

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
        
        print('Iniciando envio de e-mails!')
            
        QMessageBox.information(self, 'Envio Iniciado', 'Começando envio de e-mails')

        self.set_widgets_enabled(False)

        planilha_path = Path(self.planilha_path_edit.text())
        numero_envios = int(self.numero_envios_edit.text())
        assunto = self.assunto_edit.text()
        titulo_html = self.titulo_html_edit.text()
        mensagem_html = self.mensagem_html_edit.toPlainText()
        remetente = self.email_remetente_edit.text()
        senha = self.senha_edit.text()

        destinatarios, df_emails = self.ler_emails(planilha_path)

        self.email_sender_thread = EmailSenderThread(remetente, senha, destinatarios, df_emails, assunto, titulo_html, mensagem_html)
        self.email_sender_thread.update_status_signal.connect(self.atualizar_status)
        self.email_sender_thread.update_progress_signal.connect(self.atualizar_progresso)

        self.email_sender_thread.start()

    def campos_preenchidos(self):
        if not self.email_remetente_edit.text() or not self.senha_edit.text():
            QMessageBox.warning(self, 'Campos Vazios', 'Por favor, preencha o e-mail remetente e a senha.')
            return False

        if '@' not in self.email_remetente_edit.text() or '.com' not in self.email_remetente_edit.text():
            QMessageBox.warning(self, 'E-mail Inválido', 'Por favor, digite um e-mail válido.')
            return False

        return True

    def atualizar_status(self, status):
        print(status)

    def atualizar_progresso(self, progresso):
        print(f'Progresso: {progresso}%')
        
        if progresso == 100:
            print('Envio de e-mails concluído!')

            QMessageBox.information(self, 'Envio Concluído', 'Todos os e-mails foram enviados com sucesso!')

            self.set_widgets_enabled(True)

    def confirmar_parada_envio(self):
        reply = QMessageBox.question(self, 'Confirmação', 'Deseja realmente parar o envio de e-mails?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.parar_envio()

    def parar_envio(self):
        # Aguarda o término do thread secundário antes de emitir o sinal
        if hasattr(self, 'email_sender_thread') and self.email_sender_thread.isRunning():
            self.email_sender_thread.wait()

        self.email_sender_thread.envio_interrompido_signal.emit(True)
        QMessageBox.information(self, 'Envio Interrompido', 'O envio de e-mails foi interrompido.')

        print('Parando envio de e-mails...')

        self.set_widgets_enabled(True)

    def set_widgets_enabled(self, enabled):
        # Desabilita ou habilita os widgets com base no parâmetro 'enabled'
        self.email_remetente_edit.setEnabled(enabled)
        self.senha_edit.setEnabled(enabled)
        self.planilha_path_edit.setEnabled(enabled)
        self.choose_planilha_button.setEnabled(enabled)
        self.numero_envios_edit.setEnabled(enabled)
        self.assunto_edit.setEnabled(enabled)
        self.titulo_html_edit.setEnabled(enabled)
        self.mensagem_html_edit.setEnabled(enabled)
        self.iniciar_button.setEnabled(enabled)
        self.parar_button.setEnabled(not enabled)

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
                print('Não há E-mails duplicados na planilha!')
                return emails, df_emails

            # Salva a planilha sem duplicatas
            df_sem_duplicatas.to_excel('Enviar E-mails.xlsx', index=False)

            return df_sem_duplicatas['E-mail'].tolist(), df_sem_duplicatas
        else:
            emails = df_emails['E-mail'].tolist()
            print('Não há E-mails duplicados na planilha!')
            return emails, df_emails
        
    def baixar_planilha_base(self):
        # Abre o Google para baixar a planilha base através do link de download direto
        webbrowser.open(
            ""
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmailSenderApp()
    sys.exit(app.exec_())
