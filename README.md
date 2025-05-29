![title](https://github.com/user-attachments/assets/dae32013-6d97-446e-ba5a-a24710de9630)

# The GPT-4 Ghostwriter

A python script for fully automatically creating web articles with images about any user specified topic. The script uses OpenAI's GPT-4 as a content creator. it will first send a request to create a table of contents in a specified xml format and it will then iterate over the table of content and request GPT-4 to write a specific chapter and its subsections. For some chapters it will use GPT-4 to create a prompt that describes an image related to the article. This prompt is then submitted to Dall-E-3 for image generation. The result is formatted in HTML and inserted into a user specified web page template. 

Content generation works in any Language known to GPT-4 but i only tried german and english. Example results can be found here: 

Article example:

* [The History of Space Exploration](https://beltoforion.de/de/gpt-ghostwriter/article_history_of_space_exploration/index.php)  (Created by Version 2.0.0 in the writing style of a Carl Sagan)

## Changes

Version 2.0.0 (2025-04-24):
* Code updated to use OpenAI client class
* Code updated to use GPT-4 and Dall-E-3
* Created three separate classes for TOC creation, image creation and article creation

Version 1.0.2 (2023-01-09):
* Added command line option to set writing style.
* fixed a bug that was messing up the created HTML

Version 1.0.1 (2022-12-31):
* Added placeholder for script version number
* OpenAI prompts modified
* added option for verbose mode
* improved output quality with a hardcoded filter that will remove the first paragraph of subsections. This paragraph contained repetetive explanations about the article topic. 

Version 1.0.0:
* initial release

## Usage

In order to use this script you must have an OpenAI API key that is exported in the environment variable OPENAP_API_KEY.
To execute the script type in the following command line:

```python
python ./ghostwriter.py -t "The Rise of AI generated Content" -tmpl ./template.html -o ai_content
```

The command will create a HTML article about the topic "The Rise of AI generated Content". It will build and send the necessary API queries to OpenAI's servers and compile a web page complete with a couple of images. 

 ## Command Line Options

<b>-t</b><br/> The topic to write about. Should be written in Quotation marks.
<br/><br/>
<b>-tmpl</b><br/> The template file used for output formatting. The layout of a template file is simple. It is a text file that needs to contain the two placeholders {TOPIC}, {CONTENT} and optionally {VERSION}. The {TOPIC} placeholder will be replaced with the article topic and the {CONTENT} placeholder will be replaced with the HTML formatted article. The {VERSION} placeholder will be replaced with the script version.
<br/><br/>
<b>-o</b><br/> The output folder. If the folder does not exist it will be created.
<br/><br/>
<b>-v</b><br/> Verbose mode. In this mode the prompts will be output to the console.
<br/><br/>
<b>-s</b><br/> Writing Style. Set the Writing style. i.e. "National Geographic", "Carl Sagan" or "Drunken Pirate"
<br/><br/>
 
