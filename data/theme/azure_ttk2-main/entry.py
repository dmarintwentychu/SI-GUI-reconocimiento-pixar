import tkinter as tk
from tkinter import ttk

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.setup_frames()
        self.setup_button()
        self.setup_entry()
        self.setup_checkboxes()

    def print(self, objtext, x):
        print(objtext, x)
        print()

    def setup_frames(self):
        # frame for button --------------- frame 0 / button
        self.button_frame0 = ttk.LabelFrame(self, text="Entry", padding=(20, 10))
        self.button_frame0.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # frame for entry ---------------- frame 1 / entry
        self.entry_frame1 = ttk.LabelFrame(self, text="Entry", padding=(20, 10))
        self.entry_frame1.grid(
            row=1, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

        # frame for checkboxes ----------- frame 2 / checkboxes
        self.check_frame2 = ttk.LabelFrame(self, text="Checkbuttons", padding=(20, 10))
        self.check_frame2.grid(
            row=2, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")

    def setup_button(self):
        self.accentbutton = ttk.Button(
        self.button_frame0, text="Accent button", style="Accent.TButton",
            command=lambda: self.print("Accent button: ", "pressed")
        )
        self.accentbutton.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

    def setup_entry(self):
        self.entry = ttk.Entry(self.entry_frame1)
        self.entry.insert(0, "")
        self.entry.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.entry.bind("<Return>", lambda x: self.print("text:", self.entry.get()))

    def setup_checkboxes(self):

        # Create control variables
        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()

        # Checkbuttons - checked, unchecked, third state, disabled
        self.check_1 = ttk.Checkbutton(
            self.check_frame2, text="Unchecked", variable=self.var_0,
            command=lambda: print(self.check_1["text"] + ":", self.var_0.get()))
        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.check_2 = ttk.Checkbutton(
            self.check_frame2, text="Checked", variable=self.var_1)
        self.check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.check_3 = ttk.Checkbutton(
            self.check_frame2, text="Third state", variable=self.var_2)
        self.check_3.state(["alternate"])
        self.check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.check_4 = ttk.Checkbutton(
            self.check_frame2, text="Disabled", state="disabled")
        self.check_4.state(["disabled !alternate"])
        self.check_4.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Azure dark theme")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()