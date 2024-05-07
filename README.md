# Lyceum Nugegoda Branch - Innovate4Impact AI For Good Challenge

## Project: AI for Good - Ethical Considerations

![Project Logo/Icon](logo.png)

### Team: LNU (Lyceum Nugegoda Branch)

---

## Table of Contents

- [Overview](#overview)
- [Programs](#programs)
    - [1. Image Protection Software](#1-image-protection-software)
    - [2. AI Image Detector](#2-ai-image-detector)
    - [3. AI Art Assistant](#3-ai-art-assistant)
- [Installation](#installation)
    - [Image Protection Software](#image-protection-software)
    - [AI Image Detector](#ai-image-detector)
    - [AI Art Assistant](#ai-art-assistant)
- [Usage](#usage)
- [License](#license)

---

## Overview

The Lyceum Nugegoda Branch team, participating in the Innovate4Impact AI For Good Challenge, presents a project focusing on ethical considerations in AI. Our goal is to address issues related to AI through the development of concept programs with a positive impact.

---

## Programs

### 1. Image Protection Software

Protecting the work of artists from unauthorized usage is our primary concern. Our Image Protection Software aims to safeguard artists' creations from being misused by AI art programs. In our image protection software, we use the 'PIL' python library to encrypt each and every pixel based on an encryption key stored in the key.key file. This shows a image with random colored pixels for both the user and AI model. However, using the decryption algorithm with the same key will decrypt the image back to normal for websites and users.

### 2. AI Image Detector

The AI Image Detector is designed to identify and analyze images, contributing to various applications such as content moderation, object recognition, and more. We use libraries like PyTorch to create a neural network to train on datasets to identify AI generated art and deepfakes.

### 3. AI Art Assistant

The AI Art Assistant is a simple program that uses Stable Diffusion (SD) to generate a sketch. The program then allows the user to draw on top of the sketch in the art program. This is currently a proof of concept and prototype. Future implementations will includes the ability for the user to draw a sketch (or pose) and export the image to SD which will return a completed version of the sketch. The purpose of this program is not to complete drawings for the user but instead assist them and make the artist's job more efficient.

---

## Installation

### Image Protection Software

Download and run the ImageProtector.exe file to setup the Image Protector application. Next, use the key_gen python file to generate a key.key file and place it in the directory where the Image Protector is installed (by default, the Image Protector is installed in "C:\Users\User\AppData\Local\Programs\"; in this case, place the key.key file must be place in "C:\Users\User\AppData\Local\Programs\Image Protector")

### AI Image Detector

Download the entire folder as a zip. Install all the libraries in the requirements.txt and run the main.py


### AI Art Assistant

Download the entire folder as a zip. Install all the libraries in the requirements.txt and run the main.py


## Usage

### Image Protection Software

Simply import a png into the software using the Open Image. Press the Protect button and wait for the .safepng version of the file to be outputed in the same folder as the selected png (make sure the key.key is present)
For the decryption processs, check out the decryption.py file.


### AI Image Detector

Use the Load Image button to import an image into the program. Press Detect image to check whether it is Real or AI. 
Batch Detect allows you to sort the images into the two folders, "predicted_ai_images" and "predicted_real_images"


### AI Art Assistant

Since this is a prototype, many features are yet to be implemented. To generate an AI Image on to the background, press the "Generate AI image" button and input your prompt. SD should generate an AI image.

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE.md). See the LICENSE file for details.

---
