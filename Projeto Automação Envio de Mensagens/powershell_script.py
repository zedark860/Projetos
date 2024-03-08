import os

def generate_powershell_script(mensagem):
        # Caminho padrão
    path_padrao = os.getcwd()
    
    # Caminho do txt com todas as máquinas da rede
    path = path_padrao + r"\Users.txt"
    
    # Caminho do PsExec.exe
    filepath = path_padrao + r"\PsExec.exe"
    
    # Criar script PowerShell dinamicamente
    script_powershell = fr"""
    $computadores = Get-Content -Path "{path}"
    $mensagem = "{mensagem}"

    foreach ($computador in $computadores) {{
        $argumentos = @("\\$computador", "-s", "-i", "msg.exe", "/server:$computador", "*", "$mensagem")
        Start-Process -FilePath "{filepath}" -ArgumentList $argumentos -NoNewWindow -Wait
    }}
    """
    
    return script_powershell