import requests
import os
import openai
import pathlib
import codecs
import lxml.etree
import argparse

from PIL import Image
from io import BytesIO
#from pathlib import Path


class OpenAIGhostWriter:
    def __init__(self, output_folder : pathlib.Path, template_file : pathlib.Path, verbose : bool):
        self.__api_key = os.environ["OPENAI_API_KEY"]
        self.__model = "text-davinci-003" # biggest, best and most expensive
        self.__output_folder = output_folder
        self.__template_file = template_file
        self.__verbose = verbose
        self.__version = "1.0.1"

        openai.api_key = self.__api_key


    def __create(self, prompt, temp = 0.3, freq_penalty = 0.3, pres_penalty = 0.2, max_tokens = 4000, model = None):
        response = openai.Completion.create(
            model = self.__model if model is None else model,
            prompt = prompt,
            temperature = temp,
            max_tokens = max_tokens,
            top_p = 1.0,
            frequency_penalty = freq_penalty,
            presence_penalty = pres_penalty
        )

        if self.__verbose:
            print(f'{prompt}')

        result = response["choices"][0]["text"]
        result = result.strip()
        return result


    def write_introduction(self, topic, chapter, subsection, nwords=100):
        if chapter is None:
            prompt = f'{topic}; Introductory text with at least {nwords} words; [Format:HTML;No heading;multiple <p> sections]'
        elif subsection is None:
            prompt = f'Topic: {chapter} / {topic}; Introductory; {nwords} Words; [Format:HTML;No heading;multiple <p> sections]'
        else:
#            prompt = f'Topic: {subsection} / {chapter} / {topic}; Write essay; minimum {nwords} words; Format as html multiple <p> sections but no heading'
#            prompt = f'Topic: {subsection} / {chapter} / {topic}; Write chapter; minimum {nwords} words; Format as html multiple <p> sections but no heading'
            prompt = f'[Caption: {topic}][Topic: "{chapter}:{subsection}"][Format:HTML;No heading;multiple <p> sections]Write chapter; minimum 600 words'
            
        return self.__create(prompt, temp=0.3, freq_penalty=0.4, pres_penalty=0.3, max_tokens = 4000)


    def create_toc(self, topic, nchapter):
        if self.__verbose:
            print(f'Creating table of contents for "{topic}"')

        prompt  = f'Create table of contents for an article titled "{topic}" with at least {nchapter} chapters; Captions must be unnumbered; Output in XML with the XSD scheme listed below; Caption attribute must consist of at least two words\r\n'
        prompt += '<?xml version="1.0" encoding="utf-8"?>\n'
        prompt += '<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">\n'
        prompt += '  <xs:element name="outline">\n'
        prompt += '    <xs:complexType>\n'
        prompt += '      <xs:sequence>\n'
        prompt += '        <xs:element name="topic" type="xs:string" />\n'
        prompt += '        <xs:element maxOccurs="unbounded" name="subtopic">\n'
        prompt += '          <xs:complexType>\n'
        prompt += '            <xs:sequence>\n'
        prompt += '              <xs:element maxOccurs="unbounded" name="subsubtopic">\n'
        prompt += '                <xs:complexType>\n'
        prompt += '                  <xs:attribute name="Caption" type="xs:string" use="required" />\n'
        prompt += '                </xs:complexType>\n'
        prompt += '              </xs:element>\n'
        prompt += '            </xs:sequence>\n'
        prompt += '            <xs:attribute name="Caption" type="xs:string" use="required" />\n'
        prompt += '          </xs:complexType>\n'
        prompt += '        </xs:element>\n'
        prompt += '      </xs:sequence>\n'
        prompt += '    </xs:complexType>\n'
        prompt += '  </xs:element>\n'
        prompt += '</xs:schema>\n'

        # Use text-davinci-003 because the prompt is too complex for smaller models.
        self.__toc_xml = self.__create(prompt, model="text-davinci-003", max_tokens = 1024)
        self.__toc_xml = self.__toc_xml.strip()
        return self.__toc_xml
       

    def write(self, topic, nchapter):
        toc = self.create_toc(topic, nchapter)
        codecs.open(f'{str(self.__output_folder)}/toc.xml', 'w', 'utf-8-sig').write(toc)

        article = self.create_article_from_toc(f'{str(self.__output_folder)}/toc.xml')

        with codecs.open(self.__template_file, 'r', 'utf-8-sig') as f:
            template = f.read()

        template = template.replace('{TOPIC}', topic)
        template = template.replace('{CONTENT}', article)
        template = template.replace('{VERSION}', self.__version)

        output_file = self.__output_folder / self.__template_file.with_name('index').with_suffix(self.__template_file.suffix)
        codecs.open(output_file, 'w', 'utf-8-sig').write(template)


    def __remove_first_paragraph(self, html):
        ''' The first paragraph often contains an explanation of the topic. It needs to be removed. '''
        paragraphs = html.split('<p>')
        html = '</p>'.join(paragraphs[2:])
        return html


    def create_article_from_toc(self, toc_file):
        tree = lxml.etree.parse(toc_file)
        root = tree.getroot()

        article_code = ""

        # Iterate over the child elements of the root element
        for element in root:
            # Create an introdution for the Article
            if element.tag=="topic":
                topic = element.text
                article_code += f'\r\n<section>'
                article_code += f'\r\n<h1>{topic}</h1>'

                imagefile = f'{str(self.__output_folder)}/{topic}.jpg'
                self.create_image(topic, None, imagefile)
                article_code += f'<span class="image right">\r\n'
                article_code += f'  <img src="{topic}.jpg"></img>\r\n'
                article_code += f'</span>\r\n'

                intro = self.write_introduction(topic, chapter = None, subsection = None, nwords=300)
                article_code += intro
                article_code += f'\r\n</section>'

            elif element.tag=="subtopic":
                chapter = element.attrib['Caption']
                article_code += f'\r\n<section>'
                article_code += f'\r\n<h2>{chapter}</h2>'
                
                imagefile = f'{str(self.__output_folder)}/{topic}-{chapter}.jpg'
                self.create_image(topic, chapter, imagefile)
                article_code += f'<span class="image right">\r\n'
                article_code += f'  <img src="{topic}-{chapter}.jpg"></img>'
                article_code += f'</span>\r\n'

                # Create an introdution for the chapter
                chapter_text = self.write_introduction(topic, chapter, subsection = None, nwords=100)
                chapter_text = self.__remove_first_paragraph(chapter_text)

                article_code += chapter_text

                for subelement in element:
                    subsection = subelement.attrib['Caption']
                    article_code += f'\r\n<h3>{subsection}</h3>'

                    subsection_text = self.write_introduction(topic, chapter, subsection, nwords=600)
                    subsection_text = self.__remove_first_paragraph(subsection_text)

                    article_code += subsection_text
                
                article_code += f'\r\n</section>'

        return article_code

    def create_image(self, topic, chapter, save_path):
