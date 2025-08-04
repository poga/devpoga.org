#!/usr/bin/env python3
# /// script
# dependencies = [
#   "beautifulsoup4",
# ]
# ///

import os
import re
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

BLOG_URL = 'https://devpoga.org'
BLOG_TITLE = 'Dev.Poga'
BLOG_DESCRIPTION = 'Personal blog of Poga - transforming complex problems into fast feedback loops'
AUTHOR_EMAIL = 'hi@devpoga.org'

def extract_posts_from_index():
    """Extract blog posts from the main index.html file"""
    index_path = Path(__file__).parent / 'index.html'
    
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    post_list = soup.find('ul', id='post-list')
    posts = []
    
    if post_list:
        for li in post_list.find_all('li'):
            text = li.get_text().strip()
            link = li.find('a')
            
            if link and re.match(r'^\d{4}-\d{2}-\d{2}:', text):
                match = re.match(r'^(\d{4}-\d{2}-\d{2}):\s*(.+)$', text)
                if match:
                    date_str, title = match.groups()
                    url = link.get('href')
                    
                    full_url = f"{BLOG_URL}{url}" if url.startswith('/') else url
                    path = url[1:] if url.startswith('/') else url
                    
                    posts.append({
                        'date': date_str,
                        'title': title.strip(),
                        'url': full_url,
                        'path': path
                    })
    
    # Sort by date, newest first
    posts.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    return posts

def extract_content_from_post(post_path):
    """Extract content from a blog post HTML file"""
    try:
        full_path = Path(__file__).parent / post_path / 'index.html'
        if not full_path.exists():
            return None
        
        with open(full_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        
        if not body:
            return None
        
        # Extract text content
        text = body.get_text()
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Find content after the first heading
        content_start = 0
        for i, line in enumerate(lines):
            if line.startswith('#') or 'home' in line.lower():
                content_start = i + 1
                break
        
        if content_start < len(lines):
            content = ' '.join(lines[content_start:])
        else:
            content = ' '.join(lines)
        
        # Truncate if too long
        if len(content) > 500:
            content = content[:500] + '...'
        
        return content
        
    except Exception as e:
        print(f"Error reading post {post_path}: {e}")
        return None

def generate_rss_item(post):
    """Generate RSS item XML for a single post"""
    content = extract_content_from_post(post['path'])
    description = content or post['title']
    
    # Convert date to RFC822 format
    post_date = datetime.strptime(post['date'], '%Y-%m-%d')
    pub_date = post_date.strftime('%a, %d %b %Y %H:%M:%S +0000')
    
    return f"""    <item>
      <title><![CDATA[{post['title']}]]></title>
      <link>{post['url']}</link>
      <guid>{post['url']}</guid>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[{description}]]></description>
    </item>"""

def generate_rss_feed(posts):
    """Generate complete RSS feed XML"""
    last_build_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    items = '\n'.join(generate_rss_item(post) for post in posts[:20])
    
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{BLOG_TITLE}</title>
    <link>{BLOG_URL}</link>
    <description>{BLOG_DESCRIPTION}</description>
    <language>en-us</language>
    <lastBuildDate>{last_build_date}</lastBuildDate>
    <atom:link href="{BLOG_URL}/rss.xml" rel="self" type="application/rss+xml" />
    <managingEditor>{AUTHOR_EMAIL} (Poga)</managingEditor>
    <webMaster>{AUTHOR_EMAIL} (Poga)</webMaster>
{items}
  </channel>
</rss>"""

def main():
    """Main function to generate RSS feed"""
    print('Generating RSS feed...')
    
    posts = extract_posts_from_index()
    print(f'Found {len(posts)} posts')
    
    if not posts:
        print('No posts found, skipping RSS generation')
        return
    
    rss_content = generate_rss_feed(posts)
    output_path = Path(__file__).parent / 'rss.xml'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rss_content)
    
    print(f'RSS feed generated: {output_path}')
    print(f'Latest post: {posts[0]["title"]} ({posts[0]["date"]})')

if __name__ == '__main__':
    main()