# Hebrew / English Keyboard Layout Translator

A lightweight Windows background utility that instantly translates text typed in the wrong keyboard layout (e.g. `הקךךם` $\leftrightarrow$ `hello`, `akuo` $\leftrightarrow$ `שלום`).

When you notice a typing mistake, simply **highlight the text** and press **`Ctrl+Shift+Y`**. The utility will automatically correct it inline.

---

## 🚀 1-Click Install (For Other Computers)

To run this on another computer with **no setup or installation required**:

1. Go to your GitHub repository's **Releases** page (once you upload the binary).
2. Download the **`HebrewTypingTranslator.exe`** file from the assets list.
3. Run the downloaded `.exe` file.
   * **First Run:** A popup window will confirm: *"Hebrew Typing Translator has been successfully added to your Windows Startup and is now running in the background!"*. It automatically copies a shortcut to itself into your Windows Startup directory.
   * **Subsequent boots:** The app will launch completely silently in the background.

---

## 🛠️ How to Publish this Project to GitHub

To make this downloadable for others, run these commands in your project folder to link your local Git repository and push it to GitHub:

1. Create a new repository on [github.com](https://github.com/) (do not add a README, license, or .gitignore—keep it empty).
2. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/HebrewTypingTranslator.git`).
3. Open terminal/PowerShell in this directory and run:
   ```bash
   # Add your GitHub repository link
   git remote add origin YOUR_REPOSITORY_URL
   
   # Push your code to GitHub
   git branch -M main
   git push -u origin main
   ```
4. **Publish the executable:**
   * Go to your repository on GitHub.
   * Click **Create a new release** on the right side.
   * Upload the compiled executable `dist/HebrewTypingTranslator.exe` (found in your local project folder) as a release asset.
   * Publish the release. Now, anyone can download the `.exe` with 1 click!

---

## 💻 Running from Source (For Developers)

If you have Python installed and want to run or modify the code directly:

### 1. Install Dependencies
```bash
pip install keyboard pyperclip
```

### 2. Run in the Background
To run silently without a console window:
```bash
pythonw layout_fixer.py
```

### 3. Native AutoHotkey Alternative
If you prefer a native Windows script (requires installing AutoHotkey v2):
* Double-click `layout_fixer.ahk` to run it.
* Move `layout_fixer.ahk` into your Startup folder (`shell:startup`) to run automatically on boot.

---

## 🔍 How It Works Under the Hood
1. It listens for the `Ctrl+Shift+Y` keyboard shortcut globally.
2. When pressed, it waits 50ms for you to release the keys (preventing modifier key leaks in applications like Microsoft Word).
3. It clears the clipboard, copies the highlighted text, and analyzes the characters.
   - If it contains Hebrew, it maps it back to English.
   - If it contains English, it maps it back to Hebrew.
4. It sets the clipboard to the corrected text and simulates a `Ctrl+V` paste command.
