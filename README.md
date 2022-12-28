# openai-ghostwriter

A python script for fully automatically creating web articles with images. The scipt uses OpenAI's GPT-3 as a content creator. You need to have an API-Key in order to use the script.

## Usage

In order to use this script you must have an OpenAI API key that is exported in the environment variable OPENAP_API_KEY.
To execute the script just use python and type:

```python
python ./ghostwriter.py -t "The Rise of AI generated Content" -tmpl ./template.html -o ai_content
```

The command will create a HTML article about the topic "The Rise of AI generated Content". It will create and send the necessary API queries to OpenAI's servers and compile a web page complete with images. 

Example results can be found here: 

* [The Rise of AI generated Content](https://beltoforion.de/de/gpt3-ghostwriter/article_ai_content/index.php)
* [The entire History of Mars](https://beltoforion.de/de/gpt3-ghostwriter/article_history_of_mars/index.php)

Please note that each run will create a different article.

 ## Command Line Options

<b>-t</b><br/> The topic to write about. Should be written in Quotation marks.
<br/><br/>
<b>-tmpl</b><br/> The template file used for output formatting. The layout of a template file is simple. It is a text file that needs to contain the two placeholders {TOPIC} and {CONTENT}. The {TOPIC} placeholder will be replaced with the article topic and the {CONTENT} placeholder will be replaced with the HTML formatted article.
<br/><br/>
<b>-o</b><br/> The output folder. If the folder does not exist it will be created.
 
