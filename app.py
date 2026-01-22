
import customtkinter as ctk
import win32gui
import win32con
import threading
import keyboard
import tkinter as tk
import json
import os

# Configuración de apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "hotkey_toggle": "ctrl+space",
    "hotkey_unpin_all": "ctrl+shift+u"
}

class WindowItem(ctk.CTkFrame):
    def __init__(self, master, hwnd, title, toggle_callback):
        super().__init__(master)
        self.hwnd = hwnd
        self.title = title
        self.toggle_callback = toggle_callback

        # Layout
        self.grid_columnconfigure(0, weight=1)
        
        # Etiqueta con el título de la ventana (truncado si es muy largo)
        display_title = (title[:50] + '...') if len(title) > 50 else title
        self.label = ctk.CTkLabel(self, text=display_title, anchor="w", font=("Roboto", 14))
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Switch para Always On Top
        self.switch = ctk.CTkSwitch(self, text="Fijar", command=self.on_toggle)
        self.switch.grid(row=0, column=1, padx=10, pady=10)

        if self.check_if_topmost():
            self.switch.select()

    def check_if_topmost(self):
        try:
            ex_style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
            return (ex_style & win32con.WS_EX_TOPMOST) != 0
        except:
            return False

    def on_toggle(self):
        try:
            self.toggle_callback(self.hwnd, self.switch.get())
        except Exception as e:
            print(f"Error toggling: {e}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simple Always On Top - Alex Monrás")
        self.geometry("600x700")
        
        self.load_config()

        # Título Principal
        self.header_label = ctk.CTkLabel(self, text="Gestor de Ventanas", font=("Roboto", 24, "bold"))
        self.header_label.pack(pady=(20, 10))

        # Información de Atajos
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="x", padx=20, pady=10)
        
        self.hotkey_label_1 = ctk.CTkLabel(self.info_frame, text="", text_color="cyan")
        self.hotkey_label_1.pack(pady=2)
        
        self.hotkey_label_2 = ctk.CTkLabel(self.info_frame, text="", text_color="#ff5555")
        self.hotkey_label_2.pack(pady=2)
        
        self.update_hotkey_labels()

        # Botones de Acción
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=20, pady=(10, 20))

        self.refresh_btn = ctk.CTkButton(self.buttons_frame, text="🔄 Refrescar Lista", command=self.refresh_windows)
        self.refresh_btn.pack(side="left", expand=True, padx=5)

        self.settings_btn = ctk.CTkButton(self.buttons_frame, text="⚙️ Configurar Atajos", command=self.open_settings_dialog, fg_color="gray")
        self.settings_btn.pack(side="right", expand=True, padx=5)

        # Frame Scrollable para la lista
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Ventanas Activas")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.windows = []
        self.refresh_windows()

        # Configurar Hotkeys
        self.setup_hotkeys()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = DEFAULT_CONFIG.copy()
        else:
            self.config = DEFAULT_CONFIG.copy()
            self.save_config()

    def save_config(self):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def update_hotkey_labels(self):
        self.hotkey_label_1.configure(text=f"⚡ {self.config['hotkey_toggle']}: Fijar/Desfijar Ventana Activa")
        self.hotkey_label_2.configure(text=f"🛑 {self.config['hotkey_unpin_all']}: Desfijar TODAS")

    def setup_hotkeys(self):
        # Limpiar hotkeys previos si existen
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass

        try:
            keyboard.add_hotkey(self.config['hotkey_toggle'], self.toggle_active_window_hotkey)
            keyboard.add_hotkey(self.config['hotkey_unpin_all'], self.unpin_all_hotkey)
        except Exception as e:
            print(f"[ERROR] Atajos inválidos o conflicto: {e}")

    def open_settings_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Configurar Atajos")
        dialog.geometry("400x300")
        dialog.attributes("-topmost", True)

        ctk.CTkLabel(dialog, text="Atajo: Fijar/Desfijar Activa", font=("Roboto", 14)).pack(pady=(20, 5))
        entry_toggle = ctk.CTkEntry(dialog, placeholder_text="ej: ctrl+space")
        entry_toggle.insert(0, self.config['hotkey_toggle'])
        entry_toggle.pack(pady=5)

        ctk.CTkLabel(dialog, text="Atajo: Desfijar TODAS", font=("Roboto", 14)).pack(pady=(20, 5))
        entry_unpin = ctk.CTkEntry(dialog, placeholder_text="ej: ctrl+shift+u")
        entry_unpin.insert(0, self.config['hotkey_unpin_all'])
        entry_unpin.pack(pady=5)

        def save_and_close():
            new_toggle = entry_toggle.get()
            new_unpin = entry_unpin.get()
            
            # Validación básica
            if new_toggle and new_unpin:
                self.config['hotkey_toggle'] = new_toggle
                self.config['hotkey_unpin_all'] = new_unpin
                self.save_config()
                self.update_hotkey_labels()
                self.setup_hotkeys()
                dialog.destroy()
            else:
                print("Atajos vacíos no permitidos")

        ctk.CTkButton(dialog, text="Guardar Cambios", command=save_and_close, fg_color="green").pack(pady=30)

    def toggle_active_window_hotkey(self):
        # Obtener ventana activa
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd: return
        
        current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        is_topmost = (current_style & win32con.WS_EX_TOPMOST) != 0
        
        # Invertir estado
        new_state = not is_topmost
        self.set_always_on_top(hwnd, new_state)
        
        # Feedback sonoro simple (opcional, imprime en consola por ahora)
        print(f"Hotkey activado para {hwnd}: {'Fijado' if new_state else 'Liberado'}")
        
        # Actualizar UI si es posible (thread safe call)
        self.after(100, self.refresh_windows)

    def unpin_all_hotkey(self):
        print("Desfijando TODAS las ventanas...")
        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                self.set_always_on_top(hwnd, False)
        
        win32gui.EnumWindows(callback, None)
        self.after(100, self.refresh_windows)

    def refresh_windows(self):
        # Limpiar lista anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        self.windows = []
        win32gui.EnumWindows(self.enum_windows_callback, None)

    def enum_windows_callback(self, hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title != "Simple Always On Top - Alex Monrás":
                 item = WindowItem(self.scroll_frame, hwnd, title, self.set_always_on_top)
                 item.pack(fill="x", padx=5, pady=5)
                 self.windows.append(item)

    def set_always_on_top(self, hwnd, value):
        try:
            if value:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            else:
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        except Exception as e:
            print(f"[ERROR] No se pudo cambiar estado: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
