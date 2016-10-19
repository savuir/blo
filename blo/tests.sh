#!/bin/bash

echo "Script for smoke testing, creates, makes posts, builds, and serves blog"

python blog.py create testblog
cd testblog

python ../blog.py post about --type page

python ../blog.py post hello-worlds
echo "title: Hello worlds 2
briefing: A good story A brief description of page.
slug: hello-worlds2
tags: hello, worlds
date_time: 2015-12-12 19:52
type: post

## Title 1

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Code test

    :::python
    # Code goes here ...
    for i in range(10):
        print 'lol'
" > _blog/pages/2015-12-12__hello-worlds2.md

echo "title: Another page
briefing: A good story A brief description of page.
date_time: 2015-12-12 19:52
slug: another-page
tags: worlds, lol
type: post

## Title 1

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
" > _blog/pages/2015-12-11__another-page.md


for i in {1..59}; do
    echo "title: Another page ${i}
briefing: A good story A brief description of page.
date_time: 2015-12-12 19:${i}
slug: another-page-${i}
tags: ok
type: post

## Title 1

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
" > _blog/pages/2015-12-11__another-page-${i}.md
done


python ../blog.py build

tree

echo "Ctrl+C to exit serve mode, then script will remove test dir."
python ../blog.py serve

cd ../
rm -rf testblog