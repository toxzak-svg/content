import os
import sqlite3
import pathlib

# Configuration
# Point this to the local 'files/en-us/web/api' folder in your cloned repo
SOURCE_DIR = r"C:\dev\projects\WebAlchemist\content\files\en-us\web\api"
DATABASE_NAME = "webgpu_docs.db"

def scrape_to_db():
    # 1. Connect to/Create the Database
conn = sqlite3.connect(DATABASE_NAME)    
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            path TEXT,
            content TEXT,
            category TEXT
        )
    ''')

    # 2. Walk through the directories
    # We target folders containing 'gpu' or 'wgsl'
    for root, dirs, files in os.walk(SOURCE_DIR):
        folder_name = os.path.basename(root).lower()
        if "gpu" in folder_name or "wgsl" in folder_name:
            if "index.md" in files:
                file_path = os.path.join(root, "index.md")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determine category for better LLM context
                category = "WGSL" if "wgsl" in folder_name else "WebGPU"
                
                # Insert into DB
                cursor.execute('''
                    INSERT INTO documentation (title, path, content, category)
                    VALUES (?, ?, ?, ?)
                ''', (folder_name, root, content, category))
                print(f"Added to DB: {folder_name}")

    conn.commit()
    conn.close()
    print("\nScraping complete. Database 'webgpu_docs.db' is ready.")

if __name__ == "__main__":
    scrape_to_db()