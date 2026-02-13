# converter_logic.py - Version 2.0.0
import subprocess
import os

class eBookConverterLogic:
    """Handles the conversion of various text formats to EPUB using Pandoc."""
    
    def __init__(self):
        self.version = "2.0.0"

    def convert_to_epub(self, input_path, title, author, cover_path=None):
        """
        Converts input file to EPUB with metadata.
        Supported inputs: .rtf, .txt, .docx, .pdf (via Pandoc)
        """
        if not os.path.exists(input_path):
            return False, "Input file not found."

        # Define output path (same name, .epub extension)
        output_path = os.path.splitext(input_path)[0] + ".epub"
        
        try:
            # Base command construction
            command = [
                'pandoc', 
                input_path, 
                '--metadata', f'title={title}', 
                '--metadata', f'author={author}',
                '-o', output_path
            ]
            
            # Add cover image flag if a path was provided
            if cover_path and os.path.exists(cover_path):
                command.extend(['--epub-cover-image', cover_path])
            
            # Run the process
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            return True, output_path

        except subprocess.CalledProcessError as e:
            # Return the specific error from Pandoc
            return False, f"Pandoc Error: {e.stderr}"
        except FileNotFoundError:
            return False, "System Error: Pandoc is not installed or not in PATH."