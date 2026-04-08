#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml",
# ]
# ///
"""
Sync blog posts from Obsidian vault to Hugo site.
Converts wiki-links, handles assets, and respects the 'publish' frontmatter field.
"""

import os
import re
import shutil
import yaml
from pathlib import Path

# Configuration
OBSIDIAN_BLOG_DIR = Path.home() / "Documents" / "Main" / "Blog"
HUGO_CONTENT_DIR = Path(__file__).parent / "src" / "blog" / "content" / "posts"
HUGO_STATIC_DIR = Path(__file__).parent / "src" / "blog" / "static"

def parse_frontmatter(content):
    """Extract and parse YAML frontmatter from markdown content."""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        return None, content

    try:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    except yaml.YAMLError:
        return None, content

def extract_date_from_filename(filename):
    """Extract date from filename in format YYYY-MM-DD-post-name.md"""
    date_pattern = r'^(\d{4}-\d{2}-\d{2})-'
    match = re.match(date_pattern, filename)
    if match:
        return match.group(1)
    return None

def convert_wikilinks(content, posts_map):
    """
    Convert Obsidian wiki-links [[Link Text]] to Hugo markdown links.
    posts_map is a dict of {filename: slug} for resolving links between posts.
    """
    def replace_wikilink(match):
        link_text = match.group(1)
        # Handle [[Post Title|Display Text]] format
        if '|' in link_text:
            post_title, display_text = link_text.split('|', 1)
        else:
            post_title = display_text = link_text

        # Convert to slug (basic slugification)
        slug = post_title.lower().strip().replace(' ', '-')
        slug = re.sub(r'[^\w\-]', '', slug)

        # Create Hugo link
        return f'[{display_text}](/blog/posts/{slug}/)'

    # Match [[wiki links]]
    return re.sub(r'\[\[([^\]]+)\]\]', replace_wikilink, content)

def convert_image_paths(content):
    """Convert Obsidian image paths to Hugo static paths."""
    # Match ![[image.png]] format
    def replace_image(match):
        image_name = match.group(1)
        # Remove any path components, just use filename
        image_name = os.path.basename(image_name)
        return f'![](/blog/assets/{image_name})'

    content = re.sub(r'!\[\[([^\]]+)\]\]', replace_image, content)

    # Also handle standard markdown images that reference assets
    def replace_md_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        if 'assets/' in image_path:
            image_name = os.path.basename(image_path)
            return f'![{alt_text}](/blog/assets/{image_name})'
        return match.group(0)

    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_md_image, content)

    return content

def sync_posts():
    """Main sync function."""
    print(f"Syncing from {OBSIDIAN_BLOG_DIR} to {HUGO_CONTENT_DIR}")

    # Create directories if they don't exist
    HUGO_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    HUGO_STATIC_DIR.mkdir(parents=True, exist_ok=True)

    # Clear existing posts
    if HUGO_CONTENT_DIR.exists():
        for file in HUGO_CONTENT_DIR.glob("*.md"):
            file.unlink()

    # Build a map of posts for wiki-link resolution
    posts_map = {}

    # Process markdown files
    posts_synced = 0
    posts_skipped = 0

    for md_file in OBSIDIAN_BLOG_DIR.glob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter
        frontmatter, body = parse_frontmatter(content)

        # Skip if publish is false or missing
        if not frontmatter or not frontmatter.get('publish', False):
            print(f"  Skipping {md_file.name} (publish: false or missing)")
            posts_skipped += 1
            continue

        # Extract date from filename and add to frontmatter if not present
        if 'date' not in frontmatter:
            file_date = extract_date_from_filename(md_file.name)
            if file_date:
                frontmatter['date'] = file_date

        # Convert wiki-links and image paths
        body = convert_wikilinks(body, posts_map)
        body = convert_image_paths(body)

        # Reconstruct the file with frontmatter
        new_content = "---\n"
        new_content += yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        new_content += "---\n\n"
        new_content += body

        # Write to Hugo content directory
        dest_file = HUGO_CONTENT_DIR / md_file.name
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✓ Synced {md_file.name}")
        posts_synced += 1

    # Sync assets folder
    obsidian_assets = OBSIDIAN_BLOG_DIR / "assets"
    hugo_assets = HUGO_STATIC_DIR / "assets"

    if obsidian_assets.exists():
        # Remove old assets
        if hugo_assets.exists():
            shutil.rmtree(hugo_assets)

        # Copy new assets
        shutil.copytree(obsidian_assets, hugo_assets)
        asset_count = len(list(hugo_assets.rglob("*")))
        print(f"  ✓ Synced assets folder ({asset_count} files)")

    print(f"\nSync complete: {posts_synced} posts synced, {posts_skipped} posts skipped")

if __name__ == "__main__":
    try:
        sync_posts()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
