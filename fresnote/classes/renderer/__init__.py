from pathlib import Path
import re
from typing import List, Tuple, Dict

class Markdown:

    def render_markdown_bold_text_markups(self, text: str) -> str:
        """Converts markdown bold markups to html bold markups."""
        if "**" in text and text.count("**") % 2 == 0:
            probe = '\*\*(.*?)\*\*'
            boldTexts = re.findall(probe, text)

            for boldText in boldTexts:
                renderedText = f"<b>{boldText}</b>"
                text = text.replace(f'**{boldText}**', renderedText)
        return text

    def render_markdown_italics_text_markups(self, text: str) -> str:
        """Converts markdown italics markups to html italics markups."""
        if "__" in text and text.count("__") % 2 == 0:
            probe = '__(.*?)__'
            italicsTexts = re.findall(probe, text)

            for italicsText in italicsTexts:
                renderedText = f"<i>{italicsText}</i>"
                text = text.replace(f'__{italicsText}__', renderedText)
        return text

    def render_markdown_headers_markups(self, text: str) -> str:
        """Converts markdown header markups to html header markups."""
        if text.startswith("# "):
            text = "<h1>{}</h1>".format(text.split("# ", 1)[-1])
        elif text.startswith("## "):
            text = "<h2>{}</h2>".format(text.split("## ", 1)[-1])
        elif text.startswith("### "):
            text = "<h3>{}</h3>".format(text.split("### ", 1)[-1])
        elif text.startswith("#### "):
            text = "<h4>{}</h4>".format(text.split("#### ", 1)[-1])
        return text

    def render_markdown_ruler_markups(self, text: str) -> str:
        """Converts markdown ruler markups to html ruler tags."""
        if text.startswith('---'):
            text = "<hr>"
        return text


class Latex:

    def render_latex_red_text_markups(self, text: str) -> str:
        """Converts latex style red text to html text style tag."""
        if "\\red{" in text:
            probe = '\\\\red{(.*?)}'
            redTexts = re.findall(probe, text)

            for redText in redTexts:
                renderedText = f'<span style="color:#FF0000";>{redText}</span>'
                text = text.replace(f'\\red{{{redText}}}', renderedText)
        return text

    def render_latex_green_text_markups(self, text: str) -> str:
        """Converts latex style green text to html text style tag."""
        if "\\green{" in text:
            probe = '\\\\green{(.*?)}'
            greenTexts = re.findall(probe, text)

            for greenText in greenTexts:
                renderedText = f'<span style="color:#2EBF28";>{greenText}</span>'
                text = text.replace(f'\\green{{{greenText}}}', renderedText)
        return text

    def render_latex_link_markups(self, text: str) -> str:
        """Convert latex style link to html style <a> tag."""
        if "\\link{" in text:
            probe = '\\\\link{(.*?)}'
            links = re.findall(probe, text)
            for link in links:
                if ',' in link:
                    referenceText, url = link.split(',', 1)
                    referenceText = referenceText.strip()
                    url = url.strip()
                    if url.startswith('/'):
                        filename = Path(url).name
                        extension = Path(url).suffix
                        if extension in self.icons:
                            renderedText = '<a href="{}"><img id="todoIcon" src="/static/icons/{}" alt="drawing" width="20"/> {}</a>'.format(url, self.icons[extension], referenceText)
                        else:
                            renderedText = '<a href="{}">{}</a>'.format(url, referenceText)
                    else:
                        renderedText = '<a href="{}">{}</a>'.format(url, referenceText)
                else:
                    if link.startswith('/'):
                        filename = Path(link).name
                        extension = Path(link).suffix
                        if extension in self.icons:
                            renderedText = '<a href="{}"><img id="todoIcon" src="/static/icons/{}" alt="drawing" width="20"/> {}</a>'.format(link, self.icons[extension], filename)
                        else:
                            renderedText = '<a href="{}">{}</a>'.format(link, filename)
                    else:
                        renderedText = '<a href="{}">{}</a>'.format(link, link)
                text = text.replace(f'\\link{{{link}}}', renderedText)
        return text



