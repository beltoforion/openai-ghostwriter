import requests
import os
from openai import OpenAI
import pathlib
import codecs
import lxml.etree
import argparse
import re

from colorama import init, Fore, Style
from PIL import Image
from io import BytesIO

from abc import ABC


class OpenAiGeneratorBase(ABC):
    def __init__(self, client : OpenAI, role : str, output_folder : pathlib.Path, verbose: bool) -> None:
        self.__client = client
        self.__verbose = verbose
        self.__role = role
        self.__output_folder = output_folder
        self.__model = "gpt-4-turbo"
        self.__version = "2.0.0"

        if not output_folder.exists():
            os.mkdir(str(output_folder))
        elif not output_folder.is_dir():
            raise Exception(f'The output folder {output_folder} already exists and is not a directory!')

    @property
    def version(self) -> str:
        return self.__version
    
    @property
    def output_folder(self) -> pathlib.Path:
        return self.__output_folder
    
    @property
    def client(self) -> OpenAI:
        return self.__client
    
    @property
    def model(self) -> str:
        return self.__model 
    
    @property
    def verbose(self) -> bool:
        return self.__verbose
    
    @property
    def role(self) -> str:
        return self.__role

    
    def query(self, prompt, temp=0.3, freq_penalty=0.3, pres_penalty=0.2, max_tokens=4000, model=None) -> str:
        if self.role is None or self.role == "":
            raise ValueError("Role is not set. Please provide a valid role.")

        if self.__verbose:
            print(Fore.RESET + '\nOutgoing:')
            print(Fore.GREEN + f'{prompt}')

        response = self.client.chat.completions.create(
            model=model or self.__model,
            messages=[
                {"role": "system", "content": self.role},
                {"role": "user", "content": prompt}
            ],
            temperature=temp,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=freq_penalty,
            presence_penalty=pres_penalty
        )

        result : str | None = response.choices[0].message.content
        if result is None:
            raise ValueError("No response from OpenAI API.")

        if self.__verbose:
            print(Style.RESET_ALL +'\nIncoming:')
            print(Fore.CYAN + f'{result}')

        return result.strip()


class OpenAiTocGenerator(OpenAiGeneratorBase):
    def __init__(self, client : OpenAI, output_folder: pathlib.Path, verbose: bool):
        role : str = ('You are a assistant that writes scientific structured HTML articles. '
                      'Your writing style is entertaining but scientific. '
                      'Part of your job is to create article outlines in XML format. You do not interact directly with a human. '
                      'Your output will be processed by software. You must adhere to all formatting instructions or your output will break the toolchain.') 

        OpenAiGeneratorBase.__init__(self, client, role, output_folder, verbose)


    def create_toc(self, topic : str, nchapter : int) :
        prompt = (f'Create a well-structured XML table of contents for an article titled "{topic}".\n'
                f'- Include a maximum of 3 to {nchapter} main chapters.\n'
                '- Each chapter must have 2 to 4 sub-subsection. Make sure to not always use the same number of subsections.\n'
                '- Use the provided XSD schema exactly.\n'
                '- Each "Caption" must consist of two or more words.\n'
                '- You are not allowed to add any non xml text either before or after the XML as this will break the toolchain.\n'
                '\n<?xml version="1.0" encoding="utf-8"?>\n'
                '<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">\n'
                '  <xs:element name="outline">\n'
                '    <xs:complexType>\n'
                '      <xs:sequence>\n'
                '        <xs:element name="topic" type="xs:string" />\n'
                '        <xs:element maxOccurs="unbounded" name="subtopic">\n'
                '          <xs:complexType>\n'
                '            <xs:sequence>\n'
                '              <xs:element maxOccurs="unbounded" name="subsubtopic">\n'
                '                <xs:complexType>\n'
                '                  <xs:attribute name="Caption" type="xs:string" use="required" />\n'
                '                </xs:complexType>\n'
                '              </xs:element>\n'
                '            </xs:sequence>\n'
                '            <xs:attribute name="Caption" type="xs:string" use="required" />\n'
                '          </xs:complexType>\n'
                '        </xs:element>\n'
                '      </xs:sequence>\n'
                '    </xs:complexType>\n'
                '  </xs:element>\n'
                '</xs:schema>')
        
        toc : str = self.query(prompt)
        toc_file = f'{str(self.output_folder)}/toc.xml'
        codecs.open(f'{toc_file}', 'w', 'utf-8-sig').write(toc)

        tree = lxml.etree.parse(toc_file)
        if tree is None:
            raise ValueError(f"Failed to parse the XML file: {toc_file}")
        
        return tree


