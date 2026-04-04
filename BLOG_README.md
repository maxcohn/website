# Blog Setup

This website uses a hybrid approach:
- Root site ([index.html](index.html), [style.css](style.css)) is static HTML
- Blog lives in `blog/` directory and is built with Hugo

## Workflow

### 1. Write posts in Obsidian
Write your posts in `~/Documents/Main/Blog/` with YAML frontmatter:

```yaml
---
title: "My Post Title"
publish: true
---
```

Posts with `publish: false` or missing the `publish` field won't be synced.

### 2. Sync posts from Obsidian
```bash
./sync-blog.py
```

This script:
- Copies posts with `publish: true` from your Obsidian vault
- Converts wiki-links `[[like this]]` to Hugo links
- Converts image references to use Hugo's static folder
- Copies the `assets/` folder

### 3. Build the blog
```bash
cd blog
hugo
```

This generates the static site in `blog/public/`

### 4. Deploy to your server

Your nginx webroot structure should look like:
```
/var/www/yoursite/          # Or wherever your nginx root is
├── index.html              # Your main page
├── style.css               # Your styles
└── blog/                   # Hugo blog output goes here
    ├── index.html
    ├── posts/
    ├── assets/
    └── ...
```

Deploy the root files and blog separately:

```bash
# Deploy root site files (index.html, style.css) - using include/exclude pattern
rsync -avz \
  --include='index.html' \
  --include='style.css' \
  --include='CNAME' \
  --exclude='*' \
  /home/max/Code/website/ \
  user@yourserver:/var/www/yoursite/

# Deploy blog content
rsync -avz --delete \
  /home/max/Code/website/blog/public/ \
  user@yourserver:/var/www/yoursite/blog/
```

Or use a simpler approach with explicit file listing:
```bash
# Deploy specific root files
rsync -avz \
  /home/max/Code/website/index.html \
  /home/max/Code/website/style.css \
  user@yourserver:/var/www/yoursite/

# Deploy blog content
rsync -avz --delete \
  /home/max/Code/website/blog/public/ \
  user@yourserver:/var/www/yoursite/blog/
```

## Development

To preview the blog locally:
```bash
cd blog
hugo server
```

Visit `http://localhost:1313/blog/`

## File Structure

```
website/
├── index.html              # Main homepage
├── style.css               # Main styles
├── sync-blog.py            # Obsidian → Hugo sync script
├── blog/                   # Hugo site
│   ├── config.toml         # Hugo configuration
│   ├── content/posts/      # Synced blog posts
│   ├── static/assets/      # Synced images/assets
│   ├── themes/paper/       # Minimal theme
│   └── public/             # Built output (deploy this)
└── BLOG_README.md          # This file
```

## Notes

- The blog is accessible at `/blog/` on your site
- Individual posts are at `/blog/posts/post-name/`
- Wiki-links between posts are automatically converted
- Images in the `assets/` folder are accessible at `/blog/assets/filename`
