# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pickle
import tkinter as tk
import os
from tkinter import messagebox
import pyperclip

class Clipboard:
    def __init__(self):

        self.cwd = "/home/pooja/PycharmProjects/Clipboard_1/"
        self.data_file_path = self.cwd + "data.pkl"

        self.window = tk.Tk()
        self.window.geometry("700x300")
        self.window.title("Clipboard v1.0")
        self.show_win = None
        self.data = self._get_data()
        self.show_frame = tk.Frame(self.window).grid()



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
        # win.clipboard_clear()
        # win.clipboard_append(val)
        pyperclip.copy(val)

    def _show_clips(self):
        self.show_win = tk.Tk()
        self.show_win.geometry("700x300")
        self.show_win.title("Your Clips")
        i = 0
        for name, val in self.data.items():
            tk.Button(self.show_win, text=f"{name}", command=lambda arg=val: self._copy_to_clipboard(arg)).grid()
            # tk.Button(show_win, text=f"{name}", command=lambda: self._remove_clip(show_win, val)).grid(row=i,
            #                                                                                                  column=1)
        self.show_win.mainloop()

    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._save_data()
            self.window.destroy()

            if self.show_win:
                self.show_win.destroy()

    def _start_clipboard(self):
        # print(type(data))
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

        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.window.mainloop()

    def start(self):
        self._start_clipboard()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cb = Clipboard()
    cb.start()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
