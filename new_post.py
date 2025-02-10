import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re

def slugify(title):
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower()
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug).strip('-')
    return slug

def create_post_directory(slug):
    # Create directory if it doesn't exist
    os.makedirs(slug, exist_ok=True)

    # Create index.html in the new directory
    template = f'''
    <!doctype html public "-//w3c//dtd html 4.0 transitional//en">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Dev.Poga</title>
  <script type="module" src="https://md-block.verou.me/md-block.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  <script>setTimeout(() => hljs.highlightAll(), 100);</script>
  <link rel="stylesheet" href="/index.css">
</head>
<body>
  <md-block>
[ [home] ](/)

  </md-block>
</body>
</html>'''
    with open(f'{slug}/index.html', 'w', encoding='utf-8') as f:
        f.write(template)

def update_index_html(title, slug):
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find the post list
    post_list = soup.find(id='post-list')

    # Create new list item with today's date
    today = datetime.now().strftime('%Y-%m-%d')
    new_item = soup.new_tag('li')
    new_item.string = f' {today}: '

    # Create and add the link
    link = soup.new_tag('a', href=f'/{slug}/')
    link.string = title
    new_item.append(link)

    # Insert at the beginning of the list
    post_list.insert(0, new_item)

    # Write the updated HTML
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python new_post.py \"Your Post Title\"")
        sys.exit(1)

    title = sys.argv[1]
    slug = slugify(title)

    create_post_directory(slug)
    update_index_html(title, slug)

    print(f"Created new post directory: {slug}/")
    print(f"Updated index.html with new post")
