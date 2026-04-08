#!/bin/sh

die () {
    echo "$1"
    exit 1
}

cd src/blog || die "Failed to find 'src/blog' directory"

hugo