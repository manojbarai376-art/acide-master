import os

# फुल और फाइनल प्रोजेक्ट स्ट्रक्चर की पूरी लिस्ट
structure = {
    "core": [
        "__init__.py",
        "config.py",
        "logger.py",
        "security.py"
    ],
    "database": [
        "__init__.py",
        "db_manager.py",
        "models.py",
        "storage.json"
    ],
    "scraper": [
        "__init__.py",
        "base_scraper.py",
        "anime_shield.py",
        "parser.py",
        "proxy_manager.py",
        "ai_healer.py",
        "scheduler.py"
    ],
    "api": [
        "__init__.py",
        "server.py",
        "routes.py"
    ],
    "ui": [
        "__init__.py",
        "app_styles.py"
    ],
    "ui/controllers": [
        "main_controller.py"
    ],
    "ui/components": [
        "sidebar.py",
        "player_widget.py"
    ],
    "ui/screens": [
        "home_screen.py",
        "catalog_screen.py",
        "player_screen.py"
    ],
    "utils": [
        "__init__.py",
        "exceptions.py",
        "helpers.py"
    ],
    "assets/icons": [],
    "assets/fonts": [],
    "tests": [
        "__init__.py",
        "test_scraper.py",
        "test_db.py"
    ]
}

# रूट लेवल की फाइलें
root_files = [
    ".env.example",
    ".gitignore",
    "README.md",
    "requirements.txt",
    "Dockerfile",
    "main.py"
]

def create_project_structure():
    print("🚀 ACID Project Setup Starting...")
    
    # फोल्डर और उनके अंदर की फाइलें बनाना
    for folder, files in structure.items():
        os.makedirs(folder, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder, file)
            if not os.path.exists(file_path):
                if file == "storage.json":
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write('{\n    "anime_list": []\n}')
                else:
                    open(file_path, "w").close()
                print(f"Created file: {file_path}")

    # रूट फाइलें बनाना
    for file in root_files:
        if not os.path.exists(file):
            if file == "requirements.txt":
                with open(file, "w", encoding="utf-8") as f:
                    f.write("requests\nbeautifulsoup4\ncustomtkinter\n")
            else:
                open(file, "w").close()
            print(f"Created root file: {file}")

    print("\n✨ Sabhi folders aur files apne aap successfully ban gayi hain भाई!")

if __name__ == "__main__":
    create_project_structure()