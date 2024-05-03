import os.path

import customtkinter
from customtkinter import filedialog
from PIL import Image, ImageOps
import torch
import ai_image_detector
import torchvision.transforms as transforms
import numpy as np

torch.device("cpu")

root = customtkinter.CTk()
root.geometry("800x800")
root.title("AI Image Detector")
root.iconbitmap("icon_transparent.ico")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

model_type = customtkinter.StringVar(value="art_model")


def add_base_widgets():
    title_label = customtkinter.CTkLabel(master=frame, text="AI Image Detector", font=("Arial", 50))
    title_label.pack(pady=7, padx=12)

    combo_box = customtkinter.CTkComboBox(master=frame,
                                          values=["art_model", "deepfake_model", "nature_model"],
                                          command=load_model,
                                          variable=model_type,
                                          font=("Arial", 15))
    combo_box.pack(pady=7, padx=10)
    combo_box.set(model_type.get())

    button = customtkinter.CTkButton(master=frame, text="Load Image", command=load_image, font=("Arial", 15))
    button.pack(pady=5, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Detect Image", command=detect_image, font=("Arial", 15))
    button.pack(pady=5, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Batch Detect Images", command=batch_detect_images,
                                     font=("Arial", 15))
    button.pack(pady=20, padx=10)


test_image = 0
test_image_pil = 0


def load_image():
    print("loading image...")
    image_path = filedialog.askopenfilename(title="Select an Image",
                                            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

    if not image_path:
        return

    global test_image, test_image_pil
    test_image_pil = Image.open(image_path).convert('RGB').resize((64, 64))
    test_image = ai_image_detector.transform(test_image_pil).unsqueeze(0)

    for widget in frame.winfo_children():
        widget.destroy()

    add_base_widgets()

    image = customtkinter.CTkImage(Image.open(image_path), size=(300, 300))
    image_label = customtkinter.CTkLabel(master=frame, text="", image=image)
    image_label.pack()


trained_model = ai_image_detector.AIImageDetector()
trained_model.load_state_dict(torch.load("models/art_model.pth", map_location=torch.device('cpu')))


def load_model(model_choice):
    trained_model.load_state_dict(torch.load("models/" + model_choice + ".pth", map_location=torch.device('cpu')))
    trained_model.eval()
    print("loaded " + model_choice)


def detect_image():
    with torch.no_grad():
        output = trained_model(test_image)
        _, predicted = torch.max(output, 1)

        if predicted.item() == 0:
            prediction = "AI Image"
        else:
            prediction = "Real Image"

        message_label = customtkinter.CTkLabel(master=frame, text=prediction, font=("Arial", 20))
        message_label.pack(pady=12, padx=10)


def batch_detect_images():
    file_paths = filedialog.askopenfilenames()

    for image_path in file_paths:
        image = Image.open(image_path).convert('RGB')
        transformed_image = ai_image_detector.transform(image).unsqueeze(0)
        with torch.no_grad():
            output = trained_model(transformed_image)
            _, predicted = torch.max(output, 1)

            if predicted.item() == 0:
                image.save("predicted_ai_images/" + os.path.basename(image_path))
            else:
                image.save("predicted_real_images/" + os.path.basename(image_path))


add_base_widgets()
root.mainloop()
