"""
Gray Iron: #48494B
Gray/Black Charcoal: #222021
Gray/white Pearl River: #D9DDDC
Purple Amethyst: #9966CB
Purple Mauvre: #784B84
Gray Steel: #777B7E

"""

def my_style(style):
    style.configure('TFrame',
                         background="#333333",
                         foreground="white",
                         borderwidth=1,
                         bordercolor="#777B7E",
                         lightcolor="#48494B",
                         darkcolor="#48494B",
                         focuscolor="none",
                         font=("Georgia", 14),
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
                         width=12)
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

    style.configure("TCheckbutton",
                        #indicatorbackground="black",
                        #indicatorforeground="white",
                        background = "#222021",
                        foreground = "#D9DDDC",
                        borderwidth = 1,
                        bordercolor = "green",
                        lightcolor = "#784B84",
                        darkcolor = "#9966CB",
                        focuscolor = "none",
                        font = ("Georgia", 11),
                        width = 11,
                        height = 20)

    style.map('TCheckbutton',
                        background=[("pressed", "#1F1F1F"),
                                    ("active", "#1F1F1F")],
                        #background=[("pressed", "#777B7E"),
                        #            ("active", "#1F1F1F")],
                        borderwidth=[("active", 10)],
                        bordercolor=[("active", "green")],
                        lightcolor=[("active", "#784B84")],
                        darkcolor=[("active", "#9966CB")],
                        foreground=[("pressed", "white"),
                                    ("active", "white")]
                               )


    style.configure('check.TFrame',
                    background="#333333",
                    foreground="white",
                    borderwidth=1,
                    bordercolor="#777B7E",
                    lightcolor="#48494B",
                    darkcolor="#48494B",
                    focuscolor="none",
                    font=("Georgia", 14),
                    width=2)



def change_checkbutton(style, img_ticked_box, img_unticked_box):
    style.element_create("tickbox", "image", img_unticked_box, ("selected", img_ticked_box))
    # replace the checkbutton indicator with the custom tickbox in the Checkbutton's layout
    style.layout(
        "TCheckbutton",
        [('Checkbutton.padding',
            {'sticky': 'w',
            'children': [('Checkbutton.tickbox', {'side': 'right', 'sticky': ''}),
                        ('Checkbutton.focus',
                            {'side': 'left',
                            'sticky': 'w',
                            'children': [('Checkbutton.label', {'sticky': 'nswe'})]})]})]
    )

def change_style(e, styles, style):
    #global style
    style.configure(f'{styles}.TFrame',
                    bordercolor="#9966CB",
                    lightcolor="#48494B",
                    darkcolor="#48494B"
                    )

def change_style_back(e, styles, style):
    style.configure(f'{styles}.TFrame',
                    bordercolor="#777B7E",
                    lightcolor="#48494B",
                    darkcolor="#48494B",
                    )