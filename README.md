![titel_ghostwriter](https://user-images.githubusercontent.com/2202567/210897677-50993627-cd0d-4dbf-8ed8-d90d330ae7b7.jpg)
# openai-ghostwriter

A python script for fully automatically creating web articles with images about any user specified topic. The script uses OpenAI's GPT-3 as a content creator. it will first send a request to create a table of contents in a specified xml format and it will then iterate over the table of content and request GPT-3 to write a specific chapter and its subsections. For some chapters it will ask GPT-3 to create a prompt that describes an image related to the article. This prompt is then used to generate illustrations with GPT-3. The result is formatted in HTML and inserted into a user specified web page template. 

Content generation works in any Language known to GPT-3 but i only tried german and english.Example results can be found here: 

Article examples in english:

* [The Age of Piracy](https://beltoforion.de/de/gpt3-ghostwriter/article_article_age_of_piracy/index.php)  (Created by Version 1.0.2 in the writing style of a drunken pirate)
* [The Cambrian Explosion](https://beltoforion.de/de/gpt3-ghostwriter/article_cambrian_explosion/index.php)  (Created by Version 1.0.1)
* [Paleocene–Eocene Thermal Maximum](https://beltoforion.de/de/gpt3-ghostwriter/article_petm/index.php)  (Created by Version 1.0.1)
* [The Late Bronze Age Collapse](https://beltoforion.de/de/gpt3-ghostwriter/article_late_bronze_age_collapse/index.php)  (Created by Version 1.0.1)

Article examples in german:
* [Die Kambrische Explosion](https://beltoforion.de/de/gpt3-ghostwriter/article_kambrische_explosion/index.php) (Created by Version 1.0.1)
* [Der Niedergang des römischen Reiches](https://beltoforion.de/de/gpt3-ghostwriter/article_rom/index.php) (Created by Version 1.0.0)

Please note that each run will create a different article. 

## Changes

Version 1.0.2 (2023-01-09):
* Added command line option to set writing style.

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
<b>-v</b><br/> Verbose mode. In this mode the prompts will be output to the console.
<b>-s</b><br/> Writing Style. Set the Writing style. i.e. "National Geographic", "Carl Sagan" or "Drunken Pirate"
 
