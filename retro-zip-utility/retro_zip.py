#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  RETRO ZIP UTILITY v1.0 - The Ultimate Archive Manager!          ║
║  ════════════════════════════════════════════════════════════    ║
║  A nostalgic trip back to the golden age of the web!             ║
║  Now with DRAG & DROP technology!                                 ║
╚══════════════════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import zipfile
import os
import sys
import threading
import time
import hashlib
from datetime import datetime
from pathlib import Path
import tempfile
import shutil
import json

# Try to import optional dependencies
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False

try:
    import pyzipper
    HAS_ENCRYPTION = True
except ImportError:
    HAS_ENCRYPTION = False


class RetroZipUtility:
    """Main application class for the Retro ZIP Utility."""

    # Retro color scheme - classic 90s web vibes
    COLORS = {
        'bg_dark': '#000080',        # Navy blue
        'bg_medium': '#008080',      # Teal
        'bg_light': '#C0C0C0',       # Silver
        'accent': '#FF00FF',         # Magenta
        'accent2': '#00FF00',        # Lime
        'warning': '#FF0000',        # Red
        'text_dark': '#000000',
        'text_light': '#FFFFFF',
        'link': '#0000FF',
        'visited': '#800080',
        'button_face': '#C0C0C0',
        'button_shadow': '#808080',
        'button_highlight': '#FFFFFF',
        'marquee': '#FFFF00',        # Yellow
        'cyan': '#00FFFF',
    }

    def __init__(self):
        # Create main window with drag-drop support if available
        if HAS_DND:
            self.root = TkinterDnD.Tk()
        else:
            self.root = tk.Tk()

        self.root.title("★ RETRO ZIP UTILITY v1.0 ★ - Your #1 Archive Solution!")
        self.root.geometry("900x700")
        self.root.configure(bg=self.COLORS['bg_dark'])

        # Application state
        self.current_archive = None
        self.archive_contents = []
        self.selected_items = []
        self.history = []
        self.compression_level = 6
        self.is_processing = False

        # Settings
        self.settings = {
            'last_directory': os.path.expanduser('~'),
            'show_hidden': False,
            'confirm_overwrite': True,
            'remember_password': False,
            'theme': 'classic'
        }
        self.load_settings()

        # Build the UI
        self.create_widgets()
        self.setup_bindings()

        # Start the marquee animation
        self.marquee_pos = 0
        self.animate_marquee()

        # Blinking cursor effect
        self.blink_state = True
        self.animate_blink()

    def create_widgets(self):
        """Create all UI widgets with retro styling."""

        # === TOP BANNER ===
        self.create_banner()

        # === TOOLBAR ===
        self.create_toolbar()

        # === MAIN CONTENT ===
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg_light'],
                             relief='sunken', bd=3)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left panel - File list
        self.create_file_panel(main_frame)

        # Right panel - Details and actions
        self.create_details_panel(main_frame)

        # === BOTTOM STATUS BAR ===
        self.create_status_bar()

        # === DROP ZONE (if drag-drop available) ===
        if HAS_DND:
            self.setup_drag_drop()

    def create_banner(self):
        """Create the retro banner with animated marquee."""
        banner_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'], height=80)
        banner_frame.pack(fill='x', padx=5, pady=5)
        banner_frame.pack_propagate(False)

        # Animated stars
        star_label = tk.Label(banner_frame, text="★ ★ ★",
                             font=('Courier', 16, 'bold'),
                             fg=self.COLORS['marquee'], bg=self.COLORS['bg_dark'])
        star_label.pack(side='left', padx=10)

        # Main title with 3D effect
        title_frame = tk.Frame(banner_frame, bg=self.COLORS['bg_dark'])
        title_frame.pack(expand=True)

        # Shadow text
        shadow = tk.Label(title_frame, text="RETRO ZIP UTILITY",
                         font=('Courier', 24, 'bold'),
                         fg=self.COLORS['button_shadow'], bg=self.COLORS['bg_dark'])
        shadow.place(x=2, y=2)

        # Main text
        title = tk.Label(title_frame, text="RETRO ZIP UTILITY",
                        font=('Courier', 24, 'bold'),
                        fg=self.COLORS['cyan'], bg=self.COLORS['bg_dark'])
        title.pack()

        # Marquee text
        self.marquee_text = ">>> Welcome to RETRO ZIP UTILITY! The BEST archive manager for your desktop! " \
                           "Features: ZIP, UNZIP, Password Protection, Drag & Drop! " \
                           "Made with ♥ for Arch Linux users! <<<"
        self.marquee_label = tk.Label(banner_frame, text=self.marquee_text,
                                     font=('Courier', 10),
                                     fg=self.COLORS['marquee'],
                                     bg=self.COLORS['bg_dark'])
        self.marquee_label.pack(side='bottom', pady=5)

        # More stars
        star_label2 = tk.Label(banner_frame, text="★ ★ ★",
                              font=('Courier', 16, 'bold'),
                              fg=self.COLORS['marquee'], bg=self.COLORS['bg_dark'])
        star_label2.pack(side='right', padx=10)

    def create_toolbar(self):
        """Create the toolbar with retro 3D buttons."""
        toolbar = tk.Frame(self.root, bg=self.COLORS['bg_light'],
                          relief='raised', bd=2)
        toolbar.pack(fill='x', padx=10, pady=2)

        # Button style
        btn_config = {
            'font': ('Courier', 9, 'bold'),
            'relief': 'raised',
            'bd': 3,
            'bg': self.COLORS['button_face'],
            'activebackground': self.COLORS['button_highlight'],
            'padx': 10,
            'pady': 5
        }

        # Toolbar buttons
        buttons = [
            ("📁 New", self.new_archive, "Create new archive"),
            ("📂 Open", self.open_archive, "Open existing archive"),
            ("➕ Add", self.add_files, "Add files to archive"),
            ("📤 Extract", self.extract_files, "Extract selected files"),
            ("📦 Extract All", self.extract_all, "Extract entire archive"),
            ("🗑️ Delete", self.delete_selected, "Remove from archive"),
            ("🔍 View", self.view_file, "View selected file"),
            ("ℹ️ Info", self.show_archive_info, "Archive information"),
            ("⚙️ Options", self.show_options, "Settings"),
            ("❓ Help", self.show_help, "Help & About"),
        ]

        for text, command, tooltip in buttons:
            btn = tk.Button(toolbar, text=text, command=command, **btn_config)
            btn.pack(side='left', padx=2, pady=3)
            self.create_tooltip(btn, tooltip)

    def create_file_panel(self, parent):
        """Create the file listing panel."""
        left_frame = tk.Frame(parent, bg=self.COLORS['bg_light'])
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        # Archive path display
        path_frame = tk.Frame(left_frame, bg=self.COLORS['bg_light'])
        path_frame.pack(fill='x', pady=(0, 5))

        tk.Label(path_frame, text="Current Archive:",
                font=('Courier', 10, 'bold'),
                bg=self.COLORS['bg_light']).pack(side='left')

        self.path_var = tk.StringVar(value="[No archive loaded]")
        self.path_label = tk.Label(path_frame, textvariable=self.path_var,
                                  font=('Courier', 9),
                                  fg=self.COLORS['link'],
                                  bg=self.COLORS['bg_light'],
                                  anchor='w')
        self.path_label.pack(side='left', fill='x', expand=True, padx=5)

        # File tree with columns
        columns = ('name', 'size', 'compressed', 'ratio', 'date', 'crc')

        # Treeview with scrollbars
        tree_frame = tk.Frame(left_frame, bg=self.COLORS['text_dark'])
        tree_frame.pack(fill='both', expand=True)

        self.file_tree = ttk.Treeview(tree_frame, columns=columns,
                                     show='headings', selectmode='extended')

        # Configure columns
        self.file_tree.heading('name', text='📄 File Name', anchor='w')
        self.file_tree.heading('size', text='📊 Size', anchor='e')
        self.file_tree.heading('compressed', text='📦 Packed', anchor='e')
        self.file_tree.heading('ratio', text='📈 Ratio', anchor='e')
        self.file_tree.heading('date', text='📅 Modified', anchor='w')
        self.file_tree.heading('crc', text='🔢 CRC-32', anchor='w')

        self.file_tree.column('name', width=200, minwidth=100)
        self.file_tree.column('size', width=80, minwidth=60)
        self.file_tree.column('compressed', width=80, minwidth=60)
        self.file_tree.column('ratio', width=60, minwidth=50)
        self.file_tree.column('date', width=130, minwidth=100)
        self.file_tree.column('crc', width=80, minwidth=70)

        # Scrollbars
        v_scroll = ttk.Scrollbar(tree_frame, orient='vertical',
                                command=self.file_tree.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient='horizontal',
                                command=self.file_tree.xview)

        self.file_tree.configure(yscrollcommand=v_scroll.set,
                                xscrollcommand=h_scroll.set)

        # Grid layout for tree and scrollbars
        self.file_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Context menu
        self.create_context_menu()

    def create_details_panel(self, parent):
        """Create the details and quick actions panel."""
        right_frame = tk.Frame(parent, bg=self.COLORS['bg_medium'],
                              width=250, relief='groove', bd=2)
        right_frame.pack(side='right', fill='y', padx=5, pady=5)
        right_frame.pack_propagate(False)

        # Panel title
        tk.Label(right_frame, text="═══ QUICK PANEL ═══",
                font=('Courier', 11, 'bold'),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_medium']).pack(pady=10)

        # Drop zone
        drop_frame = tk.Frame(right_frame, bg=self.COLORS['bg_light'],
                             relief='sunken', bd=3, height=100)
        drop_frame.pack(fill='x', padx=10, pady=5)
        drop_frame.pack_propagate(False)

        self.drop_label = tk.Label(drop_frame,
                                  text="🎯 DROP FILES HERE 🎯\n\n"
                                       "Drag & Drop files to\n"
                                       "add them to archive",
                                  font=('Courier', 9),
                                  bg=self.COLORS['bg_light'],
                                  justify='center')
        self.drop_label.pack(expand=True)

        if HAS_DND:
            drop_frame.drop_target_register(DND_FILES)
            drop_frame.dnd_bind('<<Drop>>', self.on_drop)
            drop_frame.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            drop_frame.dnd_bind('<<DragLeave>>', self.on_drag_leave)
        else:
            self.drop_label.config(text="📦 DROP ZONE 📦\n\n"
                                       "Install tkinterdnd2\n"
                                       "for drag & drop!")

        # Quick stats
        stats_frame = tk.LabelFrame(right_frame, text="📊 Archive Stats",
                                   font=('Courier', 9, 'bold'),
                                   fg=self.COLORS['text_light'],
                                   bg=self.COLORS['bg_medium'])
        stats_frame.pack(fill='x', padx=10, pady=10)

        self.stats_labels = {}
        stats = [
            ('files', 'Files: '),
            ('total_size', 'Total Size: '),
            ('compressed', 'Compressed: '),
            ('ratio', 'Ratio: '),
        ]

        for key, text in stats:
            frame = tk.Frame(stats_frame, bg=self.COLORS['bg_medium'])
            frame.pack(fill='x', padx=5, pady=2)

            tk.Label(frame, text=text, font=('Courier', 8),
                    fg=self.COLORS['text_light'],
                    bg=self.COLORS['bg_medium']).pack(side='left')

            self.stats_labels[key] = tk.Label(frame, text="-",
                                             font=('Courier', 8, 'bold'),
                                             fg=self.COLORS['accent2'],
                                             bg=self.COLORS['bg_medium'])
            self.stats_labels[key].pack(side='right')

        # Compression settings
        comp_frame = tk.LabelFrame(right_frame, text="⚙️ Compression",
                                  font=('Courier', 9, 'bold'),
                                  fg=self.COLORS['text_light'],
                                  bg=self.COLORS['bg_medium'])
        comp_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(comp_frame, text="Level (0-9):",
                font=('Courier', 8),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_medium']).pack(anchor='w', padx=5)

        self.compression_var = tk.IntVar(value=6)
        comp_scale = tk.Scale(comp_frame, from_=0, to=9,
                             orient='horizontal',
                             variable=self.compression_var,
                             font=('Courier', 8),
                             bg=self.COLORS['bg_medium'],
                             fg=self.COLORS['text_light'],
                             troughcolor=self.COLORS['bg_light'],
                             activebackground=self.COLORS['accent'])
        comp_scale.pack(fill='x', padx=5, pady=5)

        # Password protection
        pwd_frame = tk.LabelFrame(right_frame, text="🔐 Password",
                                 font=('Courier', 9, 'bold'),
                                 fg=self.COLORS['text_light'],
                                 bg=self.COLORS['bg_medium'])
        pwd_frame.pack(fill='x', padx=10, pady=10)

        self.password_var = tk.StringVar()
        pwd_entry = tk.Entry(pwd_frame, textvariable=self.password_var,
                            show='*', font=('Courier', 9))
        pwd_entry.pack(fill='x', padx=5, pady=5)

        self.encrypt_var = tk.BooleanVar()
        encrypt_cb = tk.Checkbutton(pwd_frame, text="Encrypt archive",
                                   variable=self.encrypt_var,
                                   font=('Courier', 8),
                                   fg=self.COLORS['text_light'],
                                   bg=self.COLORS['bg_medium'],
                                   selectcolor=self.COLORS['bg_dark'],
                                   activebackground=self.COLORS['bg_medium'])
        encrypt_cb.pack(anchor='w', padx=5)

        if not HAS_ENCRYPTION:
            encrypt_cb.config(state='disabled')
            tk.Label(pwd_frame, text="(Install pyzipper)",
                    font=('Courier', 7),
                    fg=self.COLORS['warning'],
                    bg=self.COLORS['bg_medium']).pack()

        # Hit counter (retro web element!)
        counter_frame = tk.Frame(right_frame, bg=self.COLORS['bg_medium'])
        counter_frame.pack(side='bottom', pady=10)

        tk.Label(counter_frame, text="You are visitor #",
                font=('Courier', 8),
                fg=self.COLORS['text_light'],
                bg=self.COLORS['bg_medium']).pack()

        # Fake counter with retro LCD style
        counter_display = tk.Label(counter_frame, text="000001337",
                                  font=('Courier', 12, 'bold'),
                                  fg=self.COLORS['accent2'],
                                  bg=self.COLORS['text_dark'],
                                  relief='sunken', bd=2, padx=10)
        counter_display.pack(pady=5)

    def create_status_bar(self):
        """Create the bottom status bar."""
        status_frame = tk.Frame(self.root, bg=self.COLORS['bg_light'],
                               relief='sunken', bd=2)
        status_frame.pack(fill='x', padx=10, pady=5)

        # Status message
        self.status_var = tk.StringVar(value="Ready - Select an archive to begin!")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               font=('Courier', 9),
                               bg=self.COLORS['bg_light'],
                               anchor='w')
        status_label.pack(side='left', padx=5, fill='x', expand=True)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(status_frame,
                                       variable=self.progress_var,
                                       maximum=100, length=150)
        self.progress.pack(side='right', padx=5, pady=3)

        # Blinking indicator
        self.blink_label = tk.Label(status_frame, text="●",
                                   font=('Courier', 10),
                                   fg=self.COLORS['accent2'],
                                   bg=self.COLORS['bg_light'])
        self.blink_label.pack(side='right', padx=5)

    def create_context_menu(self):
        """Create right-click context menu."""
        self.context_menu = tk.Menu(self.root, tearoff=0,
                                   font=('Courier', 9))
        self.context_menu.add_command(label="📤 Extract Selected",
                                     command=self.extract_files)
        self.context_menu.add_command(label="🔍 View File",
                                     command=self.view_file)
        self.context_menu.add_command(label="ℹ️ Properties",
                                     command=self.show_file_properties)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Delete",
                                     command=self.delete_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✅ Select All",
                                     command=self.select_all)

        self.file_tree.bind('<Button-3>', self.show_context_menu)

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(tooltip, text=text,
                           font=('Courier', 8),
                           bg=self.COLORS['marquee'],
                           fg=self.COLORS['text_dark'],
                           relief='solid', bd=1, padx=5, pady=2)
            label.pack()

            widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def setup_bindings(self):
        """Set up keyboard shortcuts."""
        self.root.bind('<Control-n>', lambda e: self.new_archive())
        self.root.bind('<Control-o>', lambda e: self.open_archive())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Control-e>', lambda e: self.extract_all())
        self.root.bind('<Double-1>', self.on_double_click)

        self.file_tree.bind('<<TreeviewSelect>>', self.on_selection_change)

    def setup_drag_drop(self):
        """Set up drag and drop functionality."""
        if HAS_DND:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)

    # === Animation Methods ===

    def animate_marquee(self):
        """Animate the marquee text."""
        if hasattr(self, 'marquee_label'):
            text = self.marquee_text
            display = text[self.marquee_pos:] + " " + text[:self.marquee_pos]
            self.marquee_label.config(text=display[:80])
            self.marquee_pos = (self.marquee_pos + 1) % len(text)
        self.root.after(100, self.animate_marquee)

    def animate_blink(self):
        """Animate the blinking indicator."""
        if hasattr(self, 'blink_label'):
            if self.is_processing:
                color = self.COLORS['warning'] if self.blink_state else self.COLORS['accent2']
            else:
                color = self.COLORS['accent2'] if self.blink_state else self.COLORS['bg_light']
            self.blink_label.config(fg=color)
            self.blink_state = not self.blink_state
        self.root.after(500, self.animate_blink)

    # === Archive Operations ===

    def new_archive(self):
        """Create a new archive."""
        filepath = filedialog.asksaveasfilename(
            title="Create New Archive",
            defaultextension=".zip",
            filetypes=[("ZIP Archives", "*.zip"), ("All Files", "*.*")],
            initialdir=self.settings['last_directory']
        )

        if filepath:
            try:
                # Create empty archive
                with zipfile.ZipFile(filepath, 'w') as zf:
                    pass

                self.current_archive = filepath
                self.path_var.set(filepath)
                self.update_file_list()
                self.update_stats()
                self.add_to_history(filepath)
                self.settings['last_directory'] = os.path.dirname(filepath)
                self.status_var.set(f"Created new archive: {os.path.basename(filepath)}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to create archive:\n{e}")

    def open_archive(self):
        """Open an existing archive."""
        filepath = filedialog.askopenfilename(
            title="Open Archive",
            filetypes=[("ZIP Archives", "*.zip"), ("All Archives", "*.zip;*.jar;*.war;*.ear"), ("All Files", "*.*")],
            initialdir=self.settings['last_directory']
        )

        if filepath:
            self.load_archive(filepath)

    def load_archive(self, filepath):
        """Load an archive file."""
        try:
            # Check if password protected
            with zipfile.ZipFile(filepath, 'r') as zf:
                # Try to read file list
                self.archive_contents = zf.infolist()

            self.current_archive = filepath
            self.path_var.set(filepath)
            self.update_file_list()
            self.update_stats()
            self.add_to_history(filepath)
            self.settings['last_directory'] = os.path.dirname(filepath)
            self.status_var.set(f"Opened: {os.path.basename(filepath)} ({len(self.archive_contents)} files)")

        except zipfile.BadZipFile:
            messagebox.showerror("Error", "Invalid or corrupted ZIP file!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open archive:\n{e}")

    def update_file_list(self):
        """Update the file tree with archive contents."""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        if not self.current_archive:
            return

        try:
            with zipfile.ZipFile(self.current_archive, 'r') as zf:
                for info in zf.infolist():
                    # Calculate compression ratio
                    if info.file_size > 0:
                        ratio = (1 - info.compress_size / info.file_size) * 100
                        ratio_str = f"{ratio:.1f}%"
                    else:
                        ratio_str = "-"

                    # Format date
                    date_str = datetime(*info.date_time).strftime("%Y-%m-%d %H:%M")

                    # Insert into tree
                    self.file_tree.insert('', 'end', values=(
                        info.filename,
                        self.format_size(info.file_size),
                        self.format_size(info.compress_size),
                        ratio_str,
                        date_str,
                        f"{info.CRC:08X}"
                    ))

        except Exception as e:
            self.status_var.set(f"Error reading archive: {e}")

    def update_stats(self):
        """Update archive statistics display."""
        if not self.current_archive:
            for key in self.stats_labels:
                self.stats_labels[key].config(text="-")
            return

        try:
            with zipfile.ZipFile(self.current_archive, 'r') as zf:
                total_size = sum(info.file_size for info in zf.infolist())
                compressed = sum(info.compress_size for info in zf.infolist())

                if total_size > 0:
                    ratio = (1 - compressed / total_size) * 100
                else:
                    ratio = 0

                self.stats_labels['files'].config(text=str(len(zf.infolist())))
                self.stats_labels['total_size'].config(text=self.format_size(total_size))
                self.stats_labels['compressed'].config(text=self.format_size(compressed))
                self.stats_labels['ratio'].config(text=f"{ratio:.1f}%")

        except Exception as e:
            self.status_var.set(f"Error updating stats: {e}")

    def add_files(self):
        """Add files to the current archive."""
        if not self.current_archive:
            messagebox.showwarning("No Archive", "Please create or open an archive first!")
            return

        files = filedialog.askopenfilenames(
            title="Select Files to Add",
            initialdir=self.settings['last_directory']
        )

        if files:
            self.add_files_to_archive(files)

    def add_files_to_archive(self, files):
        """Add files to archive with progress."""
        if not self.current_archive:
            return

        def add_worker():
            self.is_processing = True
            total = len(files)
            added = 0

            try:
                compression = self.compression_var.get()
                password = self.password_var.get() if self.encrypt_var.get() else None

                if password and HAS_ENCRYPTION:
                    # Use pyzipper for encryption
                    with pyzipper.AESZipFile(self.current_archive, 'a',
                                            compression=pyzipper.ZIP_DEFLATED,
                                            compresslevel=compression) as zf:
                        zf.setpassword(password.encode())
                        zf.setencryption(pyzipper.WZ_AES, nbits=256)

                        for filepath in files:
                            if os.path.isfile(filepath):
                                arcname = os.path.basename(filepath)
                                zf.write(filepath, arcname)
                                added += 1
                                progress = (added / total) * 100
                                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                                self.root.after(0, lambda f=arcname:
                                              self.status_var.set(f"Adding: {f}"))
                else:
                    # Standard zip
                    with zipfile.ZipFile(self.current_archive, 'a',
                                        compression=zipfile.ZIP_DEFLATED,
                                        compresslevel=compression) as zf:
                        for filepath in files:
                            if os.path.isfile(filepath):
                                arcname = os.path.basename(filepath)
                                zf.write(filepath, arcname)
                                added += 1
                                progress = (added / total) * 100
                                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                                self.root.after(0, lambda f=arcname:
                                              self.status_var.set(f"Adding: {f}"))
                            elif os.path.isdir(filepath):
                                # Add directory recursively
                                for root, dirs, filenames in os.walk(filepath):
                                    for filename in filenames:
                                        full_path = os.path.join(root, filename)
                                        arcname = os.path.relpath(full_path,
                                                                 os.path.dirname(filepath))
                                        zf.write(full_path, arcname)

                self.root.after(0, self.update_file_list)
                self.root.after(0, self.update_stats)
                self.root.after(0, lambda: self.status_var.set(f"Added {added} file(s)"))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to add files:\n{e}"))
            finally:
                self.is_processing = False
                self.root.after(0, lambda: self.progress_var.set(0))

        thread = threading.Thread(target=add_worker, daemon=True)
        thread.start()

    def extract_files(self):
        """Extract selected files from archive."""
        if not self.current_archive:
            messagebox.showwarning("No Archive", "No archive is currently open!")
            return

        selection = self.file_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select files to extract!")
            return

        dest_dir = filedialog.askdirectory(
            title="Select Destination Directory",
            initialdir=self.settings['last_directory']
        )

        if dest_dir:
            self.extract_files_worker(selection, dest_dir)

    def extract_all(self):
        """Extract all files from archive."""
        if not self.current_archive:
            messagebox.showwarning("No Archive", "No archive is currently open!")
            return

        dest_dir = filedialog.askdirectory(
            title="Select Destination Directory",
            initialdir=self.settings['last_directory']
        )

        if dest_dir:
            selection = self.file_tree.get_children()
            self.extract_files_worker(selection, dest_dir)

    def extract_files_worker(self, selection, dest_dir):
        """Worker function to extract files."""
        def extract():
            self.is_processing = True
            total = len(selection)
            extracted = 0

            try:
                password = self.password_var.get() if self.password_var.get() else None

                with zipfile.ZipFile(self.current_archive, 'r') as zf:
                    for item in selection:
                        filename = self.file_tree.item(item)['values'][0]

                        try:
                            if password:
                                zf.extract(filename, dest_dir, pwd=password.encode())
                            else:
                                zf.extract(filename, dest_dir)

                            extracted += 1
                            progress = (extracted / total) * 100
                            self.root.after(0, lambda p=progress: self.progress_var.set(p))
                            self.root.after(0, lambda f=filename:
                                          self.status_var.set(f"Extracting: {f}"))
                        except RuntimeError as e:
                            if "password required" in str(e).lower():
                                self.root.after(0, lambda:
                                              messagebox.showerror("Password Required",
                                                                  "This archive requires a password!"))
                                return
                            raise

                self.root.after(0, lambda: self.status_var.set(
                    f"Extracted {extracted} file(s) to {dest_dir}"))
                self.root.after(0, lambda: messagebox.showinfo("Complete",
                    f"Successfully extracted {extracted} file(s)!"))

            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error",
                    f"Extraction failed:\n{e}"))
            finally:
                self.is_processing = False
                self.root.after(0, lambda: self.progress_var.set(0))

        thread = threading.Thread(target=extract, daemon=True)
        thread.start()

    def delete_selected(self):
        """Delete selected files from archive."""
        if not self.current_archive:
            return

        selection = self.file_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select files to delete!")
            return

        files_to_delete = [self.file_tree.item(item)['values'][0] for item in selection]

        if messagebox.askyesno("Confirm Delete",
                              f"Delete {len(files_to_delete)} file(s) from archive?"):
            try:
                # Create new archive without deleted files
                temp_path = self.current_archive + '.tmp'

                with zipfile.ZipFile(self.current_archive, 'r') as zf_in:
                    with zipfile.ZipFile(temp_path, 'w') as zf_out:
                        for item in zf_in.infolist():
                            if item.filename not in files_to_delete:
                                data = zf_in.read(item.filename)
                                zf_out.writestr(item, data)

                # Replace original with new
                os.replace(temp_path, self.current_archive)

                self.update_file_list()
                self.update_stats()
                self.status_var.set(f"Deleted {len(files_to_delete)} file(s)")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete files:\n{e}")

    def view_file(self):
        """View the contents of selected file."""
        selection = self.file_tree.selection()
        if not selection:
            return

        filename = self.file_tree.item(selection[0])['values'][0]

        try:
            with zipfile.ZipFile(self.current_archive, 'r') as zf:
                # Check file size
                info = zf.getinfo(filename)
                if info.file_size > 1024 * 1024:  # 1MB limit
                    messagebox.showwarning("File Too Large",
                                          "File is too large to view inline!")
                    return

                password = self.password_var.get() if self.password_var.get() else None

                try:
                    if password:
                        content = zf.read(filename, pwd=password.encode())
                    else:
                        content = zf.read(filename)
                except RuntimeError:
                    messagebox.showerror("Error", "Password required to view this file!")
                    return

                # Try to decode as text
                try:
                    text = content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        text = content.decode('latin-1')
                    except:
                        text = f"[Binary file - {len(content)} bytes]"

                # Show in new window
                viewer = tk.Toplevel(self.root)
                viewer.title(f"Viewing: {filename}")
                viewer.geometry("600x400")
                viewer.configure(bg=self.COLORS['bg_light'])

                text_widget = tk.Text(viewer, font=('Courier', 10),
                                     bg=self.COLORS['text_light'],
                                     wrap='none')
                text_widget.pack(fill='both', expand=True, padx=5, pady=5)
                text_widget.insert('1.0', text)
                text_widget.config(state='disabled')

                # Scrollbars
                v_scroll = ttk.Scrollbar(text_widget, orient='vertical',
                                        command=text_widget.yview)
                h_scroll = ttk.Scrollbar(text_widget, orient='horizontal',
                                        command=text_widget.xview)
                text_widget.configure(yscrollcommand=v_scroll.set,
                                     xscrollcommand=h_scroll.set)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to view file:\n{e}")

    def show_file_properties(self):
        """Show properties of selected file."""
        selection = self.file_tree.selection()
        if not selection:
            return

        filename = self.file_tree.item(selection[0])['values'][0]

        try:
            with zipfile.ZipFile(self.current_archive, 'r') as zf:
                info = zf.getinfo(filename)

                props = f"""
╔══════════════════════════════════════╗
║         FILE PROPERTIES              ║
╚══════════════════════════════════════╝

File Name: {info.filename}
Original Size: {self.format_size(info.file_size)}
Compressed Size: {self.format_size(info.compress_size)}
Compression Type: {self.get_compression_name(info.compress_type)}
CRC-32: {info.CRC:08X}
Modified: {datetime(*info.date_time).strftime("%Y-%m-%d %H:%M:%S")}
Internal Attr: {info.internal_attr}
External Attr: {info.external_attr}
Header Offset: {info.header_offset}
"""
                if info.comment:
                    props += f"Comment: {info.comment.decode()}\n"

                messagebox.showinfo("File Properties", props)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get properties:\n{e}")

    def show_archive_info(self):
        """Show archive information."""
        if not self.current_archive:
            messagebox.showwarning("No Archive", "No archive is currently open!")
            return

        try:
            stat = os.stat(self.current_archive)

            with zipfile.ZipFile(self.current_archive, 'r') as zf:
                total_files = len(zf.infolist())
                total_size = sum(info.file_size for info in zf.infolist())
                compressed = sum(info.compress_size for info in zf.infolist())

                info_text = f"""
╔══════════════════════════════════════╗
║        ARCHIVE INFORMATION           ║
╚══════════════════════════════════════╝

Path: {self.current_archive}
Archive Size: {self.format_size(stat.st_size)}
Number of Files: {total_files}
Total Uncompressed: {self.format_size(total_size)}
Total Compressed: {self.format_size(compressed)}
Compression Ratio: {((1 - compressed/total_size) * 100) if total_size > 0 else 0:.1f}%
Created: {datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")}
Modified: {datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")}

Comment: {zf.comment.decode() if zf.comment else "(none)"}
"""
                messagebox.showinfo("Archive Information", info_text)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get archive info:\n{e}")

    # === Event Handlers ===

    def on_drop(self, event):
        """Handle file drop event."""
        files = self.parse_drop_data(event.data)

        if not self.current_archive:
            # If dropping a zip, open it
            if len(files) == 1 and files[0].lower().endswith('.zip'):
                self.load_archive(files[0])
                return
            else:
                messagebox.showwarning("No Archive",
                                      "Please create or open an archive first!")
                return

        self.add_files_to_archive(files)
        self.drop_label.config(bg=self.COLORS['bg_light'])

    def on_drag_enter(self, event):
        """Handle drag enter event."""
        self.drop_label.config(bg=self.COLORS['accent2'])

    def on_drag_leave(self, event):
        """Handle drag leave event."""
        self.drop_label.config(bg=self.COLORS['bg_light'])

    def parse_drop_data(self, data):
        """Parse dropped file data."""
        files = []
        # Handle different formats
        if '{' in data:
            # Tcl list format
            import re
            files = re.findall(r'\{([^}]+)\}|(\S+)', data)
            files = [f[0] or f[1] for f in files]
        else:
            files = data.split()

        return [f.strip() for f in files if f.strip()]

    def on_selection_change(self, event):
        """Handle selection change in file tree."""
        selection = self.file_tree.selection()
        count = len(selection)
        if count > 0:
            self.status_var.set(f"Selected {count} file(s)")

    def on_double_click(self, event):
        """Handle double-click on file."""
        self.view_file()

    def show_context_menu(self, event):
        """Show context menu at cursor position."""
        # Select item under cursor
        item = self.file_tree.identify_row(event.y)
        if item:
            self.file_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def select_all(self):
        """Select all files in the tree."""
        for item in self.file_tree.get_children():
            self.file_tree.selection_add(item)

    # === Dialogs ===

    def show_options(self):
        """Show options dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚙️ Options")
        dialog.geometry("400x350")
        dialog.configure(bg=self.COLORS['bg_light'])
        dialog.transient(self.root)
        dialog.grab_set()

        # Title
        tk.Label(dialog, text="═══ SETTINGS ═══",
                font=('Courier', 14, 'bold'),
                bg=self.COLORS['bg_light']).pack(pady=10)

        # Options
        options_frame = tk.Frame(dialog, bg=self.COLORS['bg_light'])
        options_frame.pack(fill='both', expand=True, padx=20)

        # Show hidden files
        show_hidden_var = tk.BooleanVar(value=self.settings['show_hidden'])
        tk.Checkbutton(options_frame, text="Show hidden files",
                      variable=show_hidden_var,
                      font=('Courier', 10),
                      bg=self.COLORS['bg_light']).pack(anchor='w', pady=5)

        # Confirm overwrite
        confirm_var = tk.BooleanVar(value=self.settings['confirm_overwrite'])
        tk.Checkbutton(options_frame, text="Confirm before overwriting",
                      variable=confirm_var,
                      font=('Courier', 10),
                      bg=self.COLORS['bg_light']).pack(anchor='w', pady=5)

        # Default compression
        tk.Label(options_frame, text="Default compression level:",
                font=('Courier', 10),
                bg=self.COLORS['bg_light']).pack(anchor='w', pady=(10, 0))

        comp_var = tk.IntVar(value=self.compression_var.get())
        comp_scale = tk.Scale(options_frame, from_=0, to=9,
                             orient='horizontal',
                             variable=comp_var,
                             font=('Courier', 9),
                             bg=self.COLORS['bg_light'])
        comp_scale.pack(fill='x', pady=5)

        # Buttons
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg_light'])
        btn_frame.pack(pady=20)

        def save_settings():
            self.settings['show_hidden'] = show_hidden_var.get()
            self.settings['confirm_overwrite'] = confirm_var.get()
            self.compression_var.set(comp_var.get())
            self.save_settings()
            dialog.destroy()
            messagebox.showinfo("Saved", "Settings saved successfully!")

        tk.Button(btn_frame, text="💾 Save",
                 command=save_settings,
                 font=('Courier', 10, 'bold'),
                 relief='raised', bd=3,
                 padx=20).pack(side='left', padx=10)

        tk.Button(btn_frame, text="❌ Cancel",
                 command=dialog.destroy,
                 font=('Courier', 10, 'bold'),
                 relief='raised', bd=3,
                 padx=20).pack(side='left', padx=10)

    def show_help(self):
        """Show help dialog."""
        help_text = """
╔══════════════════════════════════════════════════════╗
║     RETRO ZIP UTILITY v1.0 - HELP & ABOUT            ║
╚══════════════════════════════════════════════════════╝

Welcome to RETRO ZIP UTILITY - The ultimate archive
manager with that classic 90s web aesthetic!

FEATURES:
─────────
• Create and open ZIP archives
• Add files via button or drag-and-drop
• Extract individual files or entire archives
• Password protection (requires pyzipper)
• Adjustable compression levels (0-9)
• View file contents directly
• Detailed file properties

KEYBOARD SHORTCUTS:
───────────────────
Ctrl+N    Create new archive
Ctrl+O    Open archive
Ctrl+A    Select all files
Ctrl+E    Extract all
Delete    Remove selected files
F1        Show this help

DRAG & DROP:
────────────
• Drop ZIP files to open them
• Drop files on archive to add them
• Requires: pip install tkinterdnd2

ENCRYPTION:
───────────
For password-protected archives, install:
    pip install pyzipper

TIPS:
─────
• Double-click files to view contents
• Right-click for context menu
• Higher compression = smaller file but slower

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Made with ♥ for Arch Linux users!
Best viewed with Netscape Navigator 4.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        dialog = tk.Toplevel(self.root)
        dialog.title("❓ Help & About")
        dialog.geometry("500x600")
        dialog.configure(bg=self.COLORS['bg_dark'])

        text = tk.Text(dialog, font=('Courier', 9),
                      bg=self.COLORS['text_dark'],
                      fg=self.COLORS['accent2'],
                      wrap='word')
        text.pack(fill='both', expand=True, padx=10, pady=10)
        text.insert('1.0', help_text)
        text.config(state='disabled')

        tk.Button(dialog, text="Close",
                 command=dialog.destroy,
                 font=('Courier', 10, 'bold'),
                 relief='raised', bd=3).pack(pady=10)

    # === Utility Methods ===

    def format_size(self, size):
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def get_compression_name(self, method):
        """Get compression method name."""
        methods = {
            0: 'Stored',
            8: 'Deflated',
            12: 'BZIP2',
            14: 'LZMA'
        }
        return methods.get(method, f'Unknown ({method})')

    def add_to_history(self, filepath):
        """Add file to history."""
        if filepath not in self.history:
            self.history.insert(0, filepath)
            self.history = self.history[:10]  # Keep last 10

    def load_settings(self):
        """Load settings from file."""
        settings_path = os.path.expanduser('~/.retro_zip_settings.json')
        try:
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    self.settings.update(json.load(f))
        except:
            pass

    def save_settings(self):
        """Save settings to file."""
        settings_path = os.path.expanduser('~/.retro_zip_settings.json')
        try:
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except:
            pass

    def run(self):
        """Run the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    print("""
    ╔════════════════════════════════════════════╗
    ║   RETRO ZIP UTILITY v1.0                   ║
    ║   Starting up...                           ║
    ╚════════════════════════════════════════════╝
    """)

    app = RetroZipUtility()
    app.run()


if __name__ == '__main__':
    main()
