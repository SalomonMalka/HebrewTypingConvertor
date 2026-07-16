#Requires AutoHotkey v2.0
#SingleInstance Force

/*
Hebrew / English Keyboard Layout Translator
This utility runs in the background and corrects text typed in the wrong keyboard layout.
Default shortcut: Ctrl+Shift+Y
*/

; --- Mappings ---
engToHeb := Map(
    "`", ";", "q", "/", "w", "'", "e", "ק", "r", "ר", "t", "א", "y", "ט", "u", "ו", "i", "ן", "o", "ם", "p", "פ",
    "[", "[", "]", "]", "\", "\", "a", "ש", "s", "ד", "d", "ג", "f", "כ", "g", "ע", "h", "י", "j", "ח",
    "k", "ל", "l", "ך", ";", "ף", "'", ",", "z", "ז", "x", "ס", "c", "ב", "v", "ה", "b", "נ", "n", "מ",
    "m", "צ", ",", "ת", ".", "ץ", "/", ".",
    "~", "~", "Q", "/", "W", "'", "E", "ק", "R", "ר", "T", "א", "Y", "ט", "U", "ו", "I", "ן", "O", "ם", "P", "פ",
    "{", "}", "}", "{", "|", "|", "A", "ש", "S", "ד", "D", "ג", "F", "כ", "G", "ע", "H", "י", "J", "ח",
    "K", "ל", "L", "ך", ":", "ף", '"', ",", "Z", "ז", "X", "ס", "C", "ב", "V", "ה", "B", "נ", "N", "מ",
    "M", "צ", "<", "ת", ">", "ץ", "?", "."
)

hebToEng := Map(
    ";", "`", "/", "q", "'", "w", "ק", "e", "ר", "r", "א", "t", "ט", "y", "ו", "u", "ן", "i", "ם", "o", "פ", "p",
    "ש", "a", "ד", "s", "ג", "d", "כ", "f", "ע", "g", "י", "h", "ח", "j", "ל", "k", "ך", "l", "ף", ";",
    ",", "'", "ז", "z", "ס", "x", "ב", "c", "ה", "v", "נ", "b", "מ", "n", "צ", "m", "ת", ",", "ץ", ".",
    ".", "/"
)

ContainsHebrew(text) {
    ; Matches Hebrew Unicode range (0590 - 05FE)
    return RegExMatch(text, "[\x{0590}-\x{05FE}]")
}

TranslateText(text) {
    if (text = "")
        return ""
        
    toEnglish := ContainsHebrew(text)
    mapping := toEnglish ? hebToEng : engToHeb
    
    translated := ""
    Loop Parse, text {
        char := A_LoopField
        if (mapping.Has(char)) {
            translated .= mapping[char]
        } else {
            translated .= char
        }
    }
    return translated
}

FixLayout() {
    ; Backup current clipboard
    oldClip := ClipboardAll()
    
    ; Clear clipboard for detection
    A_Clipboard := ""
    
    ; Send Copy command
    Send("^c")
    
    ; Wait for clipboard content, max 200ms
    if (!ClipWait(0.2)) {
        A_Clipboard := oldClip
        return
    }
    
    copied := A_Clipboard
    translated := TranslateText(copied)
    
    ; If the translated text is identical, do nothing
    if (translated == copied) {
        A_Clipboard := oldClip
        return
    }
    
    ; Paste translated text
    A_Clipboard := translated
    Send("^v")
    
    ; Wait for paste to complete (150ms) before restoring old clipboard
    Sleep(150)
    A_Clipboard := oldClip
}

; Ctrl+Shift+Y Key triggers the fixer
^+y::FixLayout()
