# Speech Recognition with TensorFlow Lite on Raspberry Pi

![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi-C51A4A?logo=raspberry-pi)
![Framework](https://img.shields.io/badge/Framework-TensorFlow%20Lite-FF6F00?logo=tensorflow)
![Course](https://img.shields.io/badge/PolyU-EIE4433-blue)

This repository contains the implementation and deployment codes for my **EIE4433 Honours Project** at **The Hong Kong Polytechnic University (PolyU)**. The project focuses on deploying a lightweight Deep Learning model for real-time speech recognition on embedded edge devices.

## 🏆 Award & Recognition

> [!IMPORTANT]
> This project was selected as one of the **"2023 Outstanding Works by Students"** by The Hong Kong Polytechnic University.

The work is officially showcased in the PolyU Library collection:
🔗 **[View Project Showcase: Smart Security Robot](https://ows.lib.polyu.edu.hk/s/ows/page/smart-security-robot)**

---

## 📖 Project Overview

This project demonstrates the end-to-end pipeline of training a speech recognition model and deploying it on a Raspberry Pi using **TensorFlow Lite (TFLite)**.

**Key Features:**
* **Model Architecture:** Lightweight CNN/RNN optimized for edge inference.
* **Optimization:** Quantization (Float16 / Int8) to reduce model size and latency.
* **Hardware:** Raspberry Pi (3B+/4B) with USB Microphone.
* **Performance:** Real-time inference with low latency (<100ms) and high accuracy on keyword spotting tasks.

## 🛠️ Hardware & Software Requirements

### Hardware
* **Raspberry Pi** (3B+ or 4B recommended)
* **USB Microphone** (or ReSpeaker HAT)
* MicroSD Card (16GB+ with Raspberry Pi OS)

### Software Dependencies
* Python 3.7+
* TensorFlow Lite Runtime
* PyAudio / SoundDevice
* NumPy

## 🚀 Installation & Setup

### 1. Clone the Repository
Open the terminal on your Raspberry Pi and clone this project:
```bash
git clone [https://github.com/Zilai-WANG/EIE4433-Speech-Recognition-of-tensorflow-Lite-on-Raspberry-pi.git](https://github.com/Zilai-WANG/EIE4433-Speech-Recognition-of-tensorflow-Lite-on-Raspberry-pi.git)
cd EIE4433-Speech-Recognition-of-tensorflow-Lite-on-Raspberry-pi
