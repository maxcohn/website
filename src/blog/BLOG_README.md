# Blog Setup

Note that only the `public/` directory is the site that gets synced to nginx.

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

## File Structure

```
website/
├── README.md               # Project readme
├── build.sh                # Build script
├── sync-blog.py            # Obsidian → Hugo sync script
└── src/                    # Website source files
    ├── index.html          # Main homepage
    ├── style.css           # Main styles
    └── blog/               # Hugo site
        ├── hugo.toml       # Hugo configuration
        ├── content/posts/  # Synced blog posts
        ├── static/assets/  # Synced images/assets
        ├── themes/         # Hugo themes
        └── public/         # Built output (deploy this)
```

## Notes

- The blog is accessible at `/blog/` on your site
- Individual posts are at `/blog/posts/post-name/`
- Wiki-links between posts are automatically converted
- Images in the `assets/` folder are accessible at `/blog/assets/filename`
