from tkinter import Tk, Label
from PIL import Image

# Replace with your image path
image_path = "C:\\Users\\KIIT\\Desktop\\courses\\ai\\apisgoogle\\map_image.png"

root = Tk()
root.title("My Image")

# Load image
image = Image.open(image_path)

# Resize image (optional)
image = image.resize((600, 400))  # Adjust dimensions as needed

# Create label and display image
image_label = Label(root, image=image)
image_label.pack()

root.mainloop()
