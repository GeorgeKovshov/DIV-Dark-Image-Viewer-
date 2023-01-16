from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
#from PIL import ImageTk, Image
import sqlite3

root = ThemedTk()

root.title("Main window")
#root.wm_attributes('-transparentcolor','')
root.geometry("500x500")#change window size
root.configure(background="#363636")#background="#222222")")#D3D3D3
style = ttk.Style(root)

#style.map('Button', background=[('active', 'red')])


#style.theme_use("clearlooks")
#style.theme_use("scidgrey")
#style.theme_use("adapta")
#style.theme_use("equilux")
style.theme_use("clam")

#style.theme_use("keramik")

frame = ttk.Frame(root, borderwidth=5, relief="sunken", padding=[0, 0, 0, 10])
"""
Gray Iron: #48494B
Gray/Black Charcoal: #222021
Gray/white Pearl River: #D9DDDC
Purple Amethyst: #9966CB
Purple Mauvre: #784B84
Gray Steel: #777B7E

"""

style.configure('TFrame',
                     background="#333333",
                     foreground="white",
                     borderwidth=1,
                     bordercolor="#9966CB",
                     lightcolor="#9966CB",
                     darkcolor="#9966CB",
                     focuscolor="none",
                     font=("Bahnschrift", 14),
                     width=2)



style.configure('TButton',
                     background="#222021",#"#777B7E",
                     foreground="#D9DDDC",
                     borderwidth=1,
                     bordercolor="#777B7E",
                     lightcolor="#48494B",
                     darkcolor="#48494B",
                     focuscolor="none",
                     #font=("Helvetica", 12),
                     font=("Georgia", 12),
                     #font=("Garamond", 14),
                     width=2)
style.map('TButton',
                    background=[("pressed", "#777B7E"),
                                ("active", "#222021")],
                    borderwidth=[("active", 1)],
                    bordercolor=[("active", "#9966CB")],
                    lightcolor=[("active", "#48494B")],
                    darkcolor=[("active", "#48494B")],
                    foreground=[("pressed", "#D9DDDC"),
                                ("active", "white")]
                           )

style.configure('TScale',
                     troughcolor="#363636",
                     background="#222021",
                     foreground="white",
                     borderwidth=1,
                     bordercolor="#D9DDDC",
                     lightcolor="#48494B",
                     darkcolor="#777B7E",
                     focuscolor="none",
                     width=2)
style.map('TScale',
                    background=[("pressed", "#D9DDDC"),
                                ("active", "black")],
                    borderwidth=[("active", 0)],
                    bordercolor=[("active", "#D9DDDC")],
                    lightcolor=[("active", "#784B84")],
                    darkcolor=[("active", "#9966CB")],
                    foreground=[("pressed", "black"),
                                ("active", "white")]
                           )


"""
style.configure('TScale',
                     troughcolor="black",
                     background="black",
                     foreground="white",
                     borderwidth=1,
                     bordercolor="red",
                     lightcolor="yellow",
                     darkcolor="purple",
                     focuscolor="none",
                     font=("Bahnschrift", 14),
                     width=2)
style.map('TScale',
                    background=[("pressed", "white"),
                                ("active", "black")],
                    borderwidth=[("active", 0)],
                    bordercolor=[("active", "blue")],
                    lightcolor=[("active", "purple")],
                    darkcolor=[("active", "black")],
                    foreground=[("pressed", "black"),
                                ("active", "red")]
                           )
"""
"""
style.configure('TButton',
                     background="black",
                     foreground="white",
                     borderwidth=1,
                     bordercolor="red",
                     lightcolor="yellow",
                     darkcolor="purple",
                     focuscolor="none",
                     font=("Bahnschrift", 14),
                     width=2)
style.map('TButton',
                    background=[("pressed", "white"),
                                ("active", "grey")],
                    borderwidth=[("active", 0)],
                    bordercolor=[("active", "blue")],
                    lightcolor=[("active", "purple")],
                    darkcolor=[("active", "black")],
                    foreground=[("pressed", "black"),
                                ("active", "red")]
                           )
"""