class OpenAiImageGenerator(OpenAiGeneratorBase):
    def __init__(self, client : OpenAI, output_folder: pathlib.Path, verbose: bool):
        role: str = (
            'You are a skilled writer working mainly on the creation of entertaining and educational web page articles. '
            'Your writing style is entertaining but scientific. You write clear, engaging, and accurate articles for a general audience. '
            'Use analogies, vivid examples, and simple language to explain complex ideas. No clickbait, no hype, no over-simplifying. Just good science, well told. '
            'For each article, you also generate one or more image prompts to be used with an AI image generator. These prompts should clearly describe the scene, '
            'focus on visual clarity and relevance to the topic, and avoid abstract or overly artistic styles unless specifically required.'
        )

        OpenAiGeneratorBase.__init__(self, client, role, output_folder, verbose)


    def create_image(self, topic, chapter, save_path):
        prompt = (
            f'Write a concise, visual description for a photorealistic illustration for an article section titled: "{topic}"{f" - {chapter}" if chapter else ""}.'
            'Keep it under 600 characters. Describe a simple specific scene with lighting, composition, and mood. Do not include HTML or quotes.'
        )
    
        image_query_prompt = self.query(prompt).strip()
        if not image_query_prompt.strip() or len(image_query_prompt) > 1000:
            print(Fore.RED +  "⚠️ Skipping image: prompt is empty or too long.")
            return

        response = self.client.images.generate(
            prompt=image_query_prompt,
            n=1,
            model="dall-e-3",
            size="1024x1024",  # DALL·E 3 typically uses 1024x1024
            response_format="url"
        )

        image_url : str | None = response.data[0].url
        if image_url is None:
            raise ValueError("No image URL returned from OpenAI API.")
        
        try:
            r = requests.get(image_url, timeout=10)
            r.raise_for_status()
            image = Image.open(BytesIO(r.content))
        except Exception as e:
            print(Fore.RED + f"⚠️ Failed to download or open image: {e}")
            return
        
        if save_path:
            image.save(save_path)


    def create_article_images_toc(self, toc_tree):
        if toc_tree is None:
            raise ValueError("Table of contents is None. Cannot create article.")
        
        root = toc_tree.getroot()
        if root is None:
            raise ValueError("Root element is None. Cannot create article.")
        
        for element in root:
            if element.tag == "topic":
                topic = element.text
                imagefile = f'{str(self.output_folder)}/{topic}.jpg'
                self.create_image(topic, None, imagefile)

            elif element.tag == "subtopic":
#                chapter = element.attrib['Caption']
#                imagefile = f'{str(self.output_folder)}/{topic}-{chapter}.jpg'
#                self.create_image(topic, chapter, imagefile)

                for subelement in element:
                    subsection = subelement.attrib['Caption']
                    imagefile = f'{str(self.output_folder)}/{topic}-{subsection}.jpg'
                    self.create_image(topic, subsection, imagefile)


class OpenAiArticleGenerator(OpenAiGeneratorBase):
    def __init__(self, client : OpenAI, output_folder: pathlib.Path, template_file: pathlib.Path, style : str, verbose: bool):
        if style is None:
            role: str = (
                'You are a skilled writer working mainly on the creation of entertaining and educational web page articles. '
                'Your writing style is entertaining but scientific. You write clear, engaging, and accurate articles for a general audience. '
                'Use analogies, vivid examples, and simple language to explain complex ideas. No clickbait, no hype, no over-simplifying. Just good science, well told. '
            )
        else:
            role: str = (
                'You are a skilled writer working mainly on the creation of entertaining and educational web page articles. '
                f'Your writing style is similar to the style of {style}. '
                'You write clear, engaging, and accurate articles for a general audience. '
                'Use analogies, vivid examples, and simple language to explain complex ideas. No clickbait, no hype, no over-simplifying. Just good science, well told. '
            )
    
        self.__template_file = template_file
        if not template_file.is_file():
            raise ValueError(f'The template file {template_file} does not exist!')
        
        OpenAiGeneratorBase.__init__(self, client, role, output_folder, verbose)


    def __write_introduction(self, topic, chapter, subsection, nwords=100):
        if chapter is None:
            prompt = f'{topic}; Introductory text with at least {nwords} words; [Format:HTML;No heading;use <p> tags]'
        elif subsection is None:
            prompt = f'Topic: {chapter} / {topic}; Introductory; {nwords} Words; [Format:HTML;No heading;use <p> tags]'
        else:
            prompt = f'[Caption: {topic}][Topic: "{chapter}:{subsection}"][Format:HTML;No heading;use <p> tags][Write: min. {nwords} words]'

        return self.query(prompt, temp=0.3, freq_penalty=0.5, pres_penalty=0.5, max_tokens=4000)


    def __remove_first_paragraph(self, html):
        paragraphs = html.split('</p>')
        fixed_html = '</p>'.join(paragraphs[1:]).strip()
        return html if not fixed_html else fixed_html


    def __create_article_from_toc(self, toc_tree):
        if toc_tree is None:
            raise ValueError("Table of contents is None. Cannot create article.")
        
        root = toc_tree.getroot()
        if root is None:
            raise ValueError("Root element is None. Cannot create article.")
        
        article_code = ""
        for element in root:
            if element.tag == "topic":
                topic = element.text
                article_code += f'\r\n<section><h1>{topic}</h1>'
                article_code += f'<span class="image right">\r\n  <img src="{topic}.jpg"></img>\r\n</span>'
                intro = self.__write_introduction(topic, None, None, 300)
                article_code += intro + '\r\n</section>'

            elif element.tag == "subtopic":
                chapter = element.attrib['Caption']
                article_code += f'\r\n<section><h2>{chapter}</h2>'
