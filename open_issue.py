import tkinter as tk
from tkinter import ttk, messagebox
import os
import webbrowser
import platform
import subprocess
from urllib.parse import quote, unquote

class PDFBrowserViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("IMM Issues Browser")
        self.root.resizable(False, False)
        self.setup_ui()
        
        # Configure modern styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

    def configure_styles(self):
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', 
                            foreground='#333333', font=('Segoe UI', 10))
        self.style.configure('TEntry', fieldbackground='white', 
                            font=('Segoe UI', 10))
        self.style.configure('Primary.TButton', background='#0078D4', 
                            foreground='white', font=('Segoe UI', 10, 'bold'))
        self.style.map('Primary.TButton', 
                      background=[('active', '#005499'), ('disabled', '#cccccc')])

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input fields
        fields = [("Year", "1869"), ("Month", "01"), ("Page", "1")]
        self.entries = {}
        
        for i, (label, default) in enumerate(fields):
            ttk.Label(main_frame, text=f"{label}:").grid(row=i, column=0, 
                                                       padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(main_frame, width=10)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=tk.EW)
            self.entries[label.lower()] = entry

        # Open button
        ttk.Button(main_frame, text="Open PDF", 
                  style='Primary.TButton', command=self.open_pdf
                  ).grid(row=3, column=0, columnspan=2, pady=15, sticky=tk.EW)

        main_frame.columnconfigure(1, weight=1)

    def validate_inputs(self):
        try:
            year = int(self.entries['year'].get())
            month = int(self.entries['month'].get())
            page = int(self.entries['page'].get())
            
            if not (1869 <= year <= 2100):
                raise ValueError("Year out of valid range (1869-2100)")
            if not (1 <= month <= 12):
                raise ValueError("Month must be between 1-12")
            if page < 1:
                raise ValueError("Page number must be at least 1")
                
            return year, month, page
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None

    def open_pdf(self):
        inputs = self.validate_inputs()
        if not inputs:
            return
            
        year, month, page = inputs
        filename = f"{year}_{month:02d}.pdf"
        
        try:
            # Get the user's Documents directory path properly
            docs_dir = os.path.expanduser('~/Documents')
            filepath = os.path.join(docs_dir, "IMM_issues", filename)
            
            # Verify file exists and is accessible
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filename}")
            if not os.access(filepath, os.R_OK):
                raise PermissionError(f"No read access to: {filename}")

            # Platform-specific handling
            if platform.system() == 'Darwin':
                self.open_macos(filepath, page)
            elif platform.system() == 'Windows':
                self.open_windows(filepath, page)
            else:
                self.open_linux(filepath, page)

        except Exception as e:
            self.show_error(e, filepath)

    def open_macos(self, filepath, page):
        """Handle macOS security restrictions with multiple fallbacks"""
        # try:
        #     # First try with NSWorkspace for proper permissions
        #     from AppKit import NSWorkspace, NSURL
        #     url = NSURL.fileURLWithPath_(filepath)
        #     success = NSWorkspace.sharedWorkspace().openURL_(url)
        #     if not success:
        #         raise RuntimeError("Failed to open with native API")
        # except ImportError:
        try:
            # Fallback to browser with proper encoding
            file_uri = f'file://{quote(filepath)}#page={page}'
            webbrowser.open_new_tab(file_uri)
        except:
            # Final fallback to AppleScript
            script = f'''
            tell application "Finder"
                set theFile to POSIX file "{filepath}" as alias
                open theFile
            end tell
            '''
            subprocess.run(['osascript', '-e', script])

    def open_windows(self, filepath, page):
        """Windows-specific opening with proper encoding"""
        try:
            file_uri = f'file:///{quote(filepath.replace("\\", "/"))}#page={page}'
            webbrowser.open_new_tab(file_uri)
        except Exception:
            os.startfile(filepath)

    def open_linux(self, filepath, page):
        """Linux handling with xdg-open"""
        try:
            subprocess.run(['xdg-open', filepath])
        except Exception:
            webbrowser.open_new_tab(f'file://{filepath}')

    def show_error(self, error, filepath):
        """User-friendly error display with troubleshooting tips"""
        docs_dir = os.path.expanduser('~/Documents')
        troubleshooting = (
            "Troubleshooting steps:\n"
            f"1. Verify file exists at: {filepath}\n"
            f"2. Check permissions in terminal: ls -l '{filepath}'\n"
            "3. Try opening manually in your PDF viewer\n"
            "4. On macOS: Grant Full Disk Access to your terminal/IDE\n"
            "   (System Settings → Privacy & Security → Full Disk Access)"
        )
        
        messagebox.showerror(
            "Open Failed",
            f"Failed to open PDF:\n{str(error)}\n\n{troubleshooting}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFBrowserViewer(root)
    root.mainloop()