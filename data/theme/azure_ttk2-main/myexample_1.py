import tkinter as tk
from tkinter import ttk

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self)
        self.setup_checkboxes()

    def print(self, objtext, x):
        print(objtext)
        print(x)
        print()

    def setup_checkboxes(self):
        # Create control variables

        self.var_0 = tk.BooleanVar()
        self.var_1 = tk.BooleanVar(value=True)
        self.var_2 = tk.BooleanVar()
        # Create a Frame for the Checkbuttons

        self.check_frame = ttk.LabelFrame(self, text="Checkbuttons", padding=(20, 10))
        self.check_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )

        # Checkbuttons - checked, unchecked, third state, disabled
        self.check_1 = ttk.Checkbutton(
            self.check_frame, text="Unchecked", variable=self.var_0,
            command=lambda: print(self.check_1["text"] + ":", self.var_0.get()))
        self.check_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.check_2 = ttk.Checkbutton(
            self.check_frame, text="Checked", variable=self.var_1)
        self.check_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

        self.check_3 = ttk.Checkbutton(
            self.check_frame, text="Third state", variable=self.var_2)
        self.check_3.state(["alternate"])
        self.check_3.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        self.check_4 = ttk.Checkbutton(
            self.check_frame, text="Disabled", state="disabled")
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