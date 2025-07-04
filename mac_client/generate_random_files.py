import os
import random
import string

def generate_random_text(length=100):
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length))

def create_random_files(directory, file_count=10, text_length=100):
    os.makedirs(directory, exist_ok=True)
    
    for i in range(file_count):
        filename = f"file_{i+1}.txt"
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            f.write(generate_random_text(text_length))
    print(f"Created {file_count} files in '{directory}'")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create files with random text.")
    parser.add_argument("directory", help="Directory to create the files in")
    parser.add_argument("--length", type=int, default=100, help="Length of random text in each file")
    args = parser.parse_args()

    create_random_files(args.directory, text_length=args.length)
