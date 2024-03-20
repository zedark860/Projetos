import git
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
import time
import shutil

# Definindo as variáveis repo_url e pasta_destino no escopo global
repo_url = ""
pasta_destino = os.path.join(os.getcwd(), "Atualizador")  # Pasta onde o programa está instalado localmente

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

root = tk.Tk()
root.title("Atualizador")
root.geometry("400x200")

# Adicionando um rótulo com a mensagem
mensagem_label = tk.Label(root, text="Verificando atualizações! Por favor, não feche o programa!", pady=10)
mensagem_label.pack()

progresso_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progresso_bar.pack(pady=10)

def checar_progresso():
    progresso_bar["value"] = 0
    while progresso_bar["value"] < 100:
        progresso_bar["value"] += 1
        root.update_idletasks()
        time.sleep(0.1)

    mensagem = atualizar_programa(repo_url, pasta_destino)
    messagebox.showinfo("Atualização Concluída", mensagem)
    root.destroy()

Thread(target=checar_progresso).start()
verificar_atualizacao()

root.mainloop()
