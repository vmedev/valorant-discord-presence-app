import tkinter as tk
from tkinter import ttk
import threading

from main import start_app


def run_ui():
    def submit():
        config = {
            "NICKNAME": entry_name.get(),
            "TAG": entry_tag.get(),
            "PUUID": entry_puuid.get(),
            "HENRIK_KEY": entry_api.get(),
            "DISCORD_CLIENT_ID": entry_discord.get(),
            "REGION": combo_box.get(),
            "REFRESH_API": 60,
            "UPDATE_INTERVAL": 15,
        }

        result.config(
            text=(
                f"Name: {config['NICKNAME']}\n"
                f"Tag: {config['TAG']}\n"
                f"API: {config['HENRIK_KEY']}\n"
                f"Discord: {config['DISCORD_CLIENT_ID']}\n"
                f"Region: {config['REGION']}"
            )
        )

        threading.Thread(target=start_app, args=(config,), daemon=True).start()

    root = tk.Tk()
    root.title("VSDA")

    root.minsize(280, 280)

    tk.Label(root, text="Name", font=16).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Tag", font=16).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="PUUID", font=16).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="API key", font=16).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Discord ID", font=16).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    tk.Label(root, text="Region", font=16).grid(row=5, column=0, padx=10, pady=5, sticky="w")

    entry_name = tk.Entry(root)
    entry_tag = tk.Entry(root)
    entry_puuid = tk.Entry(root)
    entry_api = tk.Entry(root)
    entry_discord = tk.Entry(root)

    entry_name.grid(row=0, column=1, padx=10, pady=5)
    entry_tag.grid(row=1, column=1, padx=10, pady=5)
    entry_puuid.grid(row=2, column=1, padx=10, pady=5)
    entry_api.grid(row=3, column=1, padx=10, pady=5)
    entry_discord.grid(row=4, column=1, padx=10, pady=5)

    combo_box = ttk.Combobox(root, values=["eu", "na", "latam", "br", "ap", "kr"], state="readonly")
    combo_box.grid(row=5, column=1, columnspan=2, pady=10)

    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.grid(row=6, column=0, columnspan=2, pady=10)

    result = tk.Label(text="")
    result.grid(row=7, column=0, columnspan=2)

    root.mainloop()