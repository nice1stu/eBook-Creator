# converter_logic.py - Version 2.6.2
import subprocess
import os
import requests
import re

class eBookConverterLogic:
    def __init__(self):
        self.version = "2.6.2"
        self.allowed_formats = ('.txt', '.rtf', '.docx', '.html')

    def sanitize_filename(self, filename):
        """Removes illegal characters and noise for the final filename."""
        clean = re.sub(r'LE\d+', '', filename, flags=re.I)
        clean = clean.replace(";", ",")
        clean = re.sub(r'[<>:"/\\|?*]', '', clean)
        return " ".join(clean.split()).strip()

    def parse_filename(self, filepath):
        """Expects: Author - Title"""
        filename = os.path.splitext(os.path.basename(filepath))[0]
        noise = [r'LE\d+', r'\b\d{4,5}\b', r'BattleTech']
        for pattern in noise:
            filename = re.sub(pattern, '', filename, flags=re.I)
        
        filename = re.sub(r'\s+', ' ', filename).strip(" -")
        
        if " - " in filename:
            parts = filename.split(" - ")
            # First part is Author, remainder is Title
            author = parts[0].strip()
            title = " - ".join(parts[1:]).strip()
            return title, author
        return filename, ""

    def fetch_metadata_online(self, title, author=""):
        """Fetches the best guess from Google without internal filtering."""
        search_query = f"{title} {author}".strip()
        url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults=1"
        try:
            response = requests.get(url, timeout=5).json()
            if "items" in response:
                info = response["items"][0]["volumeInfo"]
                return {
                    "title": info.get("title", "").split(":")[0].strip(),
                    "author": info.get("authors", ["Unknown"])[0],
                    "cover_url": info.get("imageLinks", {}).get("thumbnail")
                }
        except: pass
        return None

    def download_cover(self, url):
        if not url: return None
        try:
            r = requests.get(url, timeout=5)
            path = os.path.join(os.getcwd(), "temp_cover.jpg")
            with open(path, 'wb') as f: f.write(r.content)
            return path
        except: return None

    def convert_to_epub(self, input_path, output_folder, title, author, cover_path=None):
        if not os.path.exists(output_folder): os.makedirs(output_folder)
        # Use sanitized Author - Title.epub
        file_name = f"{self.sanitize_filename(author)} - {self.sanitize_filename(title)}.epub"
        output_path = os.path.join(output_folder, file_name)
        try:
            cmd = ['pandoc', input_path, '--metadata', f'title={title}', '--metadata', f'author={author}', '-o', output_path]
            if cover_path and os.path.exists(cover_path): cmd.extend(['--epub-cover-image', cover_path])
            subprocess.run(cmd, check=True, capture_output=True)
            return True, output_path
        except Exception as e: return False, str(e)