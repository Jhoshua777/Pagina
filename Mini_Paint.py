import tkinter as tk
from tkinter import colorchooser, filedialog, simpledialog
from PIL import Image, ImageDraw, ImageTk
import tkinter.font as tkFont

class MiniPaint:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Paint")
        self.canvas_width = 800
        self.canvas_height = 600
        self.brush_size = 5
        self.color = "black"
        self.shape = "brush"
        self.shapes = ["brush", "line", "rectangle", "oval", "text"]
        self.fill_color = ""
        self.fill = False
        self.undo_stack = []
        self.redo_stack = []
        self.setup_canvas()
        self.setup_tools()
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.eraser_mode = False

    def setup_canvas(self):
        # Configurar el lienzo
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
        # Crear una imagen en blanco para dibujar sobre ella
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.undo_stack.append(self.image.copy())

    def setup_tools(self):
        # Configurar las herramientas
        color_frame = tk.Frame(self.root, bg="lightgray")
        color_frame.pack(pady=5)
        # Crear un gradiente de colores para el fondo del menú
        for i, color in enumerate(["blue", "yellow", "red"]):
            color_label = tk.Label(color_frame, bg=color, width=3)
            color_label.grid(row=0, column=i, padx=2, pady=2)
        # Continuar con la configuración de las demás herramientas...
        font = tkFont.Font(family="Arial", size=10)

        self.color_button = tk.Button(color_frame, text="Color", command=self.choose_color, font=font, bg="lightblue", fg="black")
        self.color_button.grid(row=0, column=3, padx=10, pady=5)
        self.fill_button = tk.Button(color_frame, text="Fill", command=self.toggle_fill, font=font, bg="lightgreen", fg="black")
        self.fill_button.grid(row=0, column=4, padx=2, pady=5)
        self.shape_menu = tk.OptionMenu(color_frame, tk.StringVar(), *self.shapes, command=self.choose_shape)
        self.shape_menu.config(font=font, bg="lightyellow", fg="black")
        self.shape_menu.grid(row=0, column=5, padx=2, pady=5)
        self.size_scale = tk.Scale(color_frame, from_=1, to=50, orient=tk.HORIZONTAL, label="Size", command=self.change_size)
        self.size_scale.set(self.brush_size)
        self.size_scale.config(bg="lightgray")
        self.size_scale.grid(row=0, column=6, padx=2, pady=5)
        self.clear_button = tk.Button(color_frame, text="Clear", command=self.clear_canvas, font=font, bg="orange", fg="black")
        self.clear_button.grid(row=0, column=7, padx=10, pady=5)
        self.undo_button = tk.Button(color_frame, text="Undo", command=self.undo, font=font, bg="lightcoral", fg="black")
        self.undo_button.grid(row=0, column=8, padx=2, pady=5)
        self.redo_button = tk.Button(color_frame, text="Redo", command=self.redo, font=font, bg="lightcoral", fg="black")
        self.redo_button.grid(row=0, column=9, padx=2, pady=5)
        self.save_button = tk.Button(color_frame, text="Save", command=self.save, font=font, bg="lightpink", fg="black")
        self.save_button.grid(row=0, column=10, padx=10, pady=5)
        self.load_button = tk.Button(color_frame, text="Load", command=self.load, font=font, bg="lightpink", fg="black")
        self.load_button.grid(row=0, column=11, padx=2, pady=5)
        self.text_button = tk.Button(color_frame, text="Text", command=self.activate_text_tool, font=font, bg="lightblue", fg="black")
        self.text_button.grid(row=0, column=12, padx=10, pady=5)
        self.eraser_button = tk.Button(color_frame, text="Eraser", command=self.toggle_eraser, font=font, bg="gray", fg="black")
        self.eraser_button.grid(row=0, column=13, padx=10, pady=5)

    def choose_color(self):
        # Elegir un color para dibujar
        color = colorchooser.askcolor(color=self.color)[1]
        if color:
            self.color = color

    def toggle_fill(self):
        # Alternar el modo de relleno de las formas
        self.fill = not self.fill

    def choose_shape(self, shape):
        # Elegir la forma de dibujo
        self.shape = shape

    def change_size(self, val):
        # Cambiar el tamaño del pincel
        self.brush_size = int(val)

    def clear_canvas(self):
        # Borrar todo el contenido del lienzo y la imagen
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.undo_stack.append(self.image.copy())

    def paint(self, event):
        # Dibujar en el lienzo y en la imagen según la forma seleccionada
        if self.shape != "text":
            x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
            x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)

            if self.shape == "brush" and not self.eraser_mode:
                self.canvas.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)
                self.draw.ellipse([x1, y1, x2, y2], fill=self.color, outline=self.color)
            elif self.shape == "brush" and self.eraser_mode:
                self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")
                self.draw.ellipse([x1, y1, x2, y2], fill="white", outline="white")
            # Continuar con las otras formas...
        self.undo_stack.append(self.image.copy())

    def reset(self, event):
        # No se necesita implementar para corregir el error
        pass

    def undo(self):
        # Deshacer la última acción guardada en undo_stack
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.image = self.undo_stack[-1]
            self.load_image()

    def redo(self):
        # Rehacer la última acción guardada en redo_stack
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.image = self.undo_stack[-1]
            self.load_image()

    def save(self):
        # Guardar la imagen en un archivo seleccionado por el usuario
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if filename:
            self.image.save(filename)

    def load(self):
        # Cargar una imagen desde un archivo seleccionado por el usuario
        filename = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if filename:
            self.image = Image.open(filename)
            self.draw = ImageDraw.Draw(self.image)
            self.load_image()

    def load_image(self):
    # Mostrar la imagen actual en el lienzo
     self.canvas.delete("all")
     self.photo = ImageTk.PhotoImage(self.image)  # Mantener una referencia a la imagen
     self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)


    def zoom(self, event):
        # Permitir hacer zoom in/out en el lienzo
        scale = 1.1
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        if event.delta > 0:
            self.canvas.scale("all", x, y, scale, scale)
        elif event.delta < 0:
            self.canvas.scale("all", x, y, 1/scale, 1/scale)

    def activate_text_tool(self):
        # Activar la herramienta de texto
        self.shape = "text"
        self.canvas.bind("<Button-1>", self.place_text)
        self.canvas.bind("<Motion>", self.track_text_position)

    def place_text(self, event):
        # Colocar texto en el lienzo en la posición seleccionada por el usuario
        x, y = event.x, event.y
        text = simpledialog.askstring("Text", "Enter text:")
        if text:
            font = tkFont.Font(family="Arial", size=self.brush_size)
            self.draw.text((x, y), text, font=font, fill=self.color)
            self.load_image()

        self.shape = "brush"
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Motion>")

    def track_text_position(self, event):
        # Mostrar una vista previa del texto mientras se mueve el ratón
        x, y = event.x, event.y
        if self.shape == "text":
            self.canvas.delete("text_preview")
            font = tkFont.Font(family="Arial", size=self.brush_size)
            self.canvas.create_text(x, y, text="Sample Text", font=font, fill=self.color, anchor=tk.NW, tags="text_preview")

    def toggle_eraser(self):
        # Alternar el modo de borrado
        self.eraser_mode = not self.eraser_mode

if __name__ == "__main__":
    root = tk.Tk()
    paint_app = MiniPaint(root)
    root.mainloop()



