# tester.py - Version 2.6.0 (Generator Only)
import os
import shutil

def generate_test_environment():
    # We want to put these in the folder your main app actually looks at
    target_dir = "To_Be_Processed"
    
    # Refresh the folder
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    # The "Test Payload"
    test_files = {
        # Valid files that should be easy (Confidence High)
        "J.R.R. Tolkien - The Hobbit.rtf": "content",
        "Michael A. Stackpole - Warrior; Coupé.rtf": "content",
        
        # Typos/Vague names (Should trigger the Intervention UI)
        "George Orwell - 1983.txt": "content",
        "ax79_v01_final_final.txt": "content",
        
        # Junk files (Should be ignored by the app's filter)
        "Playlist_Summer.mp3": "audio data",
        "System_Log_Backup.mov": "video data"
    }

    print("--- EBOOK CREATOR TEST GENERATOR ---")
    for filename, content in test_files.items():
        path = os.path.join(target_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        print(f"Created: {filename}")

    print("\n" + "="*40)
    print(f"SUCCESS: {len(test_files)} files generated in '{target_dir}'.")
    print("You can now run 'main_gui.py' to test the Batch Mode.")
    print("="*40)

if __name__ == "__main__":
    generate_test_environment()