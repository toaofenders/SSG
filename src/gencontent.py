import os
from markdown_blocks import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
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

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Read the template file
    with open(template_path, 'r') as template_file:
        template = template_file.read()

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
                 # Read the markdown file
                with open(entry_path, 'r') as md_file:
                    markdown_content = md_file.read()

                node = markdown_to_html_node(markdown_content)
                html = node.to_html()
                #print(f"html: {html}")
                # Confirm HTML is correct before the replacement step
                #print("Converted HTML Before Replacement:", html)

                # Ensure template contains the correct placeholder
                #print("Template Before Replacement:", template)

                # Check if the placeholder `{{ content }}` is present
                if '{{ content }}' not in template:
                    print("Placeholder not found!")

                # Replace the placeholder in the template
                html_content = template.replace('{{ Content }}', html)
                # Check the final HTML content post-replacement
                #print("Final HTML Content After Replacement:", html_content)
                # Write the HTML file to the destination directory
                html_file_path = os.path.join(dest_dir_path, entry_relative_path.replace('.md', '.html'))
                with open(html_file_path, 'w') as html_file:
                    html_file.write(html_content)

    # Start processing from the root content directory
    process_directory(dir_path_content, '')

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No H1 header found")