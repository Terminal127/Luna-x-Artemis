import os

def count_lines_and_files_in_py(folder_path):
    total_lines = 0
    total_py_files = 0

    for root, dirs, files in os.walk(folder_path):
        py_files = [file for file in files if file.endswith(".py")]
        total_py_files += len(py_files)

        for file_name in py_files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                total_lines += len(lines)

    return total_lines, total_py_files

if __name__ == "__main__":
    folder_path = "C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna"  # Replace with the actual path to your folder
    lines_count, py_files_count = count_lines_and_files_in_py(folder_path)

    print(f"Total lines in .py files: {lines_count}")
    print(f"Total number of .py files: {py_files_count}")
