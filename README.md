# highlighter
raw text highlighter that produces html

# What

"Make each program do one thing well."
"Write programs to handle text streams, because that is a universal interface."

This programs takes a raw text file, allows you to select text in it, allows you to save the selection in another raw text file and produces html with the same highlights.

# Why

Sometimes, you really just want to highlight something.

# Usecases

Highlight stuff in raw text. Like code, html source, csv, etc..

You can then grab the produced html and share it as a file. Via email or something. Without signing into a service. Imagine that. 2020 here we come.

# Pictures

![behold!](UI.png?raw=True)

# Longer Why

Highlighting is a visual form of commenting or referencing.

Comments exist on a meta layer, different than the subject text.

In Code, having comments in the code file is a tradeoff between portability and "clean" separation of content and format. Distributing the comment with the code is practical, but not clean.

"DRY" exists for good reason. It is also violated every time someone puts down something that should be documentation as a comment or adds another documentation website that doesn't link or integrate into other ALL the other documentation.

To start any of this, the proper first thing to do is to separate the meta layers. And if history has tought anything, raw text is still a pretty good idea to use.

I also think there are cases where you want to show a raw data dump and highlight something.

# Technical

uses tkinter, jinja2, json

The program creates a filename+"_selection_data_dum.txt" that saves the selection as start,end,selection_string

It produces the html with jinja2, slicing the text and highlighting with <a> tags and background color. Ideally you should be able to just copy paste parts of the html.
