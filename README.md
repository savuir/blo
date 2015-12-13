# Blo

**Blo** (*blog + bro*) - yet another static site generator for personal blogs. The aim is to make a really easy tool for creating new notes and customizing your site. Do less actions and have much opportunity to make a unique site.

## Features

 * Comfortable cli control.
 * Easy config edit in JSON files.
 * Drafts templates: defult content for new notes, useful for planning new posts.
 * Page templates: easy HTML/Jinja2 customize and improve.
 * SEO friendly (as I could make it).
 * Microformats for better snippets in Google/Bing/etc.
 * Markdown with use of meta-tags to customize pages more with diffirent data.
 * Code highlight with Pygments.
 * RSS feed generation


## Installation

     python setup.py install

## Usage
Create a new blog:

     blo create myblog
     cd myblog

Create a new page or post:

     blo post hello-world 
     
You can also use pipe with your favorite editor:

     blo post hello-world | xargs subl

Build blog:

     blo build

Run blog locally:

     blo serve
     
## Configurate

Global site variables and technical paths are in `default.json`.

Templates for diffirent types of content are in `draft_templates.json`

## Customize

### Adding a custom type of content

You can add you page HTML templates for diffirent types of content. 

1. Add new HTML template to `templates` folder with a name of post type (ex. `book.html`)
2. Add new draft template to `draft_templates.json`, you can also set an URL template and default content for new type of page
3. Now you can make new type of posts: `blo post just-for-fun --type book`
