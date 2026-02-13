# tester.py - Version 2.0.0
import os
from converter_logic import eBookConverterLogic

def run_test_suite():
    print("Starting eBook Converter Test Suite v2.0.0...")
    logic = eBookConverterLogic()
    
    # 1. Create dummy RTF
    test_file = "test_input.rtf"
    with open(test_file, "w") as f:
        f.write(r"{\rtf1\ansi Test document content.}")
    
    print(f"Testing conversion of {test_file}...")
    
    # 2. Execute conversion
    success, result = logic.convert_to_epub(test_file, "Test Book", "Test Author")
    
    # 3. Validation
    if success and os.path.exists(result):
        print("✅ SUCCESS: EPUB generated successfully.")
        # Cleanup
        os.remove(test_file)
        os.remove(result)
        print("✅ SUCCESS: Cleanup completed.")
    else:
        print(f"❌ FAILED: {result}")
        if os.path.exists(test_file): os.remove(test_file)

if __name__ == "__main__":
    run_test_suite()