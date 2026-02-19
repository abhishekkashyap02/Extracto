import tkinter as tk
from tkinter import filedialog
import PyPDF2
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

# Function to extract content from a PDF
def extract_pdf_content():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        print(f"Selected PDF: {file_path}")
        
        if app.extraction_type.get() == "Text Only":
            extract_text(file_path)
        elif app.extraction_type.get() == "Images Only":
            extract_images(file_path)
        elif app.extraction_type.get() == "Text and Images":
            extract_text(file_path)
            extract_images(file_path)

# Function to extract text from PDF
def extract_text(file_path):
    print(f"Extracting text from: {file_path}")
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Updated with Extracto branding
    txt_file_path = file_path.replace(".pdf", "_extracto_text.txt")
    txt_file = open(txt_file_path, 'w', encoding='utf-8')

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        if text:
            txt_file.write(text)

    txt_file.close()
    pdf_file.close()

    app.update_info(file_path, txt_file_path, None)

# Function to extract images from PDF
def extract_images(file_path):
    print(f"Extracting images from: {file_path}")
    
    # Updated with Extracto branding
    image_dir = file_path.replace(".pdf", "_extracto_images/")
    os.makedirs(image_dir, exist_ok=True)

    pdf_document = fitz.open(file_path)
    
    image_extracted = False
    for i in range(len(pdf_document)):
        page = pdf_document.load_page(i)
        images = page.get_images(full=True)

        for image_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"{image_dir}page_{i+1}_img_{image_index+1}.{image_ext}"
            
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
                image_extracted = True

    if image_extracted:
        print(f"Images saved to: {image_dir}")
        app.update_info(file_path, None, image_dir)
    else:
        print("No images found in this PDF.")

# Update the information in the text box
def update_info(input_file, output_text_file, image_dir):
    app.info_text.config(state=tk.NORMAL)
    app.info_text.delete('1.0', tk.END)
    app.info_text.insert(tk.END, f"Input File: {input_file}\n")
    if output_text_file:
        app.info_text.insert(tk.END, f"Text File: {output_text_file}\n")
    if image_dir:
        app.info_text.insert(tk.END, f"Images Folder: {image_dir}\n")
    app.info_text.config(state=tk.DISABLED)

# Main GUI class
class ExtractoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extracto")
        self.root.geometry("1166x718")
        self.root.resizable(0, 0)

        # Background Image
        self.bg_image = Image.open("images\\background1.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_panel = tk.Label(self.root, image=self.bg_photo)
        self.bg_panel.image = self.bg_photo
        self.bg_panel.place(relwidth=1, relheight=1)

        # Main Frame
        self.main_frame = tk.Frame(self.root, bg="#2a2a2a", width=950, height=600)
        self.main_frame.place(x=100, y=50)

        # Title Label
        self.title_label = tk.Label(
            self.main_frame,
            text="Extracto - PDF Text & Image Extractor",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#2a2a2a"
        )
        self.title_label.pack(pady=30)

        # Selection Frame
        self.selection_frame = tk.Frame(self.main_frame, bg="#2a2a2a")
        self.selection_frame.pack(pady=20)

        self.extraction_type_label = tk.Label(
            self.selection_frame,
            text="Select Extraction Type:",
            font=("Helvetica", 14),
            fg="white",
            bg="#2a2a2a"
        )
        self.extraction_type_label.grid(row=0, column=0, padx=10)

        self.extraction_type = tk.StringVar(value="Text and Images")

        self.text_only_button = tk.Button(
            self.selection_frame, text="Text Only",
            font=("Helvetica", 12), fg="white",
            bg="#3047ff", relief="flat",
            width=15, height=2,
            command=lambda: self.select_extraction_type("Text Only")
        )
        self.text_only_button.grid(row=0, column=1, padx=15)

        self.text_and_images_button = tk.Button(
            self.selection_frame, text="Text and Images",
            font=("Helvetica", 12), fg="white",
            bg="#3047ff", relief="flat",
            width=15, height=2,
            command=lambda: self.select_extraction_type("Text and Images")
        )
        self.text_and_images_button.grid(row=0, column=2, padx=15)

        self.images_only_button = tk.Button(
            self.selection_frame, text="Images Only",
            font=("Helvetica", 12), fg="white",
            bg="#3047ff", relief="flat",
            width=15, height=2,
            command=lambda: self.select_extraction_type("Images Only")
        )
        self.images_only_button.grid(row=0, column=3, padx=15)

        self.add_hover_effect(self.text_only_button)
        self.add_hover_effect(self.text_and_images_button)
        self.add_hover_effect(self.images_only_button)

        # Browse Button
        self.pdf_button = tk.Button(
            self.main_frame,
            text="Browse PDF",
            font=("Helvetica", 16),
            fg="white",
            bg="#5C6BC0",
            command=extract_pdf_content,
            relief="flat",
            cursor="hand2",
            width=20,
            height=2
        )
        self.pdf_button.pack(pady=30)

        # Info Box
        self.info_text = tk.Text(
            self.main_frame,
            width=45,
            height=15,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#1e1e1e",
            fg="white",
            relief="flat"
        )
        self.info_text.pack(padx=10, pady=20)

        # Footer
        self.bottom_frame = tk.Frame(self.main_frame, bg="#2a2a2a")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.footer_label = tk.Label(
            self.bottom_frame,
            text="Extracto | Made with ❤️ by Abhishek Kashyap",
            font=("Helvetica", 12),
            fg="white",
            bg="#2a2a2a"
        )
        self.footer_label.pack()

    def select_extraction_type(self, extraction):
        self.extraction_type.set(extraction)
        self.reset_button_colors()

        if extraction == "Text Only":
            self.text_only_button.config(bg="#3f51b5")
        elif extraction == "Text and Images":
            self.text_and_images_button.config(bg="#3f51b5")
        elif extraction == "Images Only":
            self.images_only_button.config(bg="#3f51b5")

    def reset_button_colors(self):
        self.text_only_button.config(bg="#3047ff")
        self.text_and_images_button.config(bg="#3047ff")
        self.images_only_button.config(bg="#3047ff")

    def add_hover_effect(self, button):
        button.bind("<Enter>", lambda e: button.config(bg="#3f51b5"))
        button.bind("<Leave>", lambda e: button.config(bg="#3047ff"))

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = ExtractoApp(root)
    app.update_info = update_info
    root.mainloop()
