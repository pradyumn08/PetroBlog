import os
import json

blogs_dir = 'blogs'
html_files = []

# Check if the blogs directory exists
if os.path.isdir(blogs_dir):
    # Walk through the blogs directory
    for file in os.listdir(blogs_dir):
        # Check if the file is an HTML file
        if file.endswith('.html'):
            # Prepend the directory to the filename for the correct path
            html_files.append(os.path.join(blogs_dir, file))

# Sort the files alphabetically for consistent ordering
html_files.sort()

# Write the list of HTML files to a JSON file
with open('blogs.json', 'w') as f:
    json.dump(html_files, f, indent=4)

print(f"Successfully generated blogs.json with {len(html_files)} files from the '{blogs_dir}' directory.")
