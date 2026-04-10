---
date: '2026-04-10'
layout: post
publish: true
title: How I track my workouts as markdown
---

Over the last three months I've begun tracking my workouts as individual markdown files.

When I first started tracking my workouts, I was tracking them on paper. This was fine and convenient, but it was a pain when I traveled because I'd have to write them down in a separate note and remember to copy them over later.

I later moved to tracking all the workouts for a given month in markdown. The files were innamed `2025-08 Workout log.md` and would have headings for each day and workout.

Here's an example:
```
### 2025-08-04
- Bicep curls
	- Work
		- 28/18/15 @ 20
- Lat raises
	- Work
		- 21/19 @ 10
- One arm dumbbell rows
	- Warm
		- 6 @ 20
	- Work
		- 12/12 @ 50

### 2025-08-05
Still a bit sick, but mostly good

- Bench press 
	- Warm
		- 6 @ 20
		- 6 @ 30
	- Work
		- 12/12/8 @ 50
- Flys
	- 9/11 @ 20
	- Focusing on a deep stretch at the bottom. Makes the reps much harder.
- Rear delt flys
	- Warm
		- 6 @ 10
	- Work
		- Moving up to 15
		- 13/11+6 @ 15
```

This format was focused around semi-structured data. The core idea was that I didn't want to force myself into everything being super structured, but also maintain some consistency.

These files actually became kind of a pain to deal with, partially because of some Obsidian Sync conflicts. These are documented on the forum and have been somewhat resolved, but I still get the conflicts on occasion.

Moving to a single file per workout has a good few advantages:

- Files are atomic - they track a single workout session
- File contents remain semi-structured with weight and rep data, as well as my thoughts and notes
- Individual files play well with Obsidian Bases
- This solves my Obsidian Sync conflict issues

An example of my new format is:
```
---
tags:
  - workout-log
date: 2026-03-17
workout_type: Pull
max_bpm: 150
---
### Bicep curls
Working set:
- 21 @ 25
- 12 @ 25
- 10 @ 25

### Lateral raises
Working set:
- 17 @ 15
- 16 @ 15

### One arm dumbbell rows
Warm up:
- 6 @ 25

Skipped the usual 35lb warmup set. May be overkill.

Working set:
- 12 @ 45
```

For cardio workouts, there is some additional metadata surrounding distance and time.

I found this new format much easier to deal with and nice to visualize with Obsidian Bases.