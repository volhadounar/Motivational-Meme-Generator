# Motivational Meme Generator

## Overview of the project

"Motivational Meme Generator" – a multimedia application to dynamically generate memes.

This application can load quotes from a variety of filetypes (PDF, Word Documents, CSVs, Text files).
It can load images, manipulate, draw text onto images and save them.
The application accepts dynamic user input through a command-line tool and a web service. 

## Instructions of setting up and running the program

1. ``cd ...wherever...``
2. ``git clone https://github.com/volhadounar/Motivational-Meme-Generator.git``
3. ``cd Motivational-Meme-Generator``
4. ``pip install -r requirements.txt``  -- Should install everything you need
5. ``python3 app.py`` -- Running localy

Use as command-line tool to generate meme locally by:

``python3 meme.py -h``
```usage: meme.py [-h] [--path PATH] [--body BODY] [--author AUTHOR]

Generate meme with quote

options:
  -h, --help       show this help message and exit
  --path PATH      Provide the source image path
  --body BODY      Provide the text to be printed on the image
  --author AUTHOR  Provide the author of the quote
```

## Description of submodules and dependencies

Project contains Quote Engine and Meme Engine module.

The Quote Engine Module (.\QuoteEngine\ingestor.py) is responsible for ingesting many types of files that contain quotes.
Ingestor class realizes the IngestorInterface abstract base class and encapsulates all helper classes.
It implements logic to select the appropriate helper for a given file, based on filetype.
The following types are supported: .txt, .pdf, .docx, .csv 
A quote contains a body and an author: "This is a quote body" - Author

Module .\QuoteEngine\models.py implements IngestorInterface - abstract base class with two methods:
    ``` def can_ingest(cls, path: str) -> bool, 
        def parse(cls, path: str) -> List[QuoteModel]
    ```
This module implements stratagy objects that realize the IngestorInterface for each file type, so each stratagy object knows
how to parse the text and turn it into object QuoteModel.

Application uses subprocess to interface with CLI Tool Xpdf. It may not be installed on your local machine.
If this is the case, you can install it using the open source XpdfReader utility: https://www.xpdfreader.com/pdftotext-man.html

The Meme Engine Module (.\MemeEngine\meme_engine.py) is responsible for manipulating and drawing text onto images. 
It implements MemeEngine class that contains a method:
    ```def make_meme(self, img_path, text, author, width=500) -> str
    ```
This method is responsible for:
1. Loading an image using Pillow(PIL).
2. Resizing the image so that the width is at most 500px and the height is scaled proportionally.
3. Adding a quote body and the quote auther to the image.
