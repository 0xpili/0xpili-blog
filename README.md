[content above]
# Static Blog Generator

A minimalist, dark-themed static blog generator built with Python. Creates a clean, responsive blog with markdown support.

## Features

- 🌙 Dark mode by default
- 📱 Responsive design
- ✍️ Markdown support
- 🎨 Clean typography with Space Grotesk & Inter fonts
- 🚀 Easy deployment to GitHub Pages
- 💜 Purple accent colors
- 🔗 Social media links

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone this repository:
- bash
- git clone https://github.com/yourusername/blog.git
- cd blog
2. Install required packages:
- bash
- pip install markdown2 jinja2
```

### Usage

1. Add your blog posts as markdown files in the `posts/` directory
2. Run the blog generator:
- bash:README.md
- python blogmaker.py
```

3. Your blog will be generated in the `docs/` directory

### File Structure
README.md
blog/
├── blogmaker.py # Main generator script
├── posts/ # Your markdown blog posts
│ └── .md
├── templates/ # HTML templates
│ ├── base.html # Post template
│ └── index.html # Homepage template
└── docs/ # Generated blog (GitHub Pages)
## Customization

### Adding a New Post

1. Create a new markdown file in `posts/`


- Easy

```

2. Run `python blogmaker.py` to generate the site

### Modifying the Theme

- Edit `templates/base.html` for post styling
- Edit `templates/index.html` for homepage styling
- Colors and fonts can be modified in the CSS sections

## Deployment

### GitHub Pages

1. Push your changes to GitHub

2. Enable GitHub Pages in your repository settings:
   - Go to Settings → Pages
   - Set source to "Deploy from a branch"
   - Select "main" branch and "/docs" folder
   - Save

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











































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































