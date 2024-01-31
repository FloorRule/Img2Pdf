import os
import tkinter as tk
from tkinter import messagebox

import PIL.features
from PIL import Image, ImageTk


def show_folder_contents():
    folder_path = entry.get()
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        file_list.delete(0, tk.END)  # Clear previous content in the listbox
        for item in os.listdir(folder_path):
            file_list.insert(tk.END, item)
    else:
        messagebox.showerror("Error", "Invalid folder path")
    entry.config(state="disabled")


def display_image(event):
    selected_item = file_list.get(file_list.curselection())
    selected_path = os.path.join(entry.get(), selected_item)
    if os.path.isfile(selected_path) and selected_item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        img = Image.open(selected_path)
        img.thumbnail((300, 300))  # Adjust size as needed
        img = ImageTk.PhotoImage(img)
        image_canvas.config(width=img.width(), height=img.height())
        image_canvas.create_image(0, 0, anchor=tk.NW, image=img)
        image_canvas.image = img  # Keep a reference to prevent image garbage collection
    else:
        # Clear the canvas if the selected item is not an image file
        image_canvas.delete("all")


def on_select(event):
    entry.config(state="normal")
    selected_item = file_list.get(file_list.curselection())
    selected_path = os.path.join(entry.get(), selected_item)
    if os.path.isdir(selected_path):
        entry.delete(0, tk.END)
        entry.insert(tk.END, selected_path)
        show_folder_contents()
    else:
        display_image(event)
    entry.config(state="disabled")


def go_back():
    entry.config(state="normal")
    current_path = entry.get()
    if current_path:
        parent_path = os.path.dirname(current_path)
        entry.delete(0, tk.END)
        entry.insert(tk.END, parent_path)
        show_folder_contents()
    entry.config(state="disabled")

root = tk.Tk()
root.geometry("450x400")
root.resizable(False, False)
root.title("Folder Content Visualizer")
path = "./images"

# Entry field to input folder path
entry = tk.Entry(root, width=50)
entry.insert(0, path)
entry.pack()
entry.config(state="disabled")

# Canvas to display images
image_canvas = tk.Canvas(root, bg="white", width=200, height=200)
image_canvas.pack(side=tk.RIGHT, padx=10, pady=10)

# Button to display folder contents
show_button = tk.Button(root, text="Show Folder Contents", command=show_folder_contents)
#show_button.pack()

# Listbox to display folder contents
file_list = tk.Listbox(root, height=15, width=60)
file_list.pack(side=tk.LEFT, padx=10, pady=10)

# Bind a function to the listbox click event
file_list.bind('<<ListboxSelect>>', on_select)

# Back button to navigate to the parent directory
back_button = tk.Button(root, text="Back", command=go_back)
#back_button.pack()

show_folder_contents()

root.mainloop()
