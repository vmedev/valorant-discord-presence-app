import threading
import customtkinter
from main import start_app, stop_app
from app_config import load_config, save_config

class App(customtkinter.CTk):  
    def __init__(self):
        super().__init__()
        self.title("Valorant Stats in Discord Presence")
        self.resizable(0, 0)
        
        frame = customtkinter.CTkFrame(master=self)
        frame.grid(row=0, column=0)
        
        
        font = customtkinter.CTkFont(size=16)

        self.labelName = customtkinter.CTkLabel(master=frame, text="Name", font=font)
        self.labelName.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.labelTag = customtkinter.CTkLabel(master=frame, text="Tag", font=font)
        self.labelTag.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.labelPUUID = customtkinter.CTkLabel(master=frame, text="PUUID", font=font)
        self.labelPUUID.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.labelAPI = customtkinter.CTkLabel(master=frame, text="API key", font=font)
        self.labelAPI.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.labelDiscordID = customtkinter.CTkLabel(master=frame, text="Discord ID", font=font)
        self.labelDiscordID.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.labelRegion = customtkinter.CTkLabel(master=frame, text="Region", font=font)
        self.labelRegion.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.entry_name = customtkinter.CTkEntry(master=frame)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.entry_tag = customtkinter.CTkEntry(master=frame)
        self.entry_tag.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.entry_puuid = customtkinter.CTkEntry(master=frame)
        self.entry_puuid.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        api_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent")
        api_frame.grid(row=3, column=1, padx=10, pady=5)
        self.entry_api = customtkinter.CTkEntry(master=api_frame, show="*", width=150)
        self.entry_api.pack(side="left")
        customtkinter.CTkButton(master=api_frame, text="👁", width=30, command=self._toggle_api).pack(side="left", padx=(4, 0))

        discord_frame = customtkinter.CTkFrame(master=frame, fg_color="transparent")
        discord_frame.grid(row=4, column=1, padx=10, pady=5)
        self.entry_discord_id = customtkinter.CTkEntry(master=discord_frame, show="*", width=150)
        self.entry_discord_id.pack(side="left")
        customtkinter.CTkButton(master=discord_frame, text="👁", width=30, command=self._toggle_discord_id).pack(side="left", padx=(4, 0))

        self.comboboxRegion = customtkinter.CTkComboBox(master=frame, values=["eu", "na", "latam", "br", "ap", "kr"], state="readonly")
        self.comboboxRegion.grid(row=5, column=1, pady=10, padx=10, sticky="ew")

        self.start_btn = customtkinter.CTkButton(master=frame, text="Start", command=self.submit)
        self.start_btn.grid(row=6, column=0, pady=5, padx=10, sticky="ew")
        self.stop_btn = customtkinter.CTkButton(master=frame, text="Stop", command=self.stop_app)
        self.stop_btn.grid(row=6, column=1, pady=5, padx=10, sticky="ew")
        
        saved = load_config()
        if saved:
            self.entry_name.insert(0, saved.get("NICKNAME", ""))
            self.entry_tag.insert(0, saved.get("TAG", ""))
            self.entry_puuid.insert(0, saved.get("PUUID", ""))
            self.entry_api.insert(0, saved.get("HENRIK_KEY", ""))
            self.entry_discord_id.insert(0, saved.get("DISCORD_CLIENT_ID", ""))
            if saved.get("REGION"):
                self.comboboxRegion.set(saved.get("REGION", "eu"))
        
        
    def _toggle_api(self):
        if self.entry_api.cget("show") == "*":
            self.entry_api.configure(show="")
        else:
            self.entry_api.configure(show="*")
            
    def _toggle_discord_id(self):
        if self.entry_discord_id.cget("show") == "*":
            self.entry_discord_id.configure(show="")
        else:
            self.entry_discord_id.configure(show="*")
            
    def showError(self, message):
        error_window = customtkinter.CTkToplevel(self)
        error_window.title("Error")
        error_window.resizable(0, 0)
        error_label = customtkinter.CTkLabel(master=error_window, text=message, font=customtkinter.CTkFont(size=14))
        error_label.pack(padx=20, pady=20)
        ok_button = customtkinter.CTkButton(master=error_window, text="OK", command=error_window.destroy)
        ok_button.pack(pady=(0, 20))
        
    def _run_app(self, config):
        try:
            start_app(config, on_error=lambda e: self.after(0, self.showError, e))
        except Exception as e:
            print("[APP ERROR]", e)
            self.after(0, self.showError, f"An error occurred while running the application: {e}")
            
    def submit(self):
        config = {
            "NICKNAME": self.entry_name.get(),
            "TAG": self.entry_tag.get(),
            "PUUID": self.entry_puuid.get(),
            "HENRIK_KEY": self.entry_api.get(),
            "DISCORD_CLIENT_ID": self.entry_discord_id.get(),
            "REGION": self.comboboxRegion.get(),
            "REFRESH_API": 60,
            "UPDATE_INTERVAL": 15,
        }
        print(config)
        save_config(config)
        threading.Thread(target=self._run_app, args=(config,), daemon=True).start()
        
        
    def stop_app(self):
            stop_app()
            print("[APP] stop signal sent")
            
    

            
if __name__ == "__main__":
    app = App()
    app.mainloop()