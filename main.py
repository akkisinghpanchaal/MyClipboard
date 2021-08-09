# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pickle
import tkinter as tk
import os
from tkinter import messagebox, Scrollbar, RIGHT, Y, BOTTOM, X
import pyperclip

import threading
import time
from datetime import datetime
from modes import *
from clip_config import __CLIPBOARD_MODE__, __AUTO_SAVE_INTERVAL__

class SaveRoutine():
    def __init__(self, runfunc, last_saved_holder):
        self.runfunc = runfunc
        self.is_running = True
        self.lsh = last_saved_holder
        self.save_thread = threading.Thread(target=self.run)
    def run(self):
        while self.is_running:
            print("saving...")
            self.runfunc()
            print("saved!")
            self.lsh.set(f"Last saved on {datetime.now().strftime('%b %-d, %Y @ %I:%M:%S %p')}")
            time.sleep(__AUTO_SAVE_INTERVAL__)
    def terminate(self):
        self.is_running = False
    def start(self):
        self.save_thread.start()


class Clipboard:
    def __init__(self):
        self.mode = __CLIPBOARD_MODE__
        self.cwd = "/home/pooja/PycharmProjects/Clipboard_1/"
        self.data_file_path = self.cwd + self._get_data_file()

        self.window = tk.Tk(className='MyClipboardApp')
        self.window.geometry("700x300")
        self.window.title("Clipboard v1.0")
        # self.window.iconbitmap('/home/pooja/PycharmProjects/Clipboard_1/clipboard2')
        appicon = tk.Image("photo", file='/home/pooja/PycharmProjects/Clipboard_1/clipboard.png')
        self.window.tk.call('wm', 'iconphoto', self.window._w, appicon)
        self.show_win = None
        self.data = self._get_data()
        # print(self.data)
        self.show_frame = tk.Frame(self.window).grid()

        self.last_saved_string = tk.StringVar(self.window)
        self.save_routine = SaveRoutine(self._save_data, self.last_saved_string)

    def _get_data_file(self):
        if self.mode == RunMode.DEV:
            return "test_data.pkl"
        return "data.pkl"

    def _get_data(self):
        data = dict()

        if not os.path.exists(self.data_file_path):
            datafile = open(self.data_file_path, "wb")
            pickle.dump(dict(), datafile)
            datafile.close()
        datafile = open(self.data_file_path, "rb")
        data = pickle.load(datafile)
        datafile.close()
        return data

    def _save_data(self):
        datafile = open(self.data_file_path, "wb")
        pickle.dump(self.data, datafile)
        datafile.close()

    def _add_clip(self, name, value):
        print(self.data, name, value)
        if not name or not value:
            return
        else:
            self.data[name] = value
        print(self.data)

    def _copy_to_clipboard(self, val):
        print(val)
        pyperclip.copy(val)

    def _show_clips(self):
        if self.show_win is not None and self.show_win.winfo_exists():
            self.show_win.lift()
            return
        self.show_win = tk.Toplevel(self.window)
        self.show_win.title("Your Clips")
        self.show_win.grid_rowconfigure(0, weight=1)
        self.show_win.grid_columnconfigure(0, weight=1)
        clipnumber = 0
        percol = 5
        for name, val in sorted(self.data.items(), key=lambda x: x[0].lower()):
            btn = tk.Button(self.show_win,
                            text=f"{name}",
                            command=lambda arg=val: self._copy_to_clipboard(arg)).grid(row=(clipnumber % percol),
                                                                                       column=(clipnumber // percol),
                                                                                       padx=10)
            clipnumber += 1
        self.show_win.mainloop()

    def _on_closing(self):
        self.save_routine.terminate()
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._save_data()
            self.window.destroy()

            if self.show_win:
                self.show_win.destroy()

    def _start_clipboard(self):
        input_frame = tk.Frame(self.window)
        label1 = tk.Label(self.window, text="Name:\t").grid(row=0, column=0)
        inp_name_var = tk.StringVar(self.window)
        entry_name = tk.Entry(self.window, textvariable=inp_name_var).grid(row=0, column=1)
        label1 = tk.Label(self.window, text="Text:\t").grid(row=1, column=0)
        entry_var = tk.StringVar(self.window)
        entry_value = tk.Entry(self.window, textvariable=entry_var).grid(row=1, column=1)
        btn = tk.Button(self.window, text="Add Clip!",
                        command=lambda: self._add_clip(inp_name_var.get(), entry_var.get())).grid(row=2)
        show_btn = tk.Button(self.window, text="Show Clips!", command=lambda: self._show_clips()).grid()
        show_btn = tk.Button(self.window, text="Save Clips!", command=lambda: self._save_data()).grid()
        last_saved_info = tk.Label(self.window, textvariable=self.last_saved_string).grid()
        self.last_saved_string.set("things that we need now!")
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.save_routine.start()
        self.window.mainloop()

    def start(self):
        self._start_clipboard()


if __name__ == '__main__':
    cb = Clipboard()
    cb.start()
