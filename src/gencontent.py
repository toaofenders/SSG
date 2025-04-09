import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, 'r')
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, 'r')
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # function to process each directory and file
    def process_directory(current_path, relative_path):
        print(current_path, relative_path)
        for entry in os.listdir(current_path):
            entry_path = os.path.join(current_path, entry)
            entry_relative_path = os.path.join(relative_path, entry)

            if os.path.isdir(entry_path):
                # Create corresponding directory in the destination path
                dest_dir = os.path.join(dest_dir_path, entry_relative_path)
                os.makedirs(dest_dir, exist_ok=True)
                # Recursively process the subdirectory
                process_directory(entry_path, entry_relative_path)
            elif entry.endswith('.md'):
                # Determine the destination HTML file path
                html_file_path = os.path.join(dest_dir_path, entry_relative_path.replace('.md', '.html'))
                
                # Use generate_page to handle the conversion and writing
                generate_page(entry_path, template_path, html_file_path, basepath)

    # Start processing from the root content directory
    process_directory(dir_path_content, '')

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No H1 header found")