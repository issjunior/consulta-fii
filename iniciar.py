import subprocess

# Caminho completo para o script Python
script_path = "preco_teto/main.py"

# Comando para abrir um novo terminal, executar o script, e manter o terminal aberto
subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 {script_path}; exec bash'])

