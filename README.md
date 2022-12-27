# openai-ghostwriter

A python script for fully automatically creating web articles with images about any topic by using OpenAI's GPT-3.

## Requirements

In order to use this script you must have an OpenAI API key that is exported in the environment variable OPENAP_API_KEY
 
 
## Usage

You need python to execute this script. Put your images into a folder and then run the script on the content of this folder.

```python
python ./ghostwriter.py -t "The Rise of AI generated Content" -tmpl ./template.php -o ai_content
```

 ## Command Line Options

<b>-t</b><br/> The topic to write about
<br/><br/>
<b>-tmpl</b><br/> The template file used for output formatting
<br/><br/>
<b>-o</b><br/> The output folder.
 
