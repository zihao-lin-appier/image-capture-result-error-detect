# Image Detection Tool (Python + Pillow)

## Requirements

- Python 3.7 or higher
- Pillow (PIL) library

## Installation

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

Process all images in the `data` folder (default):

```bash
python3 main.py
```

Process images from a custom folder:

```bash
python3 main.py /path/to/image/folder
```
