import tkinter as tk

class AlphaTweak(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        self.parent = master
        self.canvas = tk.Canvas(self, width=200, height=100)
        self.bias = tk.Scale(self, from_=255, to=0, resolution=1, command=self.vscroll)
        self.bias.pack(side="left", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Configure>", self.configure)
        # OK button
        tk.Button(self, font=self.parent.custom_font,
                  text="OK",
                  command=self.quit).pack()
        tk.Button(self, font=self.parent.custom_font,
                  text="Cancel",
                  command=self.cancel).pack()
        
    def quit(self, event=None):
        self.parent.tweak_alpha_edge(self.bias.get())
        self.destroy()
        
    def cancel(self, event=None):
        self.destroy()
        
    def vscroll(self, event):
        self.configure(event)

    def get_line_coords(self, w, h, margin):
        x0 = 0
        y0 = (h - margin) *(-self.bias.get()+255)/255
        y1 = 0
        x1 = w - margin
        return x0, y0, x1, y1

    def get_canvas_width(self):
        return self.canvas.winfo_width()

    def get_canvas_height(self):
        return self.canvas.winfo_height()

    
    def configure(self, event):
        margin = 30
        self.canvas.delete("all")
        w = self.get_canvas_width()
        h = self.get_canvas_height()
        xy = 0, 0, w-margin, h-margin
        self.canvas.create_rectangle(xy)
        line_coords = self.get_line_coords(w, h, margin)
        self.canvas.create_line(line_coords)

        # Text
        font_size = 12
        bottom_left = font_size, h-margin+font_size 
        bottom_right = w-margin-font_size, h-margin+font_size 
        bottom_center = w/2, h-margin+font_size 
        middle_right = w-margin+font_size, h/2
        self.canvas.create_text(bottom_left,
                                text="0")
        self.canvas.create_text(bottom_right,
                                text="255")
        self.canvas.create_text(bottom_center,
                                text="Alpha input")
        self.canvas.create_text(middle_right,
                                text="Out")
