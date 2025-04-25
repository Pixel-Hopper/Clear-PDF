import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
from pathlib import Path
import fitz  # PyMuPDF

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    messagebox.showerror("Missing Package", "Please install tkinterdnd2:\n\npip install tkinterdnd2")
    raise

selected_files = []

def clean_pdf(input_path, output_path, password=None, dpi=150):
    try:
        doc = fitz.open(input_path)
    except RuntimeError as e:
        if 'password' in str(e).lower() and password:
            doc = fitz.open(input_path, password=password)
        else:
            messagebox.showerror("Error", f"Failed to open PDF: {e}")
            return

    new_pdf = fitz.open()
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        img_pdf = fitz.open()
        img_page = img_pdf.new_page(width=pix.width, height=pix.height)
        img_page.insert_image(img_page.rect, pixmap=pix)
        new_pdf.insert_pdf(img_pdf)

    new_pdf.save(output_path)

def browse_files():
    files = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF Files", "*.pdf")]
    )
    for file in files:
        add_file(file)

def add_file(file):
    if file.lower().endswith(".pdf") and file not in selected_files:
        selected_files.append(file)
        file_listbox.insert(tk.END, file)

def on_drop(event):
    print(f"Dropped: {event.data}")  # Debug line
    files = root.tk.splitlist(event.data)
    for file in files:
        add_file(file)

def choose_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_folder.set(folder)

def process_all_pdfs():
    if not selected_files:
        messagebox.showwarning("No Files", "Please add at least one PDF file.")
        return

    out_dir = Path(output_folder.get()) if output_folder.get() else None

    for file in selected_files:
        in_path = Path(file)
        output_dir = out_dir or in_path.parent
        out_file = output_dir / f"{in_path.stem}_CLEAN.pdf"
        clean_pdf(in_path, out_file)

    messagebox.showinfo("Done", f"Processed {len(selected_files)} PDF successfully.")

def clear_file_list():
    selected_files.clear()
    file_listbox.delete(0, tk.END)

# --- GUI Setup ---
root = TkinterDnD.Tk()
root.title("")
root.geometry("640x360")

output_folder = tk.StringVar()

tk.Label(root, text="Drop or browse PDF files:").pack(pady=5)

file_frame = tk.Frame(root)
file_frame.pack(padx=10, fill="both", expand=True)

scrollbar = Scrollbar(file_frame)
scrollbar.pack(side="right", fill="y")

file_listbox = Listbox(file_frame, selectmode="multiple", yscrollcommand=scrollbar.set)
file_listbox.pack(fill="both", expand=True)
scrollbar.config(command=file_listbox.yview)

# Register drag-and-drop on the root instead of file_listbox
root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop:DND_Files>>", on_drop)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Browse", command=browse_files).pack(side="left", padx=5)
tk.Button(btn_frame, text="Output", command=choose_output_folder).pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear", command=clear_file_list).pack(side="left", padx=5)
tk.Button(btn_frame, text="Export", command=process_all_pdfs).pack(side="left", padx=5)

root.mainloop()
