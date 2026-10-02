# ACID Master UI Themes and Color Palettes

class AppStyles:
    # डार्क साइबरपंक / एनीमे थीम कलर्स
    BG_DARK = "#0f1016"          # मुख्य बैकग्राउंड (गहरा काला/नीला)
    SURFACE_DARK = "#1a1c23"     # कार्ड्स और पैनल का बैकग्राउंड
    PRIMARY_ACCENT = "#ff4655"   # मुख्य हाइलाइट रंग (एनीमे रेड/पिंक)
    SECONDARY_ACCENT = "#00f0ff" # साइबर सायन (Neon Blue)
    TEXT_PRIMARY = "#ffffff"     # मुख्य सफेद टेक्स्ट
    TEXT_SECONDARY = "#8b9bb4"   # धुंधला ग्रे टेक्स्ट
    
    FONT_FAMILY = "Segoe UI"     # मॉडर्न फॅमिली फोंट

    @staticmethod
    def apply_theme(root_window):
        """विंडो पर ग्लोबल थीम या कॉन्फ़िगरेशन अप्लाई करने के लिए"""
        root_window.configure(bg=AppStyles.BG_DARK)

print("App Styles script ready!")