# Hebrew / English Keyboard Layout Fixer

A lightweight utility for Windows that instantly translates text typed in the wrong keyboard layout (e.g., `הקךךם` $\leftrightarrow$ `hello`, `akuo` $\leftrightarrow$ `שלום`).

When you notice a typing mistake, simply **highlight the text** and press **`Ctrl+Shift+Y`**. The utility will automatically correct it inline.

---

## Option 1: Python background utility (Already Set Up)

Since you already have Python installed and the dependencies (`keyboard`, `pyperclip`) are configured, you can run this script immediately.

### Run in the foreground (with a console window)
To run and see logs (ideal for testing):
```bash
python layout_fixer.py
```

### Run silently in the background (no console window)
To run it completely hidden in the background:
```bash
pythonw layout_fixer.py
```

### Run on Windows Startup
To have the script run automatically every time you start your computer:
1. Press `Win + R` to open the Run dialog.
2. Type `shell:startup` and press **Enter**. This opens your Windows Startup folder.
3. Right-click inside the folder, select **New > Shortcut**.
4. In the location field, paste the following command:
   ```cmd
   pythonw.exe "C:\Users\salom\OneDrive\Documents\Antigravity\HebrewTypingTranslator\layout_fixer.py"
   ```
5. Click **Next**, name the shortcut (e.g., "Keyboard Layout Fixer"), and click **Finish**.

---

## Option 2: AutoHotkey (AHK) Utility (Native Alternative)

If you prefer a native, ultra-lightweight Windows script with zero memory footprint:

1. Download and install **AutoHotkey v2** from the [official website](https://www.autohotkey.com/).
2. Double-click the `layout_fixer.ahk` file in this directory to run it.
3. **To run on startup:** Simply copy the `layout_fixer.ahk` file (or create a shortcut to it) and paste it into the `shell:startup` folder (opened using `Win+R` $\rightarrow$ `shell:startup`).

---

## How It Works Under the Hood
1. It listens for the `Ctrl+Shift+Y` keyboard shortcut globally.
2. When pressed, it backups your clipboard, clears it, and simulates a `Ctrl+C` copy keypress.
3. It detects if the selected text is Hebrew or English:
   - If it contains Hebrew letters, it maps them to their QWERTY layout positions.
   - If it contains English letters, it maps them to their Hebrew layout positions.
4. It places the translated text in your clipboard and simulates a `Ctrl+V` paste keypress.
5. It waits 150ms for the paste to finish, then restores your original clipboard contents.
