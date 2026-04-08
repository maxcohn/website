---
date: '2020-05-10'
layout: post
publish: true
title: 'Fun with UNIX: Mass image collection and compilation'
---

*Disclaimer: This is not the most efficient or elegant scripting you'll ever see.
I know there are better ways to go about doing what I did, but this is what
popped in my head when I was doing the scraping*

One of my favorite things that I found too late is the power of a Unix command
line environment. I had been used to basic navigation and editing in via SSH from
some courses, but I didn't take the dive into really loving Unix until a bit over
a year ago. I really love the composibility of the standard Unix utilities that
form the "Unix Philosophy", and it's something that I've gone out of my way to
become aquainted with (which usually results in me taking much longer to learn
how to do a task, ironically).

Actual shell scripting is something that I never had to work with very much, aside
from the usual small automation tasks. That's where this little adventure comes in.
I wanted to download every image of a web comic that was separated by chapter, and
then take each respective chapter and compile that into a PDF that is one page per
image.

## Step 1 - Scraping

Here's an example of the basic web structure of the website I was scraping:
```
Comic Website
|-- Chapter 250 (/chapter-250)
	|-- 001.jpg
	|-- 002.jpg
	|-- 003.jpg
	...
	|-- 050.jpg
|-- Chapter 249 (/chapter-249)
...
|-- Chapter 1 (/chapter-1)
```

My first instinct is to use Python and Requests and do some basic scraping. This
would definitely have been the fastest solution for scraping for me because this
is how I'm used to scraping. Despite this, I wanted to learn a bit more of `wget`.
I have used wget a little bit in the pasted and was amazed by how powerful it
can be, if used right. At first, I tried using wget on the root of the website
with `-r` for a recursive scrape. This ended up leading me to a lot of pages I
didn't want, so I took a step back.

Thankfully, all the URLs I wanted to scrape had a standard format, so I decided
I could just loop from 1 to 250 and wget on the specific page to download the
images. Below is the script I used:

``` bash
 for URL in $(echo https://website.com/chapter-{1..250}); do 
     NUM="$(echo $URL | egrep -o '[0-9]+$')"
     wget -H -w 1 -nd -p -P $NUM -A jpg,jpeg,png,gif $URL 2> /dev/null
 done
```

### What's going on?

I'm looping over a sequence of URLs that are created by the string containing
`{1..250}`. That expression creates a string that contains `https://website.com/
chapter-` followed by a number for each number in the specified range. Very handy
when you have a series of files with sequential names.

Next I got the number of the chapter from piping the URL into grep and only taking
the last numbers in the URL.

Now for the actual wget call. Each call is only scrapes a single chapter page,
which consits of series of images from an external host, named in order (001, 002,
etc.).

* `-H` - Span hosts. Allows us to scrape across multiple hosts. This is needed
because the images are hosted on another site.
* `-w 1` - Wait seconds. This waits one second between requests. It makes the
whole process longer, but it prevents us from over loading the image host.
* `-nd` - No directories. By default, wget creates a directory structure based
on its traversal.
* `-p` - Page requisites. Gets all the files needed.
* `-P $NUM` - Directory prefix. This is the name of the directory wget will store
everything it scrapes into. I just named the directory the name of the chapter.
* `-A jpg,jpeg,png,gif` - Accept list. These are the files we want to accept. In
this case, I just care about images.

After this script runs for quite some time (because of `-w`), I was left with
about 250 directories that each have between 20 and 50 images, numbered in order.
wget is a very powerful tool with tons of options that probably would have made
it possible to do all of what I did with a single command, but I wasn't aware and
just hopped right into this solution. After doing all of this, it seems like using
`-l 1` may have allowed me to do this. This limits a recursive wget call to a
certain depth, in this case, 1.

## Step 2 - Compiling to PDF

All of these images would make for a completely find viewing experience, but I'd
perfer to have them as a PDF. It's a bit nicer to read on a mobile device, and
it seems kind of fun to do.

After a short Google search, I found that ImageMagick was the tool I wanted.
ImageMagick made this entire process trivial. Here's the code I used.

```bash
for I in $(seq 1 276); do
	magick "$I/*.jpg" "$I/$I.pdf"
done
```

Very simple. I had just learned about `seq` when I wrote this, so I wanted to use
it. This just takes all of the jpg files (all the images were jpg in this case)
and turn them into a PDF in order. Thanks ImageMagick for doing all the heavy
lifting.

Tons of people can do this faster and more efficient than me, but I'm still in
the process of learning. It's things like this that I think are so neat,
especially for less than 10 lines of code.

In the future, I'll use the following commands to download the latest chapter
each week:

```bash
wget -H -w 1 -nd -p -P $NUM -A jpg,jpeg,png,gif $URL 2> /dev/null
magick "$NUM/*.jpg" "$NUM.pdf"
```

And with that, I could even set up a cron job to do take care of that.

I just really like this kind of thing, and I thought it would be a neat write up.
Hopefully I end up writing more about my data wrangling escapades.
