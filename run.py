import webbrowser
from time import sleep
from threading import Thread
from app import app  # Assure-toi que ton app Flask est dans app.py

# Fonction pour démarrer le serveur Flask dans un thread
def run_flask():
    app.run(debug=True, host='127.0.0.1', port=5000)

# Démarrer le serveur Flask dans un thread séparé
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Attendre un peu que le serveur Flask se lance
sleep(2)

# Ouvrir le navigateur par défaut pour l'application
webbrowser.open("http://127.0.0.1:5000/")

# Empêcher le script de se terminer immédiatement
flask_thread.join()