import os
import re

def find_broken_chart_blogs(blogs_dir):
    """
    Scans HTML files in a directory to find blogs that might have broken charts.

    A blog is considered potentially broken if it contains a <canvas> element
    but its inline <script> tag does not use a 'DOMContentLoaded' event listener,
    which is required for scripts that manipulate the DOM to run correctly when
    loaded dynamically.

    Args:
        blogs_dir (str): The path to the directory containing blog HTML files.

    Returns:
        list: A list of filenames for blogs with potentially broken charts.
    """
    broken_blogs = []
    if not os.path.isdir(blogs_dir):
        print(f"Error: Directory not found at '{blogs_dir}'")
        return broken_blogs

    for filename in os.listdir(blogs_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(blogs_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Check if the file contains a <canvas> tag.
                if '<canvas' not in content:
                    continue

                # Find all script tags with inline content.
                script_tags = re.findall(r'<script(?![^>]*src=)>([\s\S]*?)</script>', content)
                inline_scripts = [s for s in script_tags if s.strip()]

                if not inline_scripts:
                    continue

                # Check if any of the inline scripts have the required listener.
                has_dom_listener = False
                for script_content in inline_scripts:
                    if 'DOMContentLoaded' in script_content:
                        has_dom_listener = True
                        break
                
                # If a canvas exists but no script has the listener, flag it.
                if not has_dom_listener:
                    broken_blogs.append(filename)

            except Exception as e:
                print(f"Could not process file {filename}: {e}")

    return broken_blogs

if __name__ == "__main__":
    # Assume this script is in a 'tools' directory within the project root.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    blogs_directory = os.path.join(project_root, "blogs")
    
    print(f"Scanning for blogs in: {blogs_directory}")
    
    potentially_broken = find_broken_chart_blogs(blogs_directory)

    if potentially_broken:
        print("\nFound blogs with potentially broken charts:")
        print("(These files contain a <canvas> but their scripts lack a 'DOMContentLoaded' listener)\n")
        for blog_name in potentially_broken:
            print(f"- {blog_name}")
    else:
        print("\nScan complete. No blogs with potentially broken charts were found.")
