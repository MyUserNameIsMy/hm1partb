import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np

root = tk.Tk()
root.title("Homework Part B")
root.geometry("800x800")

original_image = None
display_image = None

def browse_image():
    global original_image, display_image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        original_image = Image.open(file_path)
        original_image = original_image.resize((400, 400))
        display_image = ImageTk.PhotoImage(original_image)
        img_label.config(image=display_image)
        img_label.image = display_image

def convert_to_grayscale():
    global original_image, display_image
    if original_image is not None:
        grayscale_image = ImageOps.grayscale(original_image)
        display_image = ImageTk.PhotoImage(grayscale_image)
        img_label.config(image=display_image)
        img_label.image = display_image

def update_image():
    global original_image, display_image
    if original_image is not None:
        h_low = h_low_slider.get()
        h_high = h_high_slider.get()

        original_array = np.array(original_image)
        grayscale_array = np.mean(original_array, axis=2).astype(np.uint8)
        mask = (grayscale_array >= h_low) & (grayscale_array <= h_high)

        output_array = np.zeros_like(original_array)
        output_array[mask] = original_array[mask]

        output_image = Image.fromarray(output_array)
        display_image = ImageTk.PhotoImage(output_image)
        img_label.config(image=display_image)
        img_label.image = display_image

def slider_change(event=None):
    h_low_value_label.config(text=f"h_low: {h_low_slider.get()}")
    h_high_value_label.config(text=f"h_high: {h_high_slider.get()}")
    update_image()

img_label = tk.Label(root)
img_label.pack(pady=20)

browse_button = tk.Button(root, text="Browse", command=browse_image)
browse_button.pack(pady=10)

grayscale_button = tk.Button(root, text="Convert to Grayscale", command=convert_to_grayscale)
grayscale_button.pack(pady=10)

h_low_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=slider_change)
h_low_slider.pack(fill=tk.X, padx=20)
h_low_slider.set(0)

h_low_value_label = tk.Label(root, text=f"h_low: {h_low_slider.get()}")
h_low_value_label.pack()

h_high_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=slider_change)
h_high_slider.pack(fill=tk.X, padx=20)
h_high_slider.set(255)

h_high_value_label = tk.Label(root, text=f"h_high: {h_high_slider.get()}")
h_high_value_label.pack()

root.mainloop()
