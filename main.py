import time
import threading
from datetime import datetime

from valorant_api import get_stats
from presence import DiscordPresence

stop_event = threading.Event()
lock = threading.Lock()

latest_stats = None
latest_error = None
last_api_time = None

app_config = {}


def api_loop():
    global latest_stats, latest_error, last_api_time

    while not stop_event.is_set():
        try:
            stats = get_stats(app_config)
            with lock:
                latest_stats = stats
                latest_error = None
                last_api_time = datetime.now()
            print("[API OK]", stats)
        except Exception as e:
            with lock:
                latest_error = str(e)
            print("[API ERROR]", e)

        stop_event.wait(app_config["REFRESH_API"])


def rpc_loop():
    global latest_error

    try:
        print("[RPC] connecting...")
        presence = DiscordPresence(app_config["DISCORD_CLIENT_ID"])
        print("[RPC] connected")
    except Exception as e:
        with lock:
            latest_error = f"Discord RPC init error: {e}"
        print("[RPC INIT ERROR]", e)
        return

    while not stop_event.is_set():
        with lock:
            stats = latest_stats
            err = latest_error

        if stats and not err:
            try:
                print("[RPC] updating...", stats)
                presence.update(stats)
                print("[RPC] updated")
            except Exception as e:
                with lock:
                    latest_error = f"Discord RPC update error: {e}"
                print("[RPC UPDATE ERROR]", e)

        stop_event.wait(app_config["UPDATE_INTERVAL"])


def start_app(config):
    global latest_stats, latest_error, last_api_time, app_config
    app_config = config

    try:
        latest_stats = get_stats(app_config)
        last_api_time = datetime.now()
        print("[START] first stats loaded")
    except Exception as e:
        latest_error = str(e)
        print("[START ERROR]", e)

    threading.Thread(target=api_loop, daemon=True).start()
    threading.Thread(target=rpc_loop, daemon=True).start()

    while True:
        time.sleep(60)
