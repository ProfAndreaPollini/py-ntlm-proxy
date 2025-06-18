# run_proxy_app.py (versione con import corretti)
# -*- coding: utf-8 -*-

import tkinter  # noqa: F401

import keyring.errors
import customtkinter as ctk
import configparser
import logging
import threading
import queue
from collections import deque
from typing import Optional
import time
import os
import socket
import base64
import asyncio
import sys

# --- CONTROLLO SINGLE INSTANCE ---
try:
    import win32event
    import win32api
    import winerror

    mutex_name = "Global\\PyNtlmProxyApplicationMutex"
    import ctypes  # noqa: F401

    mutex = win32event.CreateMutex(None, 1, mutex_name)  # type: ignore
    last_error = win32api.GetLastError()

    if last_error == winerror.ERROR_ALREADY_EXISTS:
        logging.warning("Un'altra istanza dell'applicazione è già in esecuzione.")
        # Chiudi forzatamente il mutex per evitare leak
        if mutex:
            win32api.CloseHandle(mutex)
        sys.exit(0)

    # Registra una funzione per rilasciare il mutex all'uscita
    def cleanup_mutex():
        if mutex:
            win32api.CloseHandle(mutex)

    import atexit

    atexit.register(cleanup_mutex)

except ImportError:
    logging.warning(
        "Librerie win32 non disponibili, il controllo di istanza singola è disabilitato."
    )
    mutex = None

# --- LIBRERIE PER LE PRESTAZIONI ---
try:
    import winloop

    winloop.install()
    logging.info("winloop attivato per prestazioni di rete superiori.")
except ImportError:
    logging.warning(
        "winloop non trovato. L'event loop di default di asyncio verrà utilizzato."
    )

# --- LIBRERIE DI TERZE PARTI ---
from PIL import Image
from pystray import MenuItem, Icon
import keyring
from ntlm_auth import ntlm

# --- LIBRERIE PROXY.PY (con import corretti) ---
from proxy.http.parser import HttpParser
from proxy.http.parser import httpParserTypes
from proxy.http.proxy import HttpProxyBasePlugin
from proxy.http.exception import HttpProtocolException, ProxyAuthenticationFailed
from proxy.core.event import EventQueue

