import git
import os
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import time
import shutil

# Definindo as variáveis repo_url e pasta_destino no escopo global
repo_url = ""
pasta_destino = os.path.join(os.getcwd(), "Atualizador")  # Pasta onde o programa está instalado localmente
progresso_da_barra_label = None

def atualizar_programa(repo_url, pasta_destino):
    try:
        if os.path.exists(pasta_destino):
            repo = git.Repo(pasta_destino)
            origin = repo.remotes.origin
            origin.fetch()
            origin.pull()

            mudancas = repo.index.diff(None)
            if mudancas:
                for arquivo_modificado in mudancas:
                    caminho_arquivo = os.path.join(pasta_destino, arquivo_modificado.a_blob.path)
                    if os.path.exists(caminho_arquivo):
                        shutil.copy(arquivo_modificado.a_blob.path, pasta_destino)
                        print(f"Arquivo baixado: {arquivo_modificado.a_blob.path}")
            else:
                return "O programa já está atualizado."
        else:
            return "Instale o programa para atualizar!"
    except Exception as e:
        return f"Ocorreu um erro durante a atualização: {str(e)}"

def verificar_atualizacao():
    Thread(target=atualizar_programa, args=(repo_url, pasta_destino)).start()
    
def checar_progresso():
    progresso_bar["value"] = 0
    while progresso_bar["value"] < 100:
        progresso_bar["value"] += 1
        progresso = progresso_bar["value"]
        porcentagem = int((progresso / 100) * 100)
        progresso_da_barra_label.configure(text=f"Progresso: {porcentagem}%", pady=10)
        root.update_idletasks()
        time.sleep(0.1)

    mensagem = atualizar_programa(repo_url, pasta_destino)
    messagebox.showinfo("Atualização Concluída", mensagem)
    root.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Atualizador")
    root.geometry("400x200")
    root.resizable(False, False)
    ctk.set_appearance_mode("Light")
    
    mensagem_label = ctk.CTkLabel(root, text="Verificando atualizações! Por favor, não feche o programa!", pady=10)
    mensagem_label.pack()

    style = ttk.Style()
    style.theme_use('default')
    style.configure('light_blue.Horizontal.TProgressbar', foreground='#6495ED')

    progresso_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", style='light_blue.Horizontal.TProgressbar')
    progresso_bar.pack(pady=10)

    progresso_da_barra_label = ctk.CTkLabel(root, text="Progresso: 0%", pady=10)
    progresso_da_barra_label.pack()

    Thread(target=checar_progresso).start()
    verificar_atualizacao()

    root.mainloop()
