import tkinter as tk
from tkinter import filedialog

window = tk.Tk()
window.file = filedialog.askopenfile()
window.mainloop()