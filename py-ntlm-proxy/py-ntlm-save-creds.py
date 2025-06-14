# save_creds.py
import keyring
import getpass

# Questo è un nome univoco per la tua applicazione.
# Tutte le credenziali verranno salvate sotto questo "servizio".
SERVICE_NAME = "PyNtlmProxyApp"

print(f"Configurazione delle credenziali per il servizio: '{SERVICE_NAME}'")

# Chiedi le informazioni all'utente
username = input("Inserisci il tuo username: ")
domain = input("Inserisci il tuo dominio: ")
password = getpass.getpass("Inserisci la tua password (non verrà visualizzata): ")

# Salviamo la password usando 'username@domain' come identificatore utente
full_username = f"{username}@{domain}"

try:
    # Salva la password nel Windows Credential Manager
    keyring.set_password(SERVICE_NAME, full_username, password)
    print("\nCredenziali salvate con successo!")
    print(f"Ora puoi avviare il proxy. Verranno usate le credenziali per '{full_username}'.")
    
    # Per completezza, potremmo salvare anche il solo nome utente e dominio se servono separati
    # ma spesso è più pulito recuperare tutto da una stringa.

except Exception as e:
    print(f"\nErrore durante il salvataggio delle credenziali: {e}")