class Renderer(Markdown, Latex):

    def __init__(self):
        self.ID = ''
        self.line = ''
        self.renderedLines = []
        self.sectionID = ''
        self.flags= {'order':[], 
                     'counts': {'fold': 0},
                     'errors': []
                    }

        """
        NOTES:
            A markup that extends multiple lines has start and end.
            Then, text is rendered within the start and end markups.
            Based on the markup, the text within the start and end points is rendered differently.
        """

        # Define start html for markups
        self.renderStart_markup = {
                'code': '<pre>',
                'fold': '<a class="btn btn-outline-light text-white col-12" data-toggle="collapse" href="#subsection_fold_{count}_{ID}" role="button" aria-expanded="false" aria-controls="subsection_fold_{count}_{ID}">'\
                        '{title}'\
                        '</a>'\
                        '<div class="row">'\
                        '<div class="col-12">'\
                        '<div class="collapse" id="subsection_fold_{count}_{ID}">'\
                        '<br>',
                'img': '<div class="container-fluid">'
        }

        # Define end html for markups
        self.renderEnd_markup = {
                'code': '</pre>',
                'fold': '</div></div></div><br>',
                'img' : '</div>'
        }

        self.icons = {
                '.pdf' : 'file-pdf-regular.svg',
                '.docx': 'file-alt-regular.svg',
                '.doc' : 'file-alt-regular.svg',
                '.xls' : 'file-alt-regular.svg',
                '.xlsx': 'file-alt-regular.svg',
                '.csv' : 'file-csv-solid.svg',
                '.txt' : 'file-alt-regular.svg',
                '.tex' : 'file-alt-regular.svg',
                '.bib' : 'file-alt-regular.svg',
                '.tsv' : 'file-csv-solid.svg'
        }

    def initialize_renderer(self):
        self.ID = ''
        self.line = ''
        self.renderedLines = []
        self.sectionID = ''
        self.flags= {'order':[], 
                     'counts': {'fold': 0},
                     'errors': []
                    }


    def is_last_flag(self, flag: str) -> bool:
        if self.flags['order'] and self.flags['order'][-1] == flag:
            return True
        else:
            return False


    def renderLine(self) -> None: 
        if self.line.startswith('```'):
            flag = 'code'
        elif self.line.startswith('\\img{'):
            flag = 'img'
        elif self.line.startswith('\\fold{'):
            flag = 'fold'
        elif self.line.lstrip().startswith('}'):
            flag = 'end'
        else:
            flag = ''


        if flag == "code":
            if self.is_last_flag("code"):
                self.flags['order'].pop()
                self.renderedLines.append(self.renderEnd_markup[flag])
            else:
                self.flags['order'].append(flag)
                self.renderedLines.append(self.renderStart_markup[flag])
        elif flag == "fold":
                self.flags['order'].append(flag)
                title = self.line.replace("\\fold{", "")
                self.flags['counts']['fold'] += 1
                args = {"ID":self.ID, "count":self.flags['counts']['fold'], "title":title}
                self.renderedLines.append(self.renderStart_markup['fold'].format(**args))
        elif flag == "img":
                self.flags['order'].append(flag)
                self.renderedLines.append(self.renderStart_markup[flag])
        elif flag == "end":
            if self.is_last_flag('code'):
                self.renderedLines.append(self.line)
            elif not self.flags["order"]:
                self.flags['errors'].append("End markup.")
                line = self.line+'<span style="color:#FF0000";>Extra ending markup found'
                self.renderedLines.append(line)
            else:
                lastFlag = self.flags['order'].pop() 
                self.renderedLines.append(self.renderEnd_markup[lastFlag])
        else:
            if self.is_last_flag("code"):
                self.renderedLines.append(self.line)
            elif self.line.strip().strip("\n"):
                if self.is_last_flag('img'):
                    try:
                        fields = self.line.split(",")
                        if len(fields) == 2:
                            caption, url = fields
                            width, height = '200', '100'
                            caption = caption.strip()
                            url     = url.strip()
                        else:
                            caption, url, width, height = fields
                            caption = caption.strip()
                            url     = url.strip()
                            width   = width.strip()
                            height  = height.strip()
                    except Exception:
                        self.flags['errors'].append('img')
                        line = '<span style="color:#FF0000";>Image should have caption, url, width, height<br>'+self.line
                    else:
                        line = '<a class="btn btn-secondary mt-2 ml-2" href="{url}" role="button">'\
                               '{caption}<br>'\
                               '<img src="{url}" width="{width}" height="{height}">'\
                               '</a>'.format(caption=caption, url=url, width=width, height=height)
                    finally:
                        self.renderedLines.append(line)
                else:
                    self.line = self.line.strip("\n")
                    self.line = self.render_markdown_headers_markups(self.line)
                    self.line = self.render_markdown_bold_text_markups(self.line)
                    self.line = self.render_markdown_italics_text_markups(self.line)
                    self.line = self.render_markdown_ruler_markups(self.line)
                    self.line = self.render_latex_green_text_markups(self.line)
                    self.line = self.render_latex_red_text_markups(self.line)
                    self.line = self.render_latex_link_markups(self.line)
                    self.line = "<p>"+self.line+"</p>"
                    self.renderedLines.append(self.line)


    def convert_db_results_into_sections(self, 
                                         notebook: str, 
                                         chapter: str, 
                                         sectionsResults: List,
                                         sectionsIDs: List,
                                         db: str) -> List[Dict]:
        """Converts results returned from the project database to a list of dictionaries. Each dictionary corresponds to a section with various markups being converted to html markups."""

        def create_tags_list(tags: str) -> List:
            if ',' in tags:
                tags = [x.strip(' ') for x in tags.split(',')]
            else:
                tags = [tags.strip(' ')]
            return tags

        def convert_section_fields_to_dictionary(notebook: str, chapter: str, dbres: Tuple) -> Dict:
            ID, section, tags, content, folded, creationDate = dbres
            sectionDict = {
                    "ID"      : ID,
                    "notebook": notebook,
                    "chapter" : chapter,
                    "section" : section,
                    "tags"    : tags,
                    "content" : content,
                    "folded"  : folded,
                    "date"    : creationDate
                    }
            return sectionDict

        # tmp is temporary so that sections are added later based on order.
        tmp = dict()
        for dbres in sectionsResults:
            sectionDict = convert_section_fields_to_dictionary(notebook, chapter, dbres)
            sectionDict['tags'] = create_tags_list(sectionDict['tags'])
            """
            NOTES:
                In the following steps the content of the section is broken down in lines based on newlines.
                In each line, the markups are converted to html.

                The splitlines(keepends=True) converts a string like:
                    'This is line 1\n\nThis is line2'
                to:
                    ['This is line 1\n', '\n', 'This is line2']
            """
            self.ID = sectionDict['ID']
            if '\n' in sectionDict['content']:
                contentLines = sectionDict['content'].splitlines(keepends=True)
                for line in contentLines:
                    self.line = line
                    self.renderLine()
            else:
                self.line = sectionDict['content']
                self.renderLine()

            htmlRendering = ''.join(self.renderedLines)
            # Produce error if markups are left in flags or close markups were not found.
            if self.flags['order'] or self.flags['errors']:
                errorText = '<span style="color:#FF0000";>Errors {} while rendering section. Check {} markups.</span><br>'.format(self.flags['errors'], self.flags['order'])
                sectionDict['content'] = errorText + htmlRendering
            else:
                sectionDict['content'] = htmlRendering
            tmp[sectionDict['ID']] = sectionDict
            self.initialize_renderer()

        sections = list()
        for sID in sectionsIDs:
            sections.append(tmp[sID])
        return sections


