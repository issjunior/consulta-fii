import subprocess
import sys
import os

# Caminho completo para o script Python que você quer executar
script_path = os.path.abspath("preco_teto/main.py")

def abrir_terminal():
    if sys.platform.startswith('linux'):
        # Para Linux, usando gnome-terminal como exemplo
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 {script_path}; exec bash'])
    elif sys.platform.startswith('win'):
        # Para Windows, usando cmd
        subprocess.Popen(['start', 'cmd', '/k', f'python {script_path}'], shell=True)
    elif sys.platform == 'darwin':
        # Para macOS, usando Terminal com AppleScript
        subprocess.Popen(['osascript', '-e', f'tell app "Terminal" to do script "python3 {script_path}"'])
    else:
        print("Sistema operacional não suportado.")

# Executa a função para abrir o terminal
abrir_terminal()
