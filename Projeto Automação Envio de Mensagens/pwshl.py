import tkinter as tk
import customtkinter as ctk
import subprocess

def enviar_mensagem_servidor(mensagem):
   # Caminho do txt com todas as máquinas da rede
    path = r"C:\Users\suporte.2.WEBCERTIFICADOS\Desktop\Enviar mensagem rede\Users - Copia.txt"
    
    # Caminho do PsExec.exe
    filepath = r"C:\Users\suporte.2.WEBCERTIFICADOS\Downloads\PsExec.exe"
    
    # Criar script PowerShell dinamicamente
    script_powershell = fr"""
$computadores = Get-Content -Path "{path}"
$mensagem = "{mensagem}"

foreach ($computador in $computadores) {{
    $argumentos = @("\\$computador", "-s", "-i", "msg.exe", "/server:$computador", "*", "$mensagem")
    Start-Process -FilePath "{filepath}" -ArgumentList $argumentos -NoNewWindow -Wait
}}
"""

    # Executar script PowerShell
    try:
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", script_powershell], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar script PowerShell: {e}")
    finally:
        print('Todas as mensagens enviadas.')


def enviar_mensagem():
    mensagem = entry_mensagem.get("1.0", tk.END)
    
    # Aqui você pode adicionar a lógica para enviar a mensagem
    enviar_mensagem_servidor(mensagem)


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