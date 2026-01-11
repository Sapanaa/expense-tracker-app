# 🧾 Automated Expense Tracker using OCR & Computer Vision

An end-to-end application that scans receipt images, extracts item-level expenses using computer vision and OCR, and calculates totals automatically.

This project demonstrates a **real-world OCR pipeline** with clean backend architecture and production-ready design.

---

## ✨ Features

- 📸 Receipt scanning with perspective correction
- 🧠 Adaptive image preprocessing for different bill types
- 🔍 OCR text extraction using Tesseract
- 🧾 Item, price, and total detection
- ⚖️ Automatic mismatch detection (calculated vs printed total)
- 🌐 REST API built with FastAPI
- 🎨 Streamlit frontend for quick testing
- 🚀 Production-ready backend architecture

---

## 🏗 Architecture Overview

Image Upload
↓
Document Scanner (OpenCV)
↓
Image Cleaner (Adaptive Thresholding)
↓
OCR Engine (Tesseract)
↓
Text Parser
↓
Expense Summary (JSON)
---

## 🧰 Tech Stack

| Layer | Technology |
|------|----------|
| Computer Vision | OpenCV |
| OCR | Tesseract + pytesseract |
| Backend | FastAPI |
| Frontend | Streamlit |
| Language | Python |
| Image Processing | NumPy |
| Deployment Ready | Docker (planned) |

---


---

## ⚙️ How It Works

### 1️⃣ Document Scanner
- Detects the **largest rectangular contour**
- Applies perspective transformation
- Falls back to original image if scanning fails

### 2️⃣ Image Cleaner
- Uses adaptive thresholding
- Handles uneven lighting and backgrounds
- Improves OCR accuracy

### 3️⃣ OCR Engine
- Extracts raw text from cleaned images
- Uses fallback strategy if OCR fails

### 4️⃣ Text Parser
- Extracts item names and prices
- Ignores tax and subtotal lines
- Calculates total and compares with detected total

---

## 🚀 Installation

```bash
git clone https://github.com/your-username/expense-tracker-app.git
cd expense-tracker-app

python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt


