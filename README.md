# RETRO ZIP UTILITY v1.0

```
╔══════════════════════════════════════════════════════════════════╗
║  RETRO ZIP UTILITY v1.0 - The Ultimate Archive Manager!          ║
║  ════════════════════════════════════════════════════════════    ║
║  A nostalgic trip back to the golden age of the web!             ║
╚══════════════════════════════════════════════════════════════════╝
```

A fully-featured ZIP archive manager with a classic 90s web aesthetic, built for Arch Linux.

## Features

- **Create/Open ZIP archives** - Full ZIP file support
- **Drag & Drop** - Drop files to add, drop ZIPs to open
- **Password Protection** - AES-256 encryption support
- **Adjustable Compression** - Levels 0-9
- **File Viewer** - View text files directly
- **Retro Theme** - Classic 90s web design with animated marquee

## Installation on Arch Linux

### 1. Install Python and Tkinter

```bash
sudo pacman -S python python-pip tk
```

### 2. Install Dependencies

```bash
# Required for drag & drop
pip install tkinterdnd2

# Required for password-protected archives
pip install pyzipper
```

Or install from requirements:

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python retro_zip.py
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Ctrl+N | Create new archive |
| Ctrl+O | Open archive |
| Ctrl+A | Select all files |
| Ctrl+E | Extract all |
| Delete | Remove selected |
| F1 | Help |

## Screenshots

The application features:
- Navy blue and teal color scheme
- Animated marquee banner
- 3D beveled buttons
- Retro "visitor counter"
- Classic Windows 95 style UI elements

## Requirements

- Python 3.6+
- Tkinter (included with Python on most systems)
- tkinterdnd2 (optional, for drag & drop)
- pyzipper (optional, for encryption)

## License

MIT License - Free to use and modify!

---

*Best viewed with Netscape Navigator 4.0*
