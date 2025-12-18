# 📄 PDF Text & Image Extractor (GUI Application)

A Python-based desktop GUI application that allows users to extract text, images, or both from PDF files using a clean and interactive interface built with Tkinter.

This tool automatically saves:
- 📄 Extracted text as a `.txt` file
- 🖼️ Extracted images into a separate folder

---

## 🚀 Features

- 📑 Extract Text Only from PDF
- 🖼️ Extract Images Only from PDF
- 📄🖼️ Extract Text and Images Together
- 🖥️ User-friendly Tkinter GUI
- 📁 Automatic output file and folder creation
- 🎨 Modern UI with hover effects and background image
- ⚡ Fast and efficient PDF processing

---

## 🛠️ Tech Stack

- Python 3
- Tkinter – GUI
- PyPDF2 – Text extraction
- PyMuPDF (fitz) – Image extraction
- Pillow (PIL) – Image handling
- OS module – File system operations

---

## 📦 Required Packages (Install Before Running)

```bash
pip install PyPDF2
pip install pymupdf
pip install pillow


```

---

## ⚠️ IMPORTANT NOTES (MUST READ)

### ⚠️ Tkinter
- Tkinter comes pre-installed with Python
- No separate installation is required

### ⚠️ Python Version
- Use Python 3.8 or above

### ⚠️ Background Image Requirement
- Ensure the following file exists:
```
images/background1.png
```
- Missing this file may cause the application to crash on startup

### ⚠️ PDF Limitations
- Text extraction works only for text-based PDFs
- Image extraction works only for embedded images
- OCR for scanned PDFs is not included

---

## 📂 Project Structure

```
pdf-text-image-extractor/
│
├── main.py
├── images/
│   └── background1.png
├── README.md
```

---

## ▶️ How to Run the Project

### Step 1: Clone the Repository
```
git clone https://github.com/your-username/pdf-text-image-extractor.git
```

### Step 2: Navigate to Project Folder
```
cd pdf-text-image-extractor
```

### Step 3: Install Required Libraries
```
pip install PyPDF2 pymupdf pillow
```

### Step 4: Run the Application
```
python main.py
```

---

## 🖥️ How the Application Works

1. Launch the application
2. Click Browse PDF
3. Select a PDF file
4. Choose extraction type:
   - Text Only
   - Images Only
   - Text and Images
5. Output files are saved automatically

---

## 📌 Output Example

```
sample.pdf
sample_text.txt
sample_images/
 ├── page_1_img_1.png
 ├── page_2_img_1.jpg
```

---

## 🔮 Future Enhancements

- OCR support for scanned PDFs
- Table extraction
- ZIP export for images
- Keyword extraction and summarization
- JSON export support
- Web version using Flask

---

## 👨‍💻 Author

Abhishek Kashyap  
B.Tech – Computer Science Engineering  
SRM Institute of Science and Technology

---

## ⭐ Support

- Star the repository
- Fork and contribute
- Improve the project

Happy Coding 🚀
```