# --- CONFIGURAZIONE GLOBALE ---
APP_DATA_DIR = os.path.join(os.environ["LOCALAPPDATA"], "PythonNtlmProxy")
CONFIG_FILE = os.path.join(APP_DATA_DIR, "cntlm.ini")
KEYRING_SERVICE = "PythonNtlmProxyApp"
os.makedirs(APP_DATA_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PythonNtlmProxy")

# --- STATO CONDIVISO TRA THREAD ---
uri_log_queue = deque(maxlen=50)
stats_data = {"requests": 0, "status": "Inattivo", "start_time": None}
stats_lock = threading.Lock()
shutdown_event = threading.Event()
event_queue = EventQueue(queue=queue.Queue())

# --- CLASSI HELPER E PLUGIN ---


class ParsedResponse:
    """Classe helper per analizzare risposte HTTP grezze."""

    def __init__(self, raw: bytearray):
        # CORREZIONE: Usa la costante importata direttamente
        self.parser = HttpParser(httpParserTypes.RESPONSE_PARSER)
        self.parser.parse(raw)
        self.code = self.parser.get_status_code()
        self.headers = self.parser.get_headers()

    def get_header(self, name: bytes) -> Optional[bytes]:
        return self.headers.get(name.lower())


class NtlmProxyPlugin(HttpProxyBasePlugin):
    """Plugin per proxy.py che implementa l'autenticazione NTLMv2 verso un proxy genitore."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Load settings from the global configuration instead of flags
        self.settings = self._load_plugin_settings()

    def _load_plugin_settings(self) -> dict:
        """Load settings from the configuration file."""
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)

            settings = {
                "username": config.get("Auth", "Username"),
                "domain": config.get("Auth", "Domain"),
                "parent_proxy": config.get("Proxy", "ParentProxy"),
            }

            full_username = f"{settings['username']}@{settings['domain']}"
            password = keyring.get_password(KEYRING_SERVICE, full_username)
            settings["password"] = password or ""

            return settings
        except Exception:
            # Return empty settings if configuration fails
            return {
                "username": "",
                "domain": "",
                "password": "",
                "parent_proxy": "",
            }

    def before_upstream_connection(self, request: HttpParser) -> Optional[HttpParser]:
        with stats_lock:
            stats_data["requests"] += 1
        uri_log_queue.append(f"[{time.strftime('%H:%M:%S')}] {request.build_url()}")

        if not self.settings["parent_proxy"]:
            return request

        # For NTLM proxy, we don't establish direct upstream connection
        # Instead we'll handle it in handle_client_request
        return None

    def handle_client_request(self, request: HttpParser) -> Optional[HttpParser]:
        # Require proxy authentication
        if not request.has_header(b"proxy-authorization"):
            raise ProxyAuthenticationFailed(headers={b"Proxy-Authenticate": b"NTLM"})

        # For CONNECT requests, we need to handle NTLM authentication
        if request.method == b"CONNECT":
            try:
                proxy_host, proxy_port_str = self.settings["parent_proxy"].split(":")
                proxy_port = int(proxy_port_str)

                # Perform NTLM handshake and get connected socket
                asyncio.run(
                    self._perform_ntlm_handshake_sync(proxy_host, proxy_port, request)
                )

                # Return successful tunnel response
                self.client.queue(b"HTTP/1.1 200 Connection established\r\n\r\n")

                # Queue the socket for handling
                # Note: This is a simplified approach - in a real implementation
                # you'd need to properly handle the socket in the proxy framework
                return None

            except Exception as e:
                uri_log_queue.append(f"[{time.strftime('%H:%M:%S')}] ERRORE: {e}")
                raise HttpProtocolException(f"Errore NTLM: {e}")

        return request

    async def _perform_ntlm_handshake_sync(
        self, host: str, port: int, request: HttpParser
    ) -> socket.socket:
        """Versione sincrona per l'handshake NTLM"""
        reader, writer = await asyncio.open_connection(host, port)
        try:
            context = ntlm.Ntlm(ntlm_compatibility=3)
            negotiate_message = context.create_negotiate_message(
                self.settings["domain"]
            )
            req1 = self._build_connect_request(
                request.host,
                request.port,
                f"NTLM {base64.b64encode(negotiate_message).decode()}",
            )
            writer.write(req1)
            await writer.drain()
            resp2_raw = await reader.read(4096)
            if not resp2_raw:
                raise HttpProtocolException("Proxy genitore ha chiuso la connessione.")
            resp2 = ParsedResponse(resp2_raw)
            if resp2.code != 407:
                raise HttpProtocolException(f"Risposta inattesa: {resp2.code}")
            auth_header = resp2.get_header(b"proxy-authenticate")
            if not auth_header or not auth_header.startswith(b"NTLM "):
                raise HttpProtocolException("Il proxy genitore non ha offerto NTLM.")
            challenge_message = base64.b64decode(auth_header.split(b" ")[1])
            authenticate_message = context.create_authenticate_message(
                challenge_message,
                self.settings["username"],
                self.settings["domain"],
                password=self.settings["password"],
            )
            req3 = self._build_connect_request(
                request.host,
                request.port,
                f"NTLM {base64.b64encode(authenticate_message).decode()}",
            )
            writer.write(req3)
            await writer.drain()
            final_resp_raw = await reader.read(4096)
            final_resp = ParsedResponse(final_resp_raw)
            if final_resp.code == 200:
                return writer.get_extra_info("socket")
            raise HttpProtocolException(
                f"Autenticazione NTLM fallita. Codice: {final_resp.code}"
            )
        except Exception as e:
            writer.close()
            raise e

    def _build_connect_request(
        self, host: bytes, port: int, auth_header: Optional[str] = None
    ) -> bytes:
        req = [
            f"CONNECT {host.decode()}:{port} HTTP/1.1",
            f"Host: {host.decode()}:{port}",
            "Proxy-Connection: keep-alive",
            "User-Agent: PythonNtlmProxy/1.0",
        ]
        if auth_header:
            req.append(f"Proxy-Authorization: {auth_header}")
        return ("\r\n".join(req) + "\r\n\r\n").encode()


class ProxyThread(threading.Thread):
    # (Invariata)
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.name = "ProxyEngineThread"

    def run(self):
        try:
            settings = self.load_settings()
        except ValueError as e:
            logger.warning(f"Configurazione mancante o incompleta: {e}")
            with stats_lock:
                stats_data["status"] = f"Configurazione richiesta: {str(e)}"
            return
        except Exception as e:
            logger.error(f"Errore nel caricamento della configurazione: {e}")
            with stats_lock:
                stats_data["status"] = f"Errore configurazione: {str(e)}"
            return

        try:
            with stats_lock:
                stats_data["status"] = "Avvio in corso..."

            # Import proxy.py main functionality
            from proxy import Proxy

            # Start the proxy server
            with stats_lock:
                stats_data["status"] = f"Attivo su porta {settings['listen_port']}"
                stats_data["start_time"] = time.time()
                stats_data["requests"] = 0

            # Create and start proxy with our custom NTLM plugin
            import ipaddress

            logger.info(
                f"Avvio del proxy NTLM su {settings['listen_port']} con parent proxy {settings['parent_proxy']}"
            )

            with Proxy(
                port=settings["listen_port"],
                hostname=ipaddress.ip_address("127.0.0.1"),
                plugins=[NtlmProxyPlugin],
            ):
                # Keep the proxy running until shutdown is requested
                while not shutdown_event.is_set():
                    time.sleep(1)

        except Exception as e:
            logger.error(f"Errore nel thread del proxy: {e}")
            with stats_lock:
                stats_data["status"] = f"Errore: {str(e)}"
        finally:
            with stats_lock:
                if not stats_data["status"].startswith("Errore:") and not stats_data[
                    "status"
                ].startswith("Configurazione richiesta:"):
                    stats_data["status"] = "Inattivo"
        logger.info("Thread del proxy terminato.")

    def load_settings(self) -> dict:
        config = configparser.ConfigParser()

        # Check if config file exists and has the required sections
        if not os.path.exists(CONFIG_FILE):
            raise ValueError(
                "File di configurazione non trovato. Configuralo dalla UI."
            )

        config.read(CONFIG_FILE)

        # Check if required sections exist
        if not config.has_section("Auth"):
            raise ValueError(
                "Sezione 'Auth' mancante nel file di configurazione. Configuralo dalla UI."
            )
        if not config.has_section("Proxy"):
            raise ValueError(
                "Sezione 'Proxy' mancante nel file di configurazione. Configuralo dalla UI."
            )

        # Try to get configuration values with better error handling
        try:
            settings = {
                "username": config.get("Auth", "Username"),
                "domain": config.get("Auth", "Domain"),
                "parent_proxy": config.get("Proxy", "ParentProxy"),
                "listen_port": config.getint("Proxy", "ListenPort"),
            }
        except (configparser.NoOptionError, ValueError) as e:
            raise ValueError(
                f"Errore nel file di configurazione: {e}. Configuralo dalla UI."
            )

        # Check if any required values are empty
        if not settings["username"] or not settings["domain"]:
            raise ValueError(
                "Username o Domain mancanti nel file di configurazione. Configuralo dalla UI."
            )

        full_username = f"{settings['username']}@{settings['domain']}"
        password = keyring.get_password(KEYRING_SERVICE, full_username)
        if not password:
            raise ValueError(
                f"Credenziali per '{full_username}' non trovate. Configurale dalla UI."
            )
        settings["password"] = password
        return settings


class ProxyUI(ctk.CTk):
    # (Invariata)
    def __init__(self, proxy_thread_manager):
        super().__init__()
        self.proxy_manager = proxy_thread_manager
        self.title("Pannello di Controllo NTLM Proxy")
        self.geometry("700x550")
        ctk.set_appearance_mode("dark")
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(expand=True, fill="both", padx=10, pady=10)
        self.tab_view.add("Stato")
        self.tab_view.add("Configurazione")
        self.tab_view.add("Log Attività")
        self.create_status_tab()
        self.create_config_tab()
        self.create_log_tab()
        self.load_config_to_ui()
        self.update_ui_loop()

    def create_status_tab(self):
        tab = self.tab_view.tab("Stato")
        self.status_label = ctk.CTkLabel(
            tab, text="Stato: Inizializzazione...", font=("Arial", 16, "bold")
        )
        self.status_label.pack(pady=20)
        self.requests_label = ctk.CTkLabel(tab, text="Richieste gestite: 0")
        self.requests_label.pack(pady=5)
        self.uptime_label = ctk.CTkLabel(tab, text="Uptime: N/D")
        self.uptime_label.pack(pady=5)
        restart_button = ctk.CTkButton(
            tab,
            text="Riavvia Motore Proxy",
            command=self.proxy_manager.restart_proxy_thread,
        )
        restart_button.pack(pady=20)

    def create_config_tab(self):
        tab = self.tab_view.tab("Configurazione")
        tab.grid_columnconfigure(1, weight=1)
        self.entries = {}
        self.entries["username"] = self._create_config_entry(tab, "Username:", 0)
        self.entries["domain"] = self._create_config_entry(tab, "Domain:", 1)
        self.entries["parentproxy"] = self._create_config_entry(tab, "Parent Proxy:", 2)
        self.entries["listenport"] = self._create_config_entry(tab, "Listen Port:", 3)
        self.entries["password"] = self._create_config_entry(
            tab, "Password:", 4, show="*"
        )
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        self.save_creds_button = ctk.CTkButton(
            button_frame,
            text="Salva Credenziali e Riavvia",
            command=self.save_credentials,
        )
        self.save_creds_button.pack(side="left", padx=10)
        self.delete_creds_button = ctk.CTkButton(
            button_frame,
            text="Elimina Credenziali e Ferma",
            command=self.delete_credentials,
            fg_color="darkred",
            hover_color="red",
        )
        self.delete_creds_button.pack(side="left", padx=10)
        self.config_status_label = ctk.CTkLabel(tab, text="", text_color="green")
        self.config_status_label.grid(row=6, column=0, columnspan=2, pady=10)

    def create_log_tab(self):
        tab = self.tab_view.tab("Log Attività")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        self.log_textbox = ctk.CTkTextbox(
            tab, state="disabled", font=("Courier New", 10)
        )
        self.log_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def _create_config_entry(self, parent, text, row, **kwargs):
        ctk.CTkLabel(parent, text=text).grid(
            row=row, column=0, padx=10, pady=10, sticky="w"
        )
        entry = ctk.CTkEntry(parent, **kwargs)
        entry.grid(row=row, column=1, padx=10, pady=10, sticky="ew")
        return entry

    def load_config_to_ui(self):
        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            self.entries["username"].insert(
                0, config.get("Auth", "Username", fallback="")
            )
            self.entries["domain"].insert(0, config.get("Auth", "Domain", fallback=""))
            self.entries["parentproxy"].insert(
                0, config.get("Proxy", "ParentProxy", fallback="")
            )
            self.entries["listenport"].insert(
                0, config.get("Proxy", "ListenPort", fallback="3128")
            )
        except Exception as e:
            self.config_status_label.configure(
                text=f"Errore caricamento config: {e}", text_color="orange"
            )

    def _save_config_from_ui(self):
        # Ensure the config directory exists
        os.makedirs(APP_DATA_DIR, exist_ok=True)

        config = configparser.ConfigParser()
        config["Auth"] = {
            "Username": self.entries["username"].get(),
            "Domain": self.entries["domain"].get(),
        }
        config["Proxy"] = {
            "ParentProxy": self.entries["parentproxy"].get(),
            "ListenPort": self.entries["listenport"].get(),
        }
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)

    def save_credentials(self):
        username = self.entries["username"].get()
        domain = self.entries["domain"].get()
        password = self.entries["password"].get()
        if not all([username, domain, password]):
            self.config_status_label.configure(
                text="Errore: tutti i campi sono obbligatori.", text_color="orange"
            )
            return
        try:
            full_username = f"{username}@{domain}"
            keyring.set_password(KEYRING_SERVICE, full_username, password)
            self._save_config_from_ui()
            self.config_status_label.configure(
                text="Credenziali salvate! Riavvio del proxy...", text_color="green"
            )
            self.proxy_manager.restart_proxy_thread()
        except Exception as e:
            self.config_status_label.configure(
                text=f"Errore salvataggio credenziali: {e}", text_color="red"
            )

    def delete_credentials(self):
        username = self.entries["username"].get()
        domain = self.entries["domain"].get()
        if not all([username, domain]):
            self.config_status_label.configure(
                text="Errore: Username e Dominio necessari.", text_color="orange"
            )
            return
        try:
            full_username = f"{username}@{domain}"
            keyring.delete_password(KEYRING_SERVICE, full_username)
            self.config_status_label.configure(
                text="Credenziali eliminate. Il proxy è stato fermato.",
                text_color="green",
            )
            self.proxy_manager.stop_proxy_thread()
        except keyring.errors.PasswordDeleteError as e:
            self.config_status_label.configure(
                text=f"Errore eliminazione credenziali: {e}", text_color="red"
            )
            # self.config_status_label.configure(
            #     text="Nessuna credenziale da eliminare.", text_color="orange"
            # )
        except Exception as e:
            self.config_status_label.configure(
                text=f"Errore eliminazione credenziali: {e}", text_color="red"
            )

    def update_ui_loop(self):
        with stats_lock:
            self.status_label.configure(text=f"Stato: {stats_data['status']}")
            self.requests_label.configure(
                text=f"Richieste gestite: {stats_data['requests']}"
            )
            if stats_data.get("start_time"):
                uptime = time.time() - stats_data["start_time"]
                self.uptime_label.configure(text=f"Uptime: {int(uptime)}s")
            else:
                self.uptime_label.configure(text="Uptime: N/D")
            self.log_textbox.configure(state="normal")
            self.log_textbox.delete("1.0", "end")
            self.log_textbox.insert("1.0", "\n".join(uri_log_queue))
            self.log_textbox.yview_moveto(1.0)
            self.log_textbox.configure(state="disabled")
        self.after(2000, self.update_ui_loop)

    def withdraw(self):
        super().withdraw()

    def show(self):
        self.deiconify()


class AppManager:
    # (Invariata)
    def __init__(self):
        self.create_default_config_if_needed()
        self.proxy_thread: Optional[ProxyThread] = None
        self.ui = ProxyUI(self)
        self.tray_icon = self.setup_tray()

    def create_default_config_if_needed(self):
        """Crea un file di configurazione di default se non esiste."""
        if not os.path.exists(CONFIG_FILE):
            os.makedirs(APP_DATA_DIR, exist_ok=True)
            config = configparser.ConfigParser()
            config["Auth"] = {
                "Username": "",
                "Domain": "",
            }
            config["Proxy"] = {
                "ParentProxy": "",
                "ListenPort": "3128",
            }
            with open(CONFIG_FILE, "w") as configfile:
                config.write(configfile)
            logger.info(f"File di configurazione di default creato: {CONFIG_FILE}")

    def run(self):
        self.start_proxy_thread()
        tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        tray_thread.start()
        self.ui.mainloop()

    def start_proxy_thread(self):
        if self.proxy_thread and self.proxy_thread.is_alive():
            return
        self.proxy_thread = ProxyThread()
        self.proxy_thread.start()

    def stop_proxy_thread(self):
        if not self.proxy_thread or not self.proxy_thread.is_alive():
            return
        event_queue.put(None)
        self.proxy_thread.join(timeout=5.0)

    def restart_proxy_thread(self):
        self.stop_proxy_thread()
        self.start_proxy_thread()

    def setup_tray(self):
        image = Image.new("RGB", (64, 64), (20, 90, 150))
        menu = (
            MenuItem("Apri Pannello", self.ui.show, default=True),
            MenuItem("Esci", self.quit_app),
        )
        return Icon("PythonProxy", image, "Proxy NTLM", menu)

    def quit_app(self):
        """Chiude l'applicazione in modo pulito."""
        logger.info("Chiusura dell'applicazione in corso...")
        shutdown_event.set()
        self.stop_proxy_thread()
        self.tray_icon.stop()
        self.ui.quit()
        # Assicuriamoci che l'applicazione termini completamente
        sys.exit(0)


if __name__ == "__main__":
    # Incolla qui il codice di avvio, è invariato
    app_manager = AppManager()
    app_manager.run()
