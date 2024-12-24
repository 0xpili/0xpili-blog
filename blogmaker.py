import os
import markdown2
from jinja2 import Template

# Define paths
TEMPLATES_DIR = "templates"
POSTS_DIR = "posts"
OUTPUT_DIR = "output"

def load_template(template_name):
    """Load a template by name."""
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    with open(template_path, "r") as file:
        return Template(file.read())

def convert_markdown_to_html(md_content):
    """Convert Markdown content to HTML."""
    return markdown2.markdown(md_content)

def save_html(output_path, html_content):
    """Save HTML content to a file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as file:
        file.write(html_content)

def generate_post_html(template, filename):
    """Generate HTML for a single post."""
    post_path = os.path.join(POSTS_DIR, filename)
    with open(post_path, "r") as file:
        md_content = file.read()
    post_html = convert_markdown_to_html(md_content)
    rendered_html = template.render(
        content=post_html,
        title=filename.replace(".md", ""),
    )
    output_path = os.path.join(OUTPUT_DIR, filename.replace(".md", ".html"))
    save_html(output_path, rendered_html)
    return filename.replace(".md", ".html")

def generate_index_html(post_files):
    """Generate a central hub listing all posts."""
    template = load_template("index.html")
    rendered_html = template.render(posts=post_files)
    save_html(os.path.join(OUTPUT_DIR, "index.html"), rendered_html)

def generate_blog():
    """Main function to generate the blog."""
    post_template = load_template("base.html")
    post_files = []  # List of posts for the index

    # Generate each post
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            post_html_filename = generate_post_html(post_template, filename)
            post_files.append({
                "title": filename.replace(".md", ""),  # Post title
                "link": post_html_filename             # HTML file link
            })

    # Generate index page
    generate_index_html(post_files)
    print(f"Blog generated! Open {os.path.join(OUTPUT_DIR, 'index.html')} to view your homepage.")

if __name__ == "__main__":
    generate_blog()