#                article_code += f'<span class="image right">\r\n  <img src="{topic}-{chapter}.jpg"></img>\r\n</span>'
                chapter_text = self.__write_introduction(topic, chapter, None, 100)
                article_code += self.__remove_first_paragraph(chapter_text)

                for subelement in element:
                    subsection = subelement.attrib['Caption']
                    article_code += f'\r\n<h3>{subsection}</h3>'
                    article_code += f'<span class="image right">\r\n  <img src="{topic}-{subsection}.jpg"></img>\r\n</span>'
                    subsection_text = self.__write_introduction(topic, chapter, subsection, 600)
                    article_code += self.__remove_first_paragraph(subsection_text)

                article_code += '\r\n</section>'

        return article_code


    def write(self, topic : str, toc_tree):
        with codecs.open(self.__template_file, 'r', 'utf-8-sig') as f:
            template = f.read()

        output_file : str = self.output_folder / self.__template_file.with_name('index').with_suffix(self.__template_file.suffix)

        # Create article html code
        article = self.__create_article_from_toc(toc_tree)

        # Set article meta information
        template = template.replace('{TOPIC}', topic)
        template = template.replace('{MODEL}', self.model)
        template = template.replace('{CONTENT}', article)
        template = template.replace('{VERSION}', self.version)

        # Write the output file
        codecs.open(output_file, 'w', 'utf-8-sig').write(template)


def main():
    parser = argparse.ArgumentParser(description='OpenAI Ghostwriter - Automatically create a web page on every topic')
    parser.add_argument("-t", "--Topic", dest="topic", required=True, type=str)
    parser.add_argument("-tmpl", "--Template", dest="template", required=True, type=str)
    parser.add_argument("-o", dest="output", required=True, type=str)
    parser.add_argument("-v", dest="verbose", action='store_true')
    parser.add_argument("-s", dest="style", required=False)
    args = parser.parse_args()

    print('\r\nOpenAI Ghostwriter\n----------------------------------')
    print(f' - topic: {args.topic}')
    print(f' - template: {args.template}')
    print(f' - writing style: {args.style}')
    print(f' - output folder: {args.output}')
    print(f' - verbose: {args.verbose}')

    topic = args.topic.replace('"', '').strip()
    template_file = pathlib.Path(args.template)
    if not template_file.is_file():
        print(f'The template file {args.template} does not exist!')
        exit(-1)

    output_folder = pathlib.Path(args.output)

    # Create the open AI client
    client : OpenAI = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    #
    # Step 1: Create the table of contents as an xml file
    #

    toc_generator = OpenAiTocGenerator(client, output_folder, args.verbose)
    toc = toc_generator.create_toc(topic, 5)

#    toc = lxml.etree.parse(f'{str(output_folder)}/toc.xml')

    #
    # Step 2: Create the article from the table of contents
    #

    image_generator = OpenAiImageGenerator(client, output_folder, args.verbose)
    image_generator.create_article_images_toc(toc)

    #
    # Step 3: Create the images
    #

    article_generator = OpenAiArticleGenerator(client, output_folder, template_file, args.style, args.verbose)
    article_generator.write(topic, toc)


if __name__ == "__main__":
    main()
