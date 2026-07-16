# Hebrew / English Keyboard Layout Convertor

A lightweight Windows background utility that instantly translates text typed in the wrong keyboard layout (e.g. `הקךךם` $\leftrightarrow$ `hello`, `akuo` $\leftrightarrow$ `שלום`).

When you notice a typing mistake, simply **highlight the text** and press **`Ctrl+Shift+Y`**. The utility will automatically correct it inline.

---

## 🚀 Quick Start & Installation

To install, manage, or run this on your computer (no technical setup or Python required):

1. Go to the **[Releases](https://github.com/SalomonMalka/HebrewTypingConvertor/releases)** page of this repository.
2. Download the **`HebrewTypingConvertor.exe`** file from the assets list of the latest release.
3. Double-click the downloaded `.exe` file to run it.
   * **First Run (Install):** A popup will ask: *"Would you like to install Hebrew Typing Convertor and run it automatically on Windows startup?"*. Click **Yes** to add it to your Startup folder and run it.
   * **Subsequent boot cycles:** The app launches completely silently in the background on startup.
   * **Subsequent manual run (Uninstall / Restart):** If you double-click the `.exe` again manually:
     - It will automatically terminate any older running background instances to let the new version take over immediately.
     - It will ask: *"Hebrew Typing Convertor is already installed. Would you like to uninstall it?"* Click **Yes** to completely remove it from startup and stop the program, or **No** to keep it running.

---

## ⌨️ How to Use

1. Type your text.
2. If you notice you typed in the wrong language layout:
   * **Highlight/select the mistyped text** (e.g., double-click the word, or hold `Shift` and use arrow keys).
   * Press **`Ctrl + Shift + Y`** on your keyboard.
3. The highlighted text will instantly swap to the correct layout!

---

## 📋 Clipboard Preservation & Performance

Unlike basic layout translators that overwrite your clipboard, this utility **automatically preserves your copied text**:
* If you copy some text (e.g., `"Hello"`) and later use `Ctrl+Shift+Y` to translate a layout error, your clipboard is temporarily used to perform the translation but is **automatically restored 150ms later**.
* After translating, pressing `Ctrl+V` will **still paste your original copied text** (`"Hello"`), keeping your clipboard completely clean!

---

## 🔍 How It Works Under the Hood
1. It listens for the `Ctrl+Shift+Y` keyboard shortcut globally.
2. When pressed, it releases all physical modifier keys (`Ctrl`, `Shift`, `Alt`, `Win`) to prevent them from getting stuck and breaking standard keyboard operations like manual `Ctrl+C` copying.
3. It backs up your current clipboard content, copies the highlighted text, and analyzes the characters.
   - If it contains Hebrew letters, it maps them back to English QWERTY positions.
   - If it contains English letters, it maps them to standard Windows Hebrew keyboard positions.
4. It sets the clipboard to the corrected text, simulates a `Ctrl+V` paste command using low-level Windows API commands (`keybd_event` via `ctypes`), and restores your original clipboard 150ms later.

---

## 💻 Running from Source (For Developers)

If you have Python installed and want to run or modify the code directly:

### 1. Install Dependencies
```bash
pip install keyboard pyperclip
```

### 2. Run the Script
To run silently without a console window:
```bash
pythonw layout_fixer.py
```

### 3. Native AutoHotkey Alternative
If you prefer a native Windows script (requires installing AutoHotkey v2):
* Double-click `layout_fixer.ahk` to run it.
* Move `layout_fixer.ahk` into your Startup folder (`shell:startup`) to run automatically on boot.
