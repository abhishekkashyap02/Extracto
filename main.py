import tkinter as tk
from tkinter import filedialog
import PyPDF2
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import os

# Function to extract content from a PDF
def extract_pdf_content():
    # Ask the user to select a file
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    
    if file_path:
        print(f"Selected PDF: {file_path}")  # Debug: Check if file is selected
        
        # Extract Text or Images or Both based on user selection
        if app.extraction_type.get() == "Text Only":
            extract_text(file_path)  # First extract text
        elif app.extraction_type.get() == "Images Only":
            extract_images(file_path)  # Then extract images
        elif app.extraction_type.get() == "Text and Images":
            extract_text(file_path)  # First extract text
            extract_images(file_path)  # Then extract images

# Function to extract text from PDF
def extract_text(file_path):
    print(f"Extracting text from: {file_path}")  # Debug: Confirm text extraction
    pdf_file = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create a text file for saving extracted text
    txt_file_path = file_path.replace(".pdf", "_text.txt")
    txt_file = open(txt_file_path, 'w', encoding='utf-8')

    # Loop through each page and extract text
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        if text:  # Check if text is not None
            txt_file.write(text)

    txt_file.close()
    pdf_file.close()

    # Update the information displayed in the UI
    app.update_info(file_path, txt_file_path, None)

# Function to extract images from PDF
def extract_images(file_path):
    print(f"Extracting images from: {file_path}")  # Debug: Confirm image extraction
    # Create directory for images
    image_dir = file_path.replace(".pdf", "_images/")
    os.makedirs(image_dir, exist_ok=True)  # Create the directory if it doesn't exist

    # Extract images from PDF
    pdf_document = fitz.open(file_path)
    
    image_extracted = False  # Flag to track if any images were extracted
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
                image_extracted = True  # Mark that at least one image was extracted

    if image_extracted:
        print(f"Images saved to: {image_dir}")  # Debug: Confirm images were extracted
        app.update_info(file_path, None, image_dir)
    else:
        print("No images found in this PDF.")  # Debug: No images found in PDF

# Update the information in the text box with colored tags
def update_info(input_file, output_text_file, image_dir):
    app.info_text.config(state=tk.NORMAL)
    app.info_text.delete('1.0', tk.END)  # Clear existing text
    app.info_text.insert(tk.END, f"Input File: {input_file}\n")
    if output_text_file:
        app.info_text.insert(tk.END, f"Text File: {output_text_file}\n")
    if image_dir:
        app.info_text.insert(tk.END, f"Images Folder: {image_dir}\n")

    app.info_text.config(state=tk.DISABLED)

# Main GUI class
class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text and Image Extractor")
        self.root.geometry("1166x718")
        self.root.resizable(0, 0)

        # Set Background Image (Optional - replace with your own image)
        self.bg_image = Image.open("images\\background1.png")  # Add your background image path here
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_panel = tk.Label(self.root, image=self.bg_photo)
        self.bg_panel.image = self.bg_photo
        self.bg_panel.place(relwidth=1, relheight=1)

        # Create a frame for the main content
        self.main_frame = tk.Frame(self.root, bg="#2a2a2a", width=950, height=600)
        self.main_frame.place(x=100, y=50)

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="Extract Text and Images from PDF", font=("Helvetica", 24, "bold"), fg="white", bg="#2a2a2a")
        self.title_label.pack(pady=30)

        # Selection Frame for extraction type
        self.selection_frame = tk.Frame(self.main_frame, bg="#2a2a2a")
        self.selection_frame.pack(pady=20)

        self.extraction_type_label = tk.Label(self.selection_frame, text="Select Extraction Type:", font=("Helvetica", 14), fg="white", bg="#2a2a2a")
        self.extraction_type_label.grid(row=0, column=0, padx=10)

        # Create Buttons for extraction types
        self.extraction_type = tk.StringVar(value="Text and Images")  # Default to extracting both

        # Button to extract Text Only
        self.text_only_button = tk.Button(self.selection_frame, text="Text Only", font=("Helvetica", 12), fg="white", bg="#3047ff", relief="flat", width=15, height=2, command=lambda: self.select_extraction_type("Text Only"))
        self.text_only_button.grid(row=0, column=1, padx=15)
        
        # Button to extract Text and Images
        self.text_and_images_button = tk.Button(self.selection_frame, text="Text and Images", font=("Helvetica", 12), fg="white", bg="#3047ff", relief="flat", width=15, height=2, command=lambda: self.select_extraction_type("Text and Images"))
        self.text_and_images_button.grid(row=0, column=2, padx=15)

        # Button to extract Images Only
        self.images_only_button = tk.Button(self.selection_frame, text="Images Only", font=("Helvetica", 12), fg="white", bg="#3047ff", relief="flat", width=15, height=2, command=lambda: self.select_extraction_type("Images Only"))
        self.images_only_button.grid(row=0, column=3, padx=15)

        # Hover effects for the buttons
        self.add_hover_effect(self.text_only_button)
        self.add_hover_effect(self.text_and_images_button)
        self.add_hover_effect(self.images_only_button)

        # PDF Button
        self.pdf_button = tk.Button(self.main_frame, text="Browse PDF", font=("Helvetica", 16), fg="white", bg="#5C6BC0", command=extract_pdf_content, relief="flat", cursor="hand2", width=20, height=2)
        self.pdf_button.pack(pady=30)

        # Info Text Box
        self.info_text = tk.Text(self.main_frame, width=45, height=15, font=("Helvetica", 12), wrap=tk.WORD, state=tk.DISABLED, bg="#1e1e1e", fg="white", relief="flat")
        self.info_text.pack(padx=10, pady=20)

        # Bottom Buttons Frame
        self.bottom_frame = tk.Frame(self.main_frame, bg="#2a2a2a")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        # Footer Info
        self.footer_label = tk.Label(self.bottom_frame, text="Made with ❤️ by Abhishek Kashyap", font=("Helvetica", 12), fg="white", bg="#2a2a2a")
        self.footer_label.pack()

    # Method to handle extraction type selection
    def select_extraction_type(self, extraction):
        # Update the extraction type
        self.extraction_type.set(extraction)
        
        # Change button colors to reflect selection
        self.reset_button_colors()
        
        if extraction == "Text Only":
            self.text_only_button.config(bg="#3f51b5")  # Selected color for Text Only
        elif extraction == "Text and Images":
            self.text_and_images_button.config(bg="#3f51b5")  # Selected color for Text and Images
        elif extraction == "Images Only":
            self.images_only_button.config(bg="#3f51b5")  # Selected color for Images Only

    # Reset button colors to default
    def reset_button_colors(self):
        self.text_only_button.config(bg="#3047ff")
        self.text_and_images_button.config(bg="#3047ff")
        self.images_only_button.config(bg="#3047ff")

    # Hover effect methods for buttons
    def add_hover_effect(self, button):
        button.bind("<Enter>", lambda e: button.config(bg="#3f51b5"))  # Darker shade on hover
        button.bind("<Leave>", lambda e: button.config(bg="#3047ff"))  # Original shade when not hovering

# Create and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFExtractorApp(root)
    app.update_info = update_info  # This line ensures that update_info is set to the correct function
    root.mainloop()
