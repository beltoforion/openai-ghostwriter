# openai-ghostwriter

A python script for fully automatically creating web articles with images about any topic by using OpenAI's GPT-3. 

## Usage

In order to use this script you must have an OpenAI API key that is exported in the environment variable OPENAP_API_KEY.
To execute the script just use python and type:

```python
python ./ghostwriter.py -t "The Rise of AI generated Content" -tmpl ./template.php -o ai_content
```

This will automatically use OpenAI's GPT-3 to automatically generate a web page including images for each chapter about the topic: "The Rise of AI generated Content"

Example results can be found here:

* [The Rise of AI generated Content](https://beltoforion.de/de/ai-ghostwriter/article_ai_content/index.php)
* [The entire History of Mars](https://beltoforion.de/de/ai-ghostwriter/article_history_of_mars/index.php)

Please note that each run will create a different article.

 ## Command Line Options

<b>-t</b><br/> The topic to write about. Should be written in Quotation marks.
<br/><br/>
<b>-tmpl</b><br/> The template file used for output formatting. The layout of a template file is simple. It is a text file that needs to contain the two placeholders {TOPIC} and {CONTENT}. The {TOPIC} placeholder will be replaced with the article topic and the {CONTENT} placeholder will be replaced with the HTML formatted article.
<br/><br/>
<b>-o</b><br/> The output folder. If the folder does not exist it will be created.
 
