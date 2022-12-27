# openai-ghostwriter

A python script for fully automatically creating web articles with images about any topic by using OpenAI's GPT-3.

## Usage

In order to use this script you must have an OpenAI API key that is exported in the environment variable OPENAP_API_KEY.
To execute the script just use python and type:

```python
python ./ghostwriter.py -t "The Rise of AI generated Content" -tmpl ./template.php -o ai_content
```

This will automatically use OpenAI's GPT-3 to automatically generate a web page including images for each chapter about the topic: "The Rise of AI generated Content"

 ## Command Line Options

<b>-t</b><br/> The topic to write about
<br/><br/>
<b>-tmpl</b><br/> The template file used for output formatting
<br/><br/>
<b>-o</b><br/> The output folder.
 
