# Hebrew / English Keyboard Layout Convertor

A lightweight Windows background utility that instantly translates text typed in the wrong keyboard layout (e.g. `הקךךם` $\leftrightarrow$ `hello`, `akuo` $\leftrightarrow$ `שלום`).

When you notice a typing mistake, simply **highlight the text** and press **`Ctrl+Shift+Y`**. The utility will automatically correct it inline.

---

## 🚀 Quick Start & Installation

To install and run this on your computer (no technical setup or Python required):

1. Go to the **[Releases](https://github.com/SalomonMalka/HebrewTypingConvertor/releases)** page of this repository.
2. Download the **`HebrewTypingConvertor.exe`** file from the assets list of the latest release.
3. Double-click the downloaded `.exe` file to run it.
   * **First Run:** A popup window will confirm: *"Hebrew Typing Convertor has been successfully added to your Windows Startup and is now running in the background!"*. It automatically copies a startup shortcut so you never have to open it manually again.
   * **Subsequent boots:** The app launches completely silently in the background on system startup.

---

## ⌨️ How to Use

1. Type your text.
2. If you notice you typed in the wrong language layout:
   * **Highlight/select the mistyped text** (e.g., double-click the word, or hold `Shift` and use arrow keys).
   * Press **`Ctrl + Shift + Y`** on your keyboard.
3. The highlighted text will instantly swap to the correct layout!

*This works globally in any text area on Windows, including web browsers, Microsoft Office (Word, Outlook), Discord, Slack, and text editors.*

---

## 🔍 How It Works Under the Hood
1. It listens for the `Ctrl+Shift+Y` keyboard shortcut globally.
2. When pressed, it waits 50ms for you to release the keys (preventing keyboard modifier leaks in complex applications like Microsoft Word).
3. It clears the clipboard, copies the highlighted text, and analyzes the characters.
   - If it contains Hebrew letters, it maps them back to English QWERTY positions.
   - If it contains English letters, it maps them to standard Windows Hebrew keyboard positions.
4. It sets the clipboard to the corrected text and simulates a `Ctrl+V` paste command.

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
