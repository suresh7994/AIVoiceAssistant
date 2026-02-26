"""
Test script for new file/folder management and project creation features
"""

import os
import shutil
from windsurf_controller import WindsurfController

def test_folder_operations():
    """Test folder creation and deletion"""
    print("\n=== Testing Folder Operations ===")
    wc = WindsurfController()
    
    # Test folder creation
    test_folder = "/tmp/test_voice_assistant_folder"
    result = wc.create_folder(test_folder)
    print(f"✓ Create folder: {result['success']} - {result.get('message', result.get('error'))}")
    
    # Verify folder exists
    assert os.path.exists(test_folder) and os.path.isdir(test_folder), "Folder should exist"
    print(f"✓ Folder exists: {os.path.exists(test_folder)}")
    
    # Test folder deletion
    result = wc.delete_folder(test_folder)
    print(f"✓ Delete folder: {result['success']} - {result.get('message', result.get('error'))}")
    
    # Verify folder deleted
    assert not os.path.exists(test_folder), "Folder should be deleted"
    print(f"✓ Folder deleted: {not os.path.exists(test_folder)}")

def test_file_operations():
    """Test file creation and deletion"""
    print("\n=== Testing File Operations ===")
    wc = WindsurfController()
    
    # Test file creation
    test_file = "/tmp/test_voice_assistant_file.txt"
    result = wc.create_file(test_file, "Test content")
    print(f"✓ Create file: {result['success']} - {result.get('message', result.get('error'))}")
    
    # Verify file exists
    assert os.path.exists(test_file) and os.path.isfile(test_file), "File should exist"
    print(f"✓ File exists: {os.path.exists(test_file)}")
    
    # Test file deletion
    result = wc.delete_file(test_file)
    print(f"✓ Delete file: {result['success']} - {result.get('message', result.get('error'))}")
    
    # Verify file deleted
    assert not os.path.exists(test_file), "File should be deleted"
    print(f"✓ File deleted: {not os.path.exists(test_file)}")

def test_project_creation():
    """Test project creation for different technologies"""
    print("\n=== Testing Project Creation ===")
    wc = WindsurfController()
    
    base_path = "/tmp/test_projects"
    os.makedirs(base_path, exist_ok=True)
    
    # Test Python project
    result = wc.create_project("test_python", "python", base_path)
    print(f"✓ Python project: {result['success']} - {result.get('message', result.get('error'))}")
    assert os.path.exists(f"{base_path}/test_python/main.py"), "Python main.py should exist"
    
    # Test Calculator project
    result = wc.create_project("test_calc", "calculator", base_path)
    print(f"✓ Calculator project: {result['success']} - {result.get('message', result.get('error'))}")
    assert os.path.exists(f"{base_path}/test_calc/calculator.py"), "Calculator.py should exist"
    
    # Test Flask project
    result = wc.create_project("test_flask", "flask", base_path)
    print(f"✓ Flask project: {result['success']} - {result.get('message', result.get('error'))}")
    assert os.path.exists(f"{base_path}/test_flask/app.py"), "Flask app.py should exist"
    assert os.path.exists(f"{base_path}/test_flask/templates"), "Templates folder should exist"
    
    # Test HTML project
    result = wc.create_project("test_html", "html", base_path)
    print(f"✓ HTML project: {result['success']} - {result.get('message', result.get('error'))}")
    assert os.path.exists(f"{base_path}/test_html/index.html"), "index.html should exist"
    assert os.path.exists(f"{base_path}/test_html/css"), "CSS folder should exist"
    
    # Cleanup
    shutil.rmtree(base_path)
    print(f"✓ Cleanup completed")

def test_recursive_delete():
    """Test recursive folder deletion"""
    print("\n=== Testing Recursive Folder Deletion ===")
    wc = WindsurfController()
    
    # Create folder with contents
    test_folder = "/tmp/test_recursive_delete"
    os.makedirs(test_folder, exist_ok=True)
    with open(f"{test_folder}/file1.txt", 'w') as f:
        f.write("test")
    os.makedirs(f"{test_folder}/subfolder", exist_ok=True)
    
    # Try non-recursive delete (should fail)
    result = wc.delete_folder(test_folder, recursive=False)
    print(f"✓ Non-recursive delete (should fail): {not result['success']}")
    assert not result['success'], "Non-recursive delete should fail on non-empty folder"
    
    # Try recursive delete (should succeed)
    result = wc.delete_folder(test_folder, recursive=True)
    print(f"✓ Recursive delete: {result['success']} - {result.get('message', result.get('error'))}")
    assert result['success'], "Recursive delete should succeed"
    assert not os.path.exists(test_folder), "Folder should be deleted"

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing New Voice Assistant Features")
    print("=" * 60)
    
    try:
        test_folder_operations()
        test_file_operations()
        test_project_creation()
        test_recursive_delete()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
