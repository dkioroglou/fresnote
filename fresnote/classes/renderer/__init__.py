# import markdown
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



class Renderer(Markdown, Latex):

    def pass_line_through_renderers(self, line: str, flags: Dict, ID: int) -> Tuple[str, Dict]: 

        def render_flag(flag, flags, *args):
            if flags['order'] and flags['order'][-1] == flag:
                    flags['order'].pop()
                    if args:
                        return (flags_end_markup[flag].format(*args), flags)
                    else:
                        return (flags_end_markup[flag], flags)
            else:
                flags['order'].append(flag)
                if args:
                    return (flags_start_markup[flag].format(*args), flags)
                else:
                    return (flags_start_markup[flag], flags)

        flags_start_markup = {
                'code': '<pre>',
                'fold': '<a class="btn btn-outline-light text-white col-12" data-toggle="collapse" href="#subsection_fold_{1}_{0}" role="button" aria-expanded="false" aria-controls="subsection_fold_{1}_{0}">{2}</a><div <div class="row"> <div class="col-12"> <div class="collapse" id="subsection_fold_{1}_{0}"><br>'
        }

        flags_end_markup = {
                'code': '</pre>',
                'fold': '</div></div></div><br>'
        }

        if not line.strip("\n"):
            return (line.strip('\n'), flags)

        if line.startswith('```'):
            try:
                line, flags = render_flag('code', flags) 
            except Exception:
                flags['errors'] = True
            return (line, flags)

        if line.startswith('\\fold{'):
            try:
                title = line.replace("\\fold{", "")
                flags['counts']['fold'] += 1
                args = [ID, flags['counts']['fold'], title]  
                line, flags = render_flag('fold', flags, *args) 
            except Exception:
                flags['errors'] = True
            return (line, flags)

        if line.startswith('}'):
            if flags['order'] and flags['order'][-1] == 'code':
                return (line, flags)
            else:
                try:
                    line, flags = render_flag(flags['order'][-1], flags)
                except Exception:
                    flags['errors'] = True
                return (line, flags)

        # Don't format text inside code-block.
        if flags['order'] and flags['order'][-1] == 'code':
            return (line, flags)

        line = self.render_markdown_headers_markups(line)
        line = self.render_markdown_bold_text_markups(line)
        line = self.render_markdown_italics_text_markups(line)
        line = self.render_latex_green_text_markups(line)
        line = self.render_latex_red_text_markups(line)
        line = "<p>"+line+"</p>"

        return (line, flags)


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
                    "section" :  section,
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
            renderedLines = list()
            flags = {'order':[], 
                     'counts': {'fold': 0},
                     'errors': False
                    }
            if '\n' in sectionDict['content']:
                contentLines = sectionDict['content'].splitlines(keepends=True)
                for line in contentLines:
                    line, flags = self.pass_line_through_renderers(line, flags, sectionDict['ID'])
                    if line:
                        renderedLines.append(line)
            else:
                line, flags = self.pass_line_through_renderers(sectionDict['content'], flags, sectionDict['ID'])
                if line:
                    renderedLines.append(line)

            # Produce error if markups are left in flags or close markups were not found.
            if flags['order'] or flags['errors']:
                sectionDict['content'] = "<r>Errors while rendering section. Check markups.</r>\n"+sectionDict['content']
            else:
                sectionDict['content'] = ''.join(renderedLines).replace('\n', '<br>')
            tmp[sectionDict['ID']] = sectionDict
        sections = list()
        for sID in sectionsIDs:
            sections.append(tmp[sID])
        return sections


