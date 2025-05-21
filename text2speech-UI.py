import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import PyPDF2
import pyttsx3
import time

class PDFReaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Audio Reader")
        self.master.geometry("400x320")
        
        # TTS Engine management
        self.engine = None
        self.paused = False
        self.stop_flag = False
        self.current_text = []
        self.text_position = 0
        self.engine_lock = threading.Lock()
        self.current_page = 0  # Track current page
        
        # GUI setup
        self.create_widgets()
    
    def create_widgets(self):
        # File Selection
        self.file_frame = tk.Frame(self.master)
        self.file_frame.pack(pady=10)
        
        self.btn_open = tk.Button(self.file_frame, text="Open PDF", command=self.open_pdf)
        self.btn_open.pack(side=tk.LEFT, padx=5)
        self.lbl_file = tk.Label(self.file_frame, text="No file selected")
        self.lbl_file.pack(side=tk.LEFT)
        
        # Page Selection
        self.page_frame = tk.Frame(self.master)
        self.page_frame.pack(pady=5)
        self.lbl_page = tk.Label(self.page_frame, text="Start Page:")
        self.lbl_page.pack(side=tk.LEFT)
        self.entry_page = tk.Entry(self.page_frame, width=5)
        self.entry_page.pack(side=tk.LEFT, padx=5)
        self.entry_page.insert(0, "1")
        
        # Controls
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(pady=15)
        self.btn_start = tk.Button(self.control_frame, text="Start", command=self.start_reading)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        self.btn_pause = tk.Button(self.control_frame, text="Pause", 
                                 command=self.toggle_pause, state=tk.DISABLED)
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_frame = tk.Frame(self.master)
        self.status_frame.pack(pady=10)
        self.lbl_status = tk.Label(self.status_frame, text="Status: Ready")
        self.lbl_status.pack(side=tk.LEFT)
        self.lbl_current_page = tk.Label(self.status_frame, text=" | Current Page: -", fg="blue")
        self.lbl_current_page.pack(side=tk.LEFT)
    
    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path = file_path
            self.lbl_file.config(text=file_path.split("/")[-1])
    
    def extract_text(self, start_page):
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if start_page < 1 or start_page > len(reader.pages):
                    raise ValueError(f"Invalid start page (1-{len(reader.pages)})")
                
                text_with_pages = []
                for page_num in range(start_page-1, len(reader.pages)):
                    raw_text = reader.pages[page_num].extract_text()
                    if cleaned := raw_text.strip():
                        cleaned_text = cleaned.replace('\t', ' ')
                        # Store sentences with their original page number (+1 for user-facing numbering)
                        page_display_num = page_num + 1
                        for sentence in cleaned_text.split('. '):
                            if stripped := sentence.strip():
                                text_with_pages.append((stripped, page_display_num))
                
                return text_with_pages if text_with_pages else None
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
    
    def start_reading(self):
        if not hasattr(self, 'pdf_path'):
            messagebox.showwarning("Warning", "Please select a PDF file first")
            return
        
        try:
            start_page = int(self.entry_page.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid page number")
            return
        
        text_with_pages = self.extract_text(start_page)
        if not text_with_pages:
            messagebox.showinfo("Info", "No readable text found")
            return
        
        self.current_text = text_with_pages
        self.text_position = 0
        self.current_page = 0
        self.stop_flag = False
        self.paused = False
        self.btn_start.config(state=tk.DISABLED)
        self.btn_pause.config(state=tk.NORMAL)
        self.lbl_status.config(text="Status: Reading")
        self.update_page_display(-1)  # Reset display
        
        # Start reading thread
        self.read_thread = threading.Thread(target=self.safe_read_aloud)
        self.read_thread.start()
    
    def safe_read_aloud(self):
        """Thread-safe reading with page tracking"""
        with self.engine_lock:
            try:
                if self.engine and self.engine._inLoop:
                    self.engine.endLoop()
                
                self.engine = pyttsx3.init()
                self.engine.setProperty('voice', 'com.apple.voice.compact.en-US.Samantha')
                self.engine.setProperty('rate', self.engine.getProperty('rate') - 50)
                
                self.engine.startLoop(False)
                last_page = -1
                
                for i in range(self.text_position, len(self.current_text)):
                    if self.stop_flag:
                        break
                        
                    while self.paused and not self.stop_flag:
                        time.sleep(0.1)
                    
                    sentence, page_number = self.current_text[i]
                    
                    # Update page display if page changed
                    if page_number != last_page:
                        last_page = page_number
                        self.master.after(0, self.update_page_display, page_number)
                    
                    self.engine.say(sentence)
                    while self.engine.isBusy() and not self.stop_flag:
                        self.engine.iterate()
                        time.sleep(0.1)
                    
                    self.text_position = i
                
                self.engine.endLoop()
                
            except RuntimeError as e:
                messagebox.showerror("Audio Error", f"Restarting engine: {str(e)}")
                self.engine = None
            finally:
                self.master.after(0, self.reset_controls)
    
    def update_page_display(self, page_number):
        """Update the current page display in the GUI"""
        self.lbl_current_page.config(text=f" | Current Page: {page_number}" if page_number != -1 else " | Current Page: -")
    
    def toggle_pause(self):
        self.paused = not self.paused
        self.btn_pause.config(text="Resume" if self.paused else "Pause")
        self.lbl_status.config(text="Status: Paused" if self.paused else "Status: Reading")

    def reset_controls(self):
        if self.engine and self.engine._inLoop:
            self.engine.endLoop()
        self.engine = None
        self.btn_start.config(state=tk.NORMAL)
        self.btn_pause.config(state=tk.DISABLED)
        self.lbl_status.config(text="Status: Ready")
        self.update_page_display(-1)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()
