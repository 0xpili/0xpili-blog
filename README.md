# MinimalistBlog Generator

A minimalist, dark-themed static blog generator built with Python. Creates a clean, responsive blog with markdown support.

## Features

- 🌙 Dark mode by default
- 📱 Responsive design
- ✍️ Markdown support
- 🎨 Clean typography with Space Grotesk & Inter fonts
- 🚀 Easy deployment to GitHub Pages
- 💜 Purple accent colors
- 🔗 Social media links

## 🚀 Quick Start

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone this repository:
```git clone https://github.com/yourusername/blog.git```
```cd blog```

2. Install required packages:
```pip install markdown2 jinja2```

### Usage

1. Add your blog posts as markdown files in the `posts/` directory
2. Run the blog generator:
```python blogmaker.py```

3. Your blog will be generated in the `docs/` directory

## 📁 Project Structure
```
blog/
├── blogmaker.py     # Main generator script
├── posts/          # Your markdown blog posts
│   └── *.md
├── templates/      # HTML templates
│   ├── base.html   # Post template
│   └── index.html  # Homepage template
└── docs/          # Generated blog (GitHub Pages)
```

## 📝 Customization

### Adding a New Post

1. Create a new markdown (.md) file in `posts/`

2. Run `python3 blogmaker.py` to generate the site

3. Run `git add .` to add the new post to the repository

4. Run `git commit -m "Added a new post"` to commit the changes

5. Run `git push` to push the changes to the repository

### Modifying the Theme

- Edit `templates/base.html` for post styling
- Edit `templates/index.html` for homepage styling
- Colors and fonts can be modified in the CSS sections

## Deployment

### GitHub Pages

1. Push your changes to GitHub

2. Enable GitHub Pages in your repository settings:
```
   - Go to Settings → Pages
   - Set source to "Deploy from a branch"
   - Select "main" branch and "/docs" folder
   - Save
   ```

Your blog will be available at `https://yourusername.github.io/blog`

## Recommendations

- Keep post filenames URL-friendly (use hyphens instead of spaces)
- Use markdown for consistent formatting
- Add images to a separate `images/` directory
- Regularly commit and push changes
- Test locally before deploying

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [Python](https://www.python.org/)
- Markdown parsing by [markdown2](https://github.com/trentm/python-markdown2)
- Templates with [Jinja2](https://jinja.palletsprojects.com/)
- Fonts from [Google Fonts](https://fonts.google.com/)








































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































