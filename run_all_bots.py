import subprocess

bots = ["1botaudio.py", "bot2.py", "bot3.py"]  # Adicione aqui os nomes dos seus scripts de bots

for bot in bots:
    subprocess.Popen(["python3", bot])
