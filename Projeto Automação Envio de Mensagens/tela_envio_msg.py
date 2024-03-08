import tkinter as tk
import customtkinter as ctk
import threading
import subprocess
import powershell_script

# Define entry_mensagem como uma variável global
entry_mensagem = None

def enviar_mensagem_servidor(mensagem):
    script_powershell = powershell_script.generate_powershell_script(mensagem)

    # Executar script PowerShell
    def run_powershell_script():
        try:
            subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", script_powershell], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar script PowerShell: {e}")
        finally:
            print('Mensagens enviadas.')
            
    powershell_thread = threading.Thread(target=run_powershell_script)
    powershell_thread.start()


def enviar_mensagem():
    global entry_mensagem
    
    mensagem = entry_mensagem.get("1.0", tk.END)
    
    enviar_mensagem_servidor(mensagem)


def gerar_janela():
    global entry_mensagem
    
    # Interface Gráfica
    root = ctk.CTk()
    root.title('Enviar Mensagem para Todos')

    # Campo de entrada para a mensagem
    label_mensagem = ctk.CTkLabel(root, text='Mensagem:')
    label_mensagem.pack(pady=5)

    entry_mensagem = ctk.CTkTextbox(root)
    entry_mensagem.pack(padx=5, pady=5)

    # Botão para enviar a mensagem
    enviar_button = ctk.CTkButton(root, text='Enviar', command=enviar_mensagem)
    enviar_button.pack(pady=10)

    # Definir tamanho da janela
    largura_janela = 325
    altura_janela = 300
    posicao_x = (root.winfo_screenwidth() - largura_janela) // 2
    posicao_y = (root.winfo_screenheight() - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

    root.mainloop()
    
def start_gui():
    gui_thread = threading.Thread(target=gerar_janela)
    gui_thread.start()
    
if __name__ == "__main__":
    start_gui()