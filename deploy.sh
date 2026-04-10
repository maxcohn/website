#!/bin/sh
#
#

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
. "$SCRIPT_DIR/.env"

#TODO: more reliable way to get the current repo's path
# Sync the blog
rsync -avz --delete \
    "$SCRIPT_DIR/src/blog/public/" \
    "${WEBSITE_SSH_HOST}:${WEBSITE_WWW_PATH}/blog"

# Sync the other files
rsync -avz \
  "$SCRIPT_DIR/src/index.html" \
  "$SCRIPT_DIR/src/style.css" \
  "$SCRIPT_DIR/src/tools" \
  "${WEBSITE_SSH_HOST}:${WEBSITE_WWW_PATH}"

