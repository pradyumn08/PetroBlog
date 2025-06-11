import os
import re
from check_chart_scripts import find_broken_chart_blogs

def wrap_script_content(script_content):
    """Wraps the given JavaScript content in a DOMContentLoaded event listener."""
    # First, strip any leading/trailing whitespace to ensure clean wrapping.
    stripped_content = script_content.strip()
    # Indent the original script content for readability inside the new function.
    indented_content = "\n".join([f"    {line}" for line in stripped_content.split('\n')])
    return f"\ndocument.addEventListener('DOMContentLoaded', function() {{\n{indented_content}\n}});\n"

def fix_blog_scripts(blogs_dir, files_to_fix):
    """
    Corrects inline scripts in specified HTML files by wrapping them in a 
    'DOMContentLoaded' event listener.

    Args:
        blogs_dir (str): The path to the directory containing blog HTML files.
        files_to_fix (list): A list of filenames to be corrected.
    
    Returns:
        int: The number of files successfully fixed.
    """
    fixed_count = 0
    for filename in files_to_fix:
        filepath = os.path.join(blogs_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Find all inline script tags and replace their content.
            # This regex ensures we only target script tags that do not have a 'src' attribute.
            def replace_script(match):
                script_content = match.group(1)
                # Only wrap non-empty scripts that don't already have the listener.
                if script_content.strip() and 'DOMContentLoaded' not in script_content:
                    wrapped_content = wrap_script_content(script_content)
                    return f"<script>{wrapped_content}</script>"
                else:
                    # Return the original script tag if it's empty or already correct.
                    return match.group(0)

            # Use a non-greedy search to handle multiple script tags correctly.
            new_content = re.sub(r'<script(?![^>]*src=)>([\s\S]*?)</script>', replace_script, content)

            # If changes were made, write them back to the file.
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"- Fixed: {filename}")
                fixed_count += 1

        except Exception as e:
            print(f"- Error processing {filename}: {e}")
            
    return fixed_count

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    blogs_directory = os.path.join(project_root, "blogs")

    print("Step 1: Finding blogs with broken chart scripts...")
    broken_files = find_broken_chart_blogs(blogs_directory)

    if not broken_files:
        print("\nNo broken blog files found. Nothing to fix.")
    else:
        print(f"\nFound {len(broken_files)} blogs to fix.")
        print("\nStep 2: Applying fixes...")
        
        num_fixed = fix_blog_scripts(blogs_directory, broken_files)
        
        print(f"\nFix process complete. Successfully fixed {num_fixed} out of {len(broken_files)} files.")
