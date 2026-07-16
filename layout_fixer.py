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

# Windows Virtual Key Codes
VK_CONTROL = 0x11
VK_SHIFT = 0x10
VK_MENU = 0x12
VK_LWIN = 0x5B
VK_C = 0x43
VK_V = 0x56
KEYEVENTF_KEYUP = 0x0002

def send_key_event(vk, down=True):
    flags = 0 if down else KEYEVENTF_KEYUP
    try:
        import ctypes
        ctypes.windll.user32.keybd_event(vk, 0, flags, 0)
    except Exception:
        pass

def release_modifiers():
    # Explicitly release Ctrl, Shift, Alt, and Win keys to prevent stuck modifiers
    for vk in [VK_CONTROL, VK_SHIFT, VK_MENU, VK_LWIN]:
        send_key_event(vk, down=False)

def simulate_copy():
    release_modifiers()
    send_key_event(VK_CONTROL, down=True)
    send_key_event(VK_C, down=True)
    time.sleep(0.02)
    send_key_event(VK_C, down=False)
    send_key_event(VK_CONTROL, down=False)

def simulate_paste():
    release_modifiers()
    send_key_event(VK_CONTROL, down=True)
    send_key_event(VK_V, down=True)
    time.sleep(0.02)
    send_key_event(VK_V, down=False)
    send_key_event(VK_CONTROL, down=False)

def fix_layout():
    """Copies selected text, translates it, and pastes it back, then restores previous clipboard."""
    # Save the original clipboard content to restore it later
    try:
        old_clipboard = pyperclip.paste()
    except Exception:
        old_clipboard = ""

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
    simulate_copy()
    
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
            
    # If nothing was selected, restore clipboard and exit
    if not copied_text:
        try:
            pyperclip.copy(old_clipboard)
        except Exception:
            pass
        return
        
    # Translate the text
    translated_text = translate_text(copied_text)
    
    # If the translated text is identical, restore clipboard and exit
    if translated_text == copied_text:
        try:
            pyperclip.copy(old_clipboard)
        except Exception:
            pass
        return
        
    # Put translated text on clipboard and paste it
    try:
        pyperclip.copy(translated_text)
    except Exception:
        time.sleep(0.05)
        try:
            pyperclip.copy(translated_text)
        except Exception:
            # Restore clipboard on failure
            try:
                pyperclip.copy(old_clipboard)
            except Exception:
                pass
            return
            
    simulate_paste()
    
    # Wait a small delay for the pasting to finish, then restore the user's original clipboard
    time.sleep(0.15)
    try:
        pyperclip.copy(old_clipboard)
    except Exception:
        pass

def setup_startup(is_startup: bool = False):
    """Checks if a shortcut to the script/exe exists in Windows Startup. If not, prompts user to create one. If yes, offers uninstall."""
    try:
        is_frozen = getattr(sys, 'frozen', False)
        current_path = sys.executable if is_frozen else os.path.abspath(sys.argv[0])
        
        startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut_path = os.path.join(startup_folder, 'HebrewTypingConvertor.lnk')
        
        if os.path.exists(shortcut_path):
            # If the user manually ran it (not from startup boot) and it's compiled, offer to uninstall
            if not is_startup and is_frozen:
                import ctypes
                # MB_YESNO (4) | MB_ICONQUESTION (32) = 36
                res = ctypes.windll.user32.MessageBoxW(
                    0,
                    "Hebrew Typing Convertor is already installed on your computer.\n\nWould you like to uninstall it (remove it from Windows Startup)?",
                    "Uninstall Hebrew Typing Convertor",
                    36
                )
                if res == 6:  # 6 is IDYES. User wants to uninstall.
                    try:
                        os.remove(shortcut_path)
                        ctypes.windll.user32.MessageBoxW(
                            0,
                            "Hebrew Typing Convertor has been successfully uninstalled from Windows Startup.",
                            "Uninstall Successful",
                            64 # MB_ICONINFORMATION
                        )
                        # Terminate all running instances of this executable
                        import subprocess
                        subprocess.run("taskkill /f /im HebrewTypingConvertor.exe", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except Exception as e:
                        ctypes.windll.user32.MessageBoxW(
                            0,
                            f"Failed to delete startup shortcut: {e}",
                            "Uninstall Failed",
                            16 # MB_ICONERROR
                        )
                    sys.exit(0)
            return
            
        if is_frozen:
            import ctypes
            # MB_YESNO (4) | MB_ICONQUESTION (32) = 36
            res = ctypes.windll.user32.MessageBoxW(
                0,
                "Would you like to install Hebrew Typing Convertor and run it automatically on Windows startup?",
                "Install Hebrew Typing Convertor",
                36
            )
            if res != 6:  # 6 is IDYES. If user clicked No (7) or closed it, exit immediately.
                sys.exit(0)
        
        import subprocess
        # Powershell script to create shortcut (.lnk) with '--startup' argument
        ps_cmd = (
            f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_path}'); "
            f"$s.TargetPath = '{current_path}'; "
            f"$s.Arguments = '--startup'; "
            f"$s.WorkingDirectory = '{os.path.dirname(current_path)}'; "
            f"$s.Save()"
        )
        cmd = f'powershell -NoProfile -Command "{ps_cmd}"'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Show success popup notification if running as compiled EXE
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

_instance_mutex = None

def check_single_instance():
    """Uses a Windows Mutex to ensure only one instance of the app runs at a time."""
    global _instance_mutex
    try:
        import ctypes
        # Create a unique named global mutex
        _instance_mutex = ctypes.windll.kernel32.CreateMutexW(None, True, "Global\\HebrewTypingConvertorMutex")
        if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            # If manually run (not on boot), alert the user that it is already running
            if '--startup' not in sys.argv and getattr(sys, 'frozen', False):
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "Hebrew Typing Convertor is already running in the background!\n\nUse Ctrl+Shift+Y to translate highlighted text.",
                    "Already Running",
                    64 # MB_ICONINFORMATION
                )
            sys.exit(0)
    except Exception:
        pass

def main():
    is_startup = '--startup' in sys.argv
    setup_startup(is_startup)
    check_single_instance()
    
    # If this is a manual launch, show a quick notification that it is running in background
    if not is_startup and getattr(sys, 'frozen', False):
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            "Hebrew Typing Convertor is now running in the background!\n\nUse Ctrl+Shift+Y to translate highlighted text.",
            "Running",
            64 # MB_ICONINFORMATION
        )
        
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
