import subprocess

bots = ["1botaudio.py"]  # Adicione aqui os nomes dos seus scripts de bots

for bot in bots:
    subprocess.Popen(["python3", bot])
