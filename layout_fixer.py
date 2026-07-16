"""
Hebrew / English Keyboard Layout Translator
This utility runs in the background and corrects text typed in the wrong keyboard layout.
Default shortcut: Ctrl+Shift+Y
"""

import time
import threading
import sys
import os
import pyperclip
import keyboard

# --- Configuration ---
HOTKEY = 'ctrl+shift+y'

# --- Layout Mappings ---
# Maps English characters to the Hebrew layout keys they share physical space with on standard QWERTY/Hebrew keyboards.
MAP_ENG_TO_HEB = {
    '`': ';', 'q': '/', 'w': "'", 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם', 'p': 'פ',
    '[': '[', ']': ']', '\\': '\\', 'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח',
    'k': 'ל', 'l': 'ך', ';': 'ף', "'": ',', 'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ', 'n': 'מ',
    'm': 'צ', ',': 'ת', '.': 'ץ', '/': '.',
    # Shift/Caps Lock equivalents (mapping uppercase English to Hebrew layout)
    '~': '~', 'Q': '/', 'W': "'", 'E': 'ק', 'R': 'ר', 'T': 'א', 'Y': 'ט', 'U': 'ו', 'I': 'ן', 'O': 'ם', 'P': 'פ',
    '{': '}', '}': '{', '|': '|', 'A': 'ש', 'S': 'ד', 'D': 'ג', 'F': 'כ', 'G': 'ע', 'H': 'י', 'J': 'ח',
    'K': 'ל', 'L': 'ך', ':': 'ף', '"': ',', 'Z': 'ז', 'X': 'ס', 'C': 'ב', 'V': 'ה', 'B': 'נ', 'N': 'מ',
    'M': 'צ', '<': 'ת', '>': 'ץ', '?': '.'
}

# Reverse mapping: Hebrew layout keys back to standard lowercase English layout keys.
MAP_HEB_TO_ENG = {
    ';': '`', '/': 'q', "'": 'w', 'ק': 'e', 'ר': 'r', 'א': 't', 'ט': 'y', 'ו': 'u', 'ן': 'i', 'ם': 'o', 'פ': 'p',
    'ש': 'a', 'ד': 's', 'ג': 'd', 'כ': 'f', 'ע': 'g', 'י': 'h', 'ח': 'j', 'ל': 'k', 'ך': 'l', 'ף': ';',
    ',': "'", 'ז': 'z', 'ס': 'x', 'ב': 'c', 'ה': 'v', 'נ': 'b', 'מ': 'n', 'צ': 'm', 'ת': ',', 'ץ': '.',
    '.': '/'
}

def contains_hebrew(text: str) -> bool:
    """Returns True if the text contains any Hebrew character."""
    return any('\u0590' <= char <= '\u05fe' for char in text)

def translate_text(text: str) -> str:
    """Translates the layout of the given text between Hebrew and English."""
    if not text:
        return text
    
    # If the text contains any Hebrew, translate it to English. Otherwise, translate to Hebrew.
    to_english = contains_hebrew(text)
    mapping = MAP_HEB_TO_ENG if to_english else MAP_ENG_TO_HEB
    
    return "".join(mapping.get(char, char) for char in text)

def fix_layout():
    """Copies selected text, translates it, and pastes it back."""
    # Wait for the hotkey keys to be released to prevent modifier leakage (e.g., Ctrl+Shift+C in Word)
    keys = [k.strip() for k in HOTKEY.split('+')]
    for _ in range(50):  # Timeout after 500ms
        if not any(keyboard.is_pressed(k) for k in keys):
            break
        time.sleep(0.01)
    
    # Tiny delay to let the OS register the key releases
    time.sleep(0.05)

    # Clear clipboard to detect if new content is copied
    try:
        pyperclip.copy("")
    except Exception:
        pass
    
    # Trigger Copy (Ctrl+C)
    keyboard.send('ctrl+c')
    
    # Wait for the clipboard to receive the copied text (up to 500ms)
    copied_text = ""
    for _ in range(50):
        time.sleep(0.01)
        try:
            copied_text = pyperclip.paste()
        except Exception:
            pass
        if copied_text:
            break
            
    # If nothing was selected, do nothing
    if not copied_text:
        return
        
    # Translate the text
    translated_text = translate_text(copied_text)
    
    # If the translated text is identical, do nothing
    if translated_text == copied_text:
        return
        
    # Put translated text on clipboard and paste it
    try:
        pyperclip.copy(translated_text)
    except Exception:
        time.sleep(0.05)
        try:
            pyperclip.copy(translated_text)
        except Exception:
            return
            
    keyboard.send('ctrl+v')

def setup_startup():
    """Checks if a shortcut to the script/exe exists in Windows Startup. If not, creates one."""
    try:
        is_frozen = getattr(sys, 'frozen', False)
        current_path = sys.executable if is_frozen else os.path.abspath(sys.argv[0])
        
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut_path = os.path.join(startup_folder, 'HebrewTypingConvertor.lnk')
        
        if not os.path.exists(shortcut_path):
            import subprocess
            # Powershell script to create shortcut (.lnk)
            ps_cmd = (
                f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_path}'); "
                f"$s.TargetPath = '{current_path}'; "
                f"$s.WorkingDirectory = '{os.path.dirname(current_path)}'; "
                f"$s.Save()"
            )
            cmd = f'powershell -NoProfile -Command "{ps_cmd}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Show popup notification if running as compiled EXE
            if is_frozen:
                import ctypes
                ctypes.windll.user32.MessageBoxW(
                    0, 
                    "Hebrew Typing Convertor has been successfully added to your Windows Startup and is now running in the background!\n\nUse Ctrl+Shift+Y to translate highlighted text.", 
                    "Setup Successful", 
                    64 # MB_ICONINFORMATION
                )
    except Exception:
        pass

def main():
    setup_startup()
    print("=" * 60)
    print(" Hebrew / English Keyboard Layout Fixer (Active)")
    print(f" Shortcut: Press '{HOTKEY.upper()}' to translate highlighted text")
    print(" Press Ctrl+C in this console window to exit.")
    print("=" * 60)
    
    # Add hotkey listener in a separate daemon thread to keep typing responsive
    keyboard.add_hotkey(HOTKEY, lambda: threading.Thread(target=fix_layout, daemon=True).start(), suppress=True)
    
    # Keep the main thread alive
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\nExiting layout fixer. Goodbye!")

if __name__ == "__main__":
    main()
