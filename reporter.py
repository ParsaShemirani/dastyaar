#!/usr/bin/env python3
import os

def write_tree_and_contents(root_dir: str, output_path: str, max_depth: int = 2):
    """
    Walks the directory up to max_depth (ignoring dot‑prefixed names), writes the tree structure,
    then writes the name and contents of each file found, and logs the root path.
    """
    with open(output_path, 'w', encoding='utf-8') as out_f:
        # Log the root directory path
        out_f.write(f"REPORT ROOT DIRECTORY: {os.path.abspath(root_dir)}\n")
        out_f.write("\n")

        # Part 1: Tree structure
        out_f.write(f"PROJECT TREE (up to {max_depth} levels, skipping dotfiles)\n")
        out_f.write("=" * 40 + "\n")
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Filter out dot‑dirs so we don’t descend into them
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            # Compute current depth
            rel_path = os.path.relpath(dirpath, root_dir)
            depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
            if depth > max_depth:
                dirnames[:] = []  # stop deeper descent
                continue

            indent = '    ' * depth
            out_f.write(f"{indent}{os.path.basename(dirpath) or '.'}/\n")

            # List non‑dot files only
            for fname in sorted(filenames):
                if fname.startswith('.'):
                    continue
                out_f.write(f"{indent}    {fname}\n")

        # Part 2: File contents
        out_f.write("\n\nFILE CONTENTS\n")
        out_f.write("=" * 40 + "\n")
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Again, skip dot‑dirs
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            rel_path = os.path.relpath(dirpath, root_dir)
            depth = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
            if depth > max_depth:
                dirnames[:] = []
                continue

            for fname in sorted(filenames):
                if fname.startswith('.'):
                    continue
                file_path = os.path.join(dirpath, fname)
                rel_file = os.path.relpath(file_path, root_dir)
                out_f.write(f"\n--- {rel_file} ---\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        out_f.write(f.read() + "\n")
                except Exception as e:
                    out_f.write(f"<Could not read file: {e}>\n")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(project_root, "project_report.txt")
    write_tree_and_contents(project_root, output_file, max_depth=2)
    print(f"All done! Report written to {output_file}")