#        prompt = f'Create an DALL-E prompt in english that will create a photorealistic illustration for an article with this title:'
        prompt = f'Create an DALL-E prompt in english for creating a photorealistic illustration for an article with this title:'
        if chapter is None:        
            prompt += f'{topic}'
        else:
            prompt += f'{topic} - {chapter}'

        prompt_dalle = self.__create(prompt)
        prompt_dalle = prompt_dalle.replace('"', '')
        prompt_dalle = prompt_dalle.strip()
        self.create_image_from_prompt(prompt_dalle, save_path)


    def create_image_from_prompt(self, prompt, save_path=None):
        if self.__verbose:
            print(f'{prompt}')

        response = openai.Image.create(
            prompt=prompt,
            n=1,
            #size="1024x1024"
            size="512x512"
        )
        image_url = response['data'][0]['url']
        response = requests.get(image_url)

        image = Image.open(BytesIO(response.content))

        if save_path:
            image.save(save_path)


def main():
    parser = argparse.ArgumentParser(description='OpenAI Ghostwriter - Automatically create a web page on every topic')
    parser.add_argument("-t", "--Topic", dest="topic", help='The topic to write about', required=True, type=str)
    parser.add_argument("-tmpl", "--Template", dest="template", help='A template with a file where the created HTML fragment shall be inserted', required=True, type=str)    
    parser.add_argument("-o", dest="output", help='Name of output folder', required=True, type=str, default=None)
    parser.add_argument("-v", dest="verbose", action='store_true', help='Output prompts', required=False)    
    args = parser.parse_args()

    print('\r\n')
    print('OpenAI Ghostwriter')
    print('----------------------------------')
    print(f' - topic: {args.topic}')
    print(f' - template: {args.template}')    
    print(f' - output folder: {args.output}')    
    print(f' - verbose: {args.verbose}')    

    topic = args.topic.replace('"', '').strip()
    template_file = pathlib.Path(args.template)
    if not template_file.is_file():
        print(f'The template file {args.template} does not exists!')
        exit(-1)

    output_folder = pathlib.Path(args.output) 
    if not output_folder.exists():
        os.mkdir(str(output_folder))
    elif not output_folder.is_dir():
        print(f'The output folder {args.output} already exists and is not a directory!')
        exit(-1)

    controller = OpenAIGhostWriter(output_folder, template_file, args.verbose)
    controller.write(topic, 3)

if __name__ == "__main__":
    main()