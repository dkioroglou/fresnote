import configparser
from pathlib import Path
import re
from typing import List, Tuple, Dict
import fresnote.classes

class InlineRenderers:

    def __init__(self, configName):
        self.configName = configName
        self.icons = {
                '.pdf' : 'file-pdf-regular.svg',
                '.docx': 'file-doc-solid.svg',
                '.doc' : 'file-doc-solid.svg',
                '.xls' : 'file-xls-solid.svg',
                '.xlsx': 'file-xls-solid.svg',
                '.csv' : 'file-csv-solid.svg',
                '.tsv' : 'file-tsv-solid.svg',
                '.txt' : 'file-txt-solid.svg',
                '.tex' : 'file-tex-solid.svg',
                '.bib' : 'file-bib-solid.svg'
        }

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

    def render_markdown_code_text_markups(self, text: str) -> str:
        """Converts markdown code markups to html code markups."""
        if "`" in text and text.count("`") % 2 == 0:
            probe = '`(.*?)`'
            codeTexts = re.findall(probe, text)

            for codeText in codeTexts:
                renderedText = f"<code>{codeText}</code>"
                text = text.replace(f'`{codeText}`', renderedText)
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

    def render_red_text_markups(self, text: str) -> str:
        """Converts latex style red text to html text style tag."""
        if "\\red{" in text:
            probe = '\\\\red{(.*?)}'
            redTexts = re.findall(probe, text)

            for redText in redTexts:
                renderedText = f'<span style="color:#FF0000";>{redText}</span>'
                text = text.replace(f'\\red{{{redText}}}', renderedText)
        return text

    def render_green_text_markups(self, text: str) -> str:
        """Converts latex style green text to html text style tag."""
        if "\\green{" in text:
            probe = '\\\\green{(.*?)}'
            greenTexts = re.findall(probe, text)

            for greenText in greenTexts:
                renderedText = f'<span style="color:#2EBF28";>{greenText}</span>'
                text = text.replace(f'\\green{{{greenText}}}', renderedText)
        return text

    def render_link_markups(self, text: str) -> str:
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

    def render_icon_markups(self, text: str) -> str:
        icons = {
                'todo' : '<img id="todoIcon" src="/static/icons/todo-circle-regular.svg" alt="drawing" width="20"/>',
                'done' : '<img id="todoIcon" src="/static/icons/check-circle-regular.svg" alt="drawing" width="20"/>',
                'error': '<img id="todoIcon" src="/static/icons/bug-solid.svg" alt="drawing" width="20"/>'
                }
        for icon in icons.keys():
            if f"\{icon}" in text:
                text = text.replace(f"\{icon}", icons[icon])
        return text

    def render_blockquote_markups(self, text: str) -> str:
        if text.startswith(">"):
            text = "<blockquote>{}</blockquote>".format(text[2:])
        return text

    def render_math_inline_markups(self, text: str) -> str:
        if "$" in text and text.count("$") % 2 == 0:
            probe = '\\$(.*?)\\$'
            mathTexts = re.findall(probe, text)
            for mathText in mathTexts:
                renderedText = f"<span class='katex-math-inline'>{mathText}</span>"
                text = text.replace(f'${mathText}$', renderedText)
        elif "\(" in text and '\)' in text:
            probe = '\\\\\((.*?)\\\\\)'
            mathTexts = re.findall(probe, text)
            for mathText in mathTexts:
                renderedText = f"<span class='katex-math-inline'>{mathText}</span>"
                text = text.replace(f'\({mathText}\)', renderedText)
        return text

    def render_script_markups(self, text: str) -> str:
        if "\\script{" in text:
            probe = '\\\\script{(.*?)}'
            scriptTexts = re.findall(probe, text)

            for scriptText in scriptTexts:
                try:
                    project, scriptPath = scriptText.split(",")
                    project = project.strip()
                    scriptPath = scriptPath.strip()
                except Exception:
                    text = '<span style="color:#FF0000";>Script markups should include: "project: script/path"<br>'+text
                    return text
                scriptID = project+"-"+scriptPath.replace("/", "-").replace(".", "-")
                sectionIndicator = f'<span class="badge badge-pill badge-info ">{project}: {scriptPath}</span>'
                renderedText = ('<div><a class="btn btn-sm btn-success text-white fresnote-script-button mr-2" role="button" '
                                f'onclick="viewScript(\'{project}\', \'{scriptPath}\')"> View</a> '
                                '<a class="btn btn-sm btn-warning text-black fresnote-script-button mr-2" role="button" '
                                f'onclick="runScript(\'{project}\', \'{scriptPath}\', \'{scriptID}\')">Run</a> {sectionIndicator} '
                                f'<span class="fresnote-spinner ml-2" hidden id="spinner-{scriptID}"></span> '
                                f'<span class="fresnote-spinner-text" hidden id="{scriptID}" style="color:red;"></span></div>')
                text = text.replace(f'\\script{{{scriptText}}}', renderedText)
        return text

    def render_table_markups(self, text: str) -> str:
        if "\\table{" in text:
            probe = '\\\\table{(.*?)}'
            tables = re.findall(probe, text)
            for table in tables:
                try:
                    title, project, tablePath, delimiter = table.split(",")
                    title = title.strip()
                    project = project.strip()
                    tablePath = tablePath.strip()
                    delimiter = delimiter.strip()
                except Exception:
                    text = '<span style="color:#FF0000";>Table markups should include: "title,project,table/path,delimiter"<br>'+text
                    return text
                renderedText = '<a href="/{project}/table/{filepath}/{delimiter}"><img id="todoIcon" src="/static/icons/table-solid.svg" alt="drawing" width="20"/> {title}</a>'.format(title=title, project=project, filepath=tablePath, delimiter=delimiter)
                text = text.replace(f'\\table{{{table}}}', renderedText)
        return text 

    def render_include_section_markups(self, text: str) -> str:
        if text.startswith('\include-section{'):
            probe = '\\\\include-section{(.*?)}'
            results = re.findall(probe, text)
            for res in results:
                try:
                    project, sectionID = res.split(',')
                    project = project.strip()
                    sectionID = int(sectionID.strip())
                except Exception:
                    text = '<span style="color:#FF0000";>Include-section markups should have: "project,sectionID"<br>'+text
                    return text

                try:
                    # The following import produces circular import error:
                    # from fresnote.classes import Notebook
                    # A workaround was to do the following import:
                    # import fresnote.classes
                    notes = fresnote.classes.Notebook(project, self.configName)
                    sectionsList = notes.get_sections_based_on_IDs([sectionID])
                except Exception:
                    text = f'<span style="color:#FF0000";>Error parsing content from section: "{project},{sectionID}"<br>'+text
                    return text
                sectionIndicator = f'<a href="/{project}/view/{sectionID}"><span class="badge badge-pill badge-info">{project}: section {sectionID}</span></a><hr>'
                if sectionsList:
                    renderedText = sectionIndicator + sectionsList[0]['content'] + '<hr>'
                else:
                    renderedText = sectionIndicator + '<span style="color:#FF0000";>No content found for section<br>'
                text = text.replace(f'\\include-section{{{res}}}', renderedText)
        return text


    def render_include_file_markups(self, text: str) -> str:
        if text.startswith('\include-file{'):
            probe = '\\\\include-file{(.*?)}'
            results = re.findall(probe, text)
            for res in results:
                try:
                    project, filePath = res.split(',')
                    project = project.strip()
                    filePath = filePath.strip()
                except Exception:
                    text = '<span style="color:#FF0000";>Include-file markups should have: "project,filePath"<br>'+text
                    return text

                try:
                    notes = fresnote.classes.Notebook(project, self.configName)
                    projectPath = Path(notes.projectPath)
                    filePath = projectPath.joinpath(filePath)
                except Exception:
                    text = '<span style="color:#FF0000";>Project does not exist: {project}<br>'+text
                    return text

                if not Path(filePath).exists():
                    text = '<span style="color:#FF0000";>Included file does not exist: {filePath}<br>'+text
                    return text

                sectionIndicator = f'<span class="badge badge-pill badge-info">file: {filePath}</span><hr>'
                fileContent = open(filePath, encoding="utf-8").read()
                renderedText = sectionIndicator+"<p><pre>"+fileContent+"</pre></p><hr>"
                text = text.replace(f'\\include-file{{{res}}}', renderedText)
        return text



class Renderer:

    def __init__(self, configName):
        self.configName = configName
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
                'img' : '<div class="container-fluid">',
                'list': '<ul>',
                'math': '<span class="katex-math-equation">'
        }

        # Define end html for markups
        self.renderEnd_markup = {
                'code': '</pre>',
                'fold': '</div></div></div><br>',
                'img' : '</div><br>',
                'list': '</ul>',
                'math': '</span>'
        }

        
        self.renderers = InlineRenderers(self.configName)
        self.renderersMethods = [method for method in dir(self.renderers) if callable(getattr(self.renderers, method)) and not method.startswith("__")]
        

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

    def pass_line_through_renderers(self) -> str:
        self.line = self.line.strip("\n")
        for method in self.renderersMethods:
            render = getattr(self.renderers, method)
            self.line = render(self.line)

    def renderLine(self) -> None: 
        if self.line.startswith('```'):
            flag = 'code'
        elif self.line.startswith('\\img{'):
            flag = 'img'
        elif self.line.startswith('\\fold{'):
            flag = 'fold'
        elif self.line.startswith('\\list{'):
            flag = 'list'
        elif self.line.startswith('$$'):
            flag = 'math'
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
        elif flag == "math":
            if self.is_last_flag("math"):
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
        elif flag == "list":
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
            elif self.is_last_flag("math"):
                self.renderedLines.append(self.line.strip("\n"))
            elif self.line.strip().strip("\n"):
                if self.is_last_flag('list'):
                    if self.line.startswith("* "):
                        self.line = self.line.replace("* ", '')
                    else:
                        if self.line.startswith("\\") and self.renderedLines[-1].startswith("<ul>"):
                            self.renderedLines[-1] = '<ul style="list-style: none;padding-left:1em;">'
                        elif not self.line.startswith("\\") and self.renderedLines[-1].startswith("<ul>"):
                            self.renderedLines[-1] = '<ul style="list-style: none;padding-left:1.4em;">'
                    self.pass_line_through_renderers()
                    self.line = f'<li>{self.line}</li>'
                    self.renderedLines.append(self.line)
                elif self.is_last_flag('img'):
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
                    self.pass_line_through_renderers()
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


