import markdown
import re

md = markdown.Markdown(extensions=['mdx_math', 'tables', 
                                   'fenced_code', 'toc', 
                                   'admonition', 'sane_lists', 
                                   'nl2br', 'pymdownx.tasklist'])

class Renderer:

    def convert_db_results_into_sections(self, notebook, chapter, sectionsResults, sectionsIDs):

        def process_tags(tags):
            if ',' in tags:
                tags = [x.strip(' ') for x in tags.split(',')]
            else:
                tags = [tags.strip(' ')]
            return tags

        sections = list()
        tmp = dict()
        if sectionsResults:
            for res in sectionsResults:
                ID, section, tags, content, visible, folded, creationDate = res

                tags = process_tags(tags)
                content = self.replace_includes(content)
                content = self.replace_includes_folded(content, ID)

                sectionDict = dict()
                sectionDict['project'] = info["project"]
                sectionDict['chapter'] = info["chapter"]
                sectionDict['ID'] = ID
                # sectionDict['section'] = self.replace_various_markups_for_section(section, content)
                sectionDict['section'] = section
                sectionDict['section'] = self.insert_tag_icon_annotations_to_section(tags, sectionDict['section'])
                sectionDict['tags'] = tags
                sectionDict['content'] = md.convert(content)
                sectionDict['content'] = self.replace_various_markups(sectionDict['content'], ID)
                sectionDict['folded'] = folded
                
                tmp[ID] = sectionDict

            # Put sections with order specified in passed order list
            for sID in order:
                sections.append(tmp[sID])
        return sections

    def replace_includes(self, text):
        if '\\include{' in text:
            probe = '\\\\include{(.*?)}'
            includes = re.findall(probe, text)

            for include in includes:
                project = False
                try:
                    if ":" in include:
                        project, includeID = include.split(":")
                        project = project.strip(' ')
                        includeID = int(includeID.strip(" "))
                    else:
                        includeID = int(include.strip(' '))

                    if project:
                        includeContent = get_section_content(notebook, includeID)
                    else:
                        includeContent = self.get_section_content_without_backup(includeID)

                except Exception:
                    text = "<r>Error retrieving content for included sections</r>\n"+text 
                    text = text.replace('\\include{{{}}}'.format(include), '<r>\\include{{{}}}</r>'.format(include))
                    return text
                if notebook:
                    sectionIndicator = '<a href="/{0}/view_sections/{1}"><span class="badge badge-pill badge-info">section {1}</span></a><hr>'.format(notebook, includeID)
                else:
                    sectionIndicator = '<a href="/{0}/view_sections/{1}"><span class="badge badge-pill badge-info">section {1}</span></a><hr>'.format(self.notebookName, includeID)
                includeContent = sectionIndicator + '\\begin{included-section-marker}\n' + includeContent + "\n\n" + "<hr>" + '\\end{included-section-marker}' + "<br>"
                if notebook:
                    text = text.replace('\\include{{{}:{}}}'.format(notebook, includeID), includeContent)
                else:
                    text = text.replace('\\include{{{{}}}}'.format(includeID), includeContent)
        return text




# def get_section_content_without_backup_from_another_notebook(notebook, ID):
#     notebookDir = config.get(notebook, 'notebookDir')
#     if '~' in notebookDir:
#         notebookDir = os.path.expanduser(notebookDir)
#     db = '{}/{}'.format(notebookDir, config.get(notebook, 'notebookDB'))
#     with contextlib.closing(sqlite3.connect(db)) as conn:
#         with contextlib.closing(conn.cursor()) as c:
#             query = """
#             SELECT content FROM knowledgebase 
#             WHERE id=(?)
#             """
#
#             c.execute(query, (ID,))
#             result = c.fetchone()
#     sectionContent = result[0]
#     return sectionContent
#

#     def replace_book_markups(self, text):
#         probe = '\\\\book{(.*?)}'
#         books = re.findall(probe, text)
#
#         parts = re.split(probe, text)
#         tmp = list()
#         for part in parts:
#             if part in books:
#                 book, page = part.split(',')
#                 book = book.strip(' ')
#                 page = page.strip(' ')
#                 part = '<a href="https://dkioroglou.com/read_book?file=protected/books/{}.pdf#page={}"><img id="todoIcon" src="/static/icons/book-solid.svg" alt="drawing" width="20"/></a>'.format(book, page)
#             tmp.append(part)
#
#         text = ''.join(tmp)
#         return text
#
#
#
#     def replace_script_markups(self, text):
#         probe = '\\\\script{(.*?)}'
#         scripts = re.findall(probe, text)
#         parts = re.split(probe, text)
#         tmp = list()
#         for part in parts:
#             if part in scripts:
#                 scriptName = part
#                 part = """
#                 <a href="/{}/highlight/{}" role="button">
#                 <img id="todoIcon" src="/static/icons/file-code-regular.svg" alt="drawing" width="20"/> {}
#                 </a>
#                 """.format(self.notebookName, scriptName, scriptName)
#             tmp.append(part)
#         text = ''.join(tmp)
#         return text
#
#
#     def replace_view_file_markups(self, text):
#         probe = '\\\\view-file{(.*?)}'
#         files = re.findall(probe, text)
#
#         parts = re.split(probe, text)
#         tmp = list()
#         for part in parts:
#             if part in files:
#                 fileName = part
#                 filePath = os.path.join(self.docsDir, fileName)
#                 if os.path.exists(filePath):
#                     fileContent = open(filePath, encoding="utf-8").read()
#                 else:
#                     fileContent = "File not found:\n{}".format(fileName)
#                 part = """
# <pre style="background-color:#F0F0F0; padding: 12px; font-size: 14px;">
# {}
# </pre>""".format(fileContent)
#             tmp.append(part)
#
#         text = ''.join(tmp)
#         return text
#
#
#     """
#     NOTES:
#         STAYS - CHANGED
#     """
#     def replace_button_image_markups(self, text):
#         probe = '\\\\btnimg{(.*?)}'
#         imgs = re.findall(probe, text)
#
#         parts = re.split(probe, text)
#         tmp = list()
#         for part in parts:
#             if part in imgs:
#                 try:
#                     caption, url, width, height = part.split(',')
#                 except Exception:
#                     return 'Error: btnimg requires caption, url, width, height.'
#                 caption= caption.strip(' ')
#
#                 if url.strip(' ').split('/')[1] in self.allNotebooks:
#                     url = url.strip(' ')
#                 else:
#                     url = '/{}'.format(self.notebookName) + url.strip(' ')
#
#                 width = width.strip(' ')
#                 height = height.strip(' ')
#                 part = """
#                 <a class="btn btn-secondary mt-2" href="{}" role="button">
#                 {} <br>
#                 <img src="{}" width="{}" height="{}">
#                 </a>
#                 """.format(url, caption, url, width, height)
#
#             tmp.append(part)
#
#         text = ''.join(tmp)
#         return text
#
#
#     def replace_images_markups(self, text):
#         probe = '\\\\imgs{(.*?)}'
#         IMGS = re.findall(probe, text, re.DOTALL)
#
#         if IMGS:
#             for image in IMGS:
#                 tmp = ['<div class="container-fluid">']
#                 imgList = image.split("<br />\n")
#                 for img in imgList:
#
#                     try:
#                         caption, url, width, height = img.split(',')
#                     except Exception:
#                         return '<r>Error: images markups requires caption, url, width, height for each image. Also ending curly bracket should be at the end of the final image and not in newline.</r>\n\n' + text
#
#                     caption= caption.strip(' ')
#                     if url.strip(' ').split('/')[1] in self.allNotebooks:
#                         url = url.strip(' ')
#                     else:
#                         url = '/{}'.format(self.notebookName) + url.strip(' ')
#                     width = width.strip(' ')
#                     height = height.strip(' ')
#
#                     part = """
#                     <a class="btn btn-secondary mt-2" href="{}" role="button">
#                     {} <br>
#                     <img src="{}" width="{}" height="{}">
#                     </a>
#                     """.format(url, caption, url, width, height)
#                     tmp.append(part)
#
#                 tmp.append('<br><br>')
#                 tmp.append('</div>')
#                 tmp = ''.join(tmp)
#                 text = text.replace('\\imgs{{{}}}'.format(image), tmp)
#             return text
#         else:
#             return text
#
#
#
#     def replace_link_markups(self, text):
#         probe = '\\\\link{(.*?)}'
#         links = re.findall(probe, text)
#
#         parts = re.split(probe, text)
#         tmp = list()
#         for part in parts:
#             if part in links:
#
#                 try:
#                     reference, url = part.split(',')
#                 except Exception:
#                     return 'Error: link requires reference and url.'
#
#                 reference= reference.strip(' ')
#                 url = url.strip(' ')
#                 urlExtension = os.path.splitext(url)[-1]
#                 docsIcons = {
#                         '.pdf': 'file-pdf-regular.svg',
#                         '.docx': 'file-alt-regular.svg',
#                         '.doc': 'file-alt-regular.svg',
#                         '.xls': 'file-alt-regular.svg',
#                         '.xlsx': 'file-alt-regular.svg',
#                         '.csv': 'file-csv-solid.svg',
#                         '.txt': 'file-alt-regular.svg',
#                         '.tex': 'file-alt-regular.svg',
#                         '.bib': 'file-alt-regular.svg',
#                         '.tsv': 'file-csv-solid.svg'
#                         }
#                 if urlExtension and urlExtension in docsIcons.keys():
#                     part = '<a href="{}"><img id="todoIcon" src="/static/icons/{}" alt="drawing" width="20"/> {}</a>'.format(url, docsIcons[urlExtension], reference)
#                 else:
#                     part = '<a href="{}">{}</a>'.format(url, reference)
#             tmp.append(part)
#
#         text = ''.join(tmp)
#         return text
#
#
#
#     def replace_button_markups(self, text):
#         probe = '\\\\button{(.*?)}'
#         buttons = re.findall(probe, text)
#
#         parts = re.split(probe, text)
#         tmp = list()
#         for part in parts:
#             if part in buttons:
#                 linkName, url = part.split('---')
#                 linkName = linkName.strip(' ')
#                 url = url.strip(' ')
#                 part = '<a class="btn btn-sm btn-outline-secondary" role="button" href="{}">{}</a>'.format(url, linkName)
#             tmp.append(part)
#
#         text = ''.join(tmp)
#         return text
#
#
#
#     """
#     NOTES:
#         STAYS - CHANGED 
#     """
#     def table(self, text, ID):
#         probe = '\\\\table{(.*?)}'
#         tables = re.findall(probe, text)
#
#         parts = re.split(probe, text)
#         tmp = list()
#         count = 1
#         for part in parts:
#             if part in tables:
#                 try:
#                     title, fname, separator = part.split(',')
#                 except Exception:
#                     return "<r>Error: table markup excepts title, filename and separator</r>\n"+text
#                 title = title.strip(' ')
#                 fname = fname.strip(' ')
#                 separator = separator.strip(' ')
#                 if fname.startswith('/'):
#                     fpath = "{}{}".format(self.notebookDir, fname)
#                 else:
#                     fpath = "{}/{}".format(self.notebookDir, fname)
#                 if os.path.exists(fpath):
#                     part = '<a href="/{}/view_table/{}/{}"><img id="todoIcon" src="/static/icons/table-solid.svg" alt="drawing" width="20"/> {}</a>'.format(self.notebookName, fname, separator, title)
#                     tmp.append(part)
#                 else:
#                     tmp.append('Table: {}'.format(fpath))
#                     count += 1
#             else:
#                 tmp.append(part)
#         text = ''.join(tmp)
#         return text
#
#
#
#     """
#     NOTES:
#         STAYS - UNCHANGED 
#     """
#     def table_data(self, text, ID):
#         probe = '\\\\table_data{(.*?)}'
#         tables = re.findall(probe, text, re.DOTALL)
#
#         separator = ','
#         count = 1
#         for data in tables:
#             cols, *rows = data.split('\n')
#             table = '<input type="text" id="filterTableInput_{0}_{1}" onkeyup="dkFilterTable({0},{1})" placeholder="Filter table" title="Filter table"><br><br>'.format(ID, count)
#             table += '<table id="dkTable_{0}_{1}" class="table table-striped"><thead><tr>'.format(ID, count)
#             for col in cols.split(separator):
#                 table += '<th>{}</th>'.format(col)
#             table += '</tr></thead><tbody>'
#
#             for row in rows:
#                 table += '<tr>'
#                 for col in row.split(separator):
#                     table += "<td>{}</td>".format(col)
#                 table += "</tr>"
#             table += '</tbody></table>\n'
#
#             text = text.replace('\\table_data{{{}}}'.format(data), table)
#             count += 1
#         return text
#
#
#
#
#     def replace_view_pdf_markups(self, text):
#         probe = '\\\\view-pdf{(.*?)}'
#         books = re.findall(probe, text)
#
#         parts = re.split(probe, text)
#         tmp = list()
#         for part in parts:
#             if part in books:
#                 part = '<a href="https://dkioroglou.com/read_book?file=view_pdf_serve_dir/{}"><img id="todoIcon" src="/static/icons/book-solid.svg" alt="drawing" width="20"/></a>'.format(part)
#             tmp.append(part)
#
#         text = ''.join(tmp)
#         return text
#
#
#     def replace_details_fold_markups(self, text):
#         probe = '\\\\details{(.*?)}'
#         details = re.findall(probe, text, re.DOTALL)
#
#         for detail in details:
#             title, *content = detail.split('\n')
#             content = '\n'.join(content)
#             newText = """<details>
# <summary>{}</summary>
# {}
# </details>
# """.format(title, content)
#             text = text.replace('\\details{{{}}}'.format(detail), newText)
#         return text
#
#
#     """
#     NOTES:
#         STAYS - CHANGED 
#     """
#
#
#     """
#     NOTES:
#         STAYS - CHANGED 
#     """
#     def replace_includes_folded(self, text, ID):
#         if '\\include-folded{' in text:
#             probe = '\\\\include-folded{(.*?)}'
#             includes = re.findall(probe, text)
#
#             count = 1
#             for include in includes:
#                 notebook = False
#                 try:
#                     if ":" in include:
#                         notebook, includeID = include.split(":")
#                         notebook = notebook.strip(' ')
#                         includeID = int(includeID.strip(" "))
#                     else:
#                         includeID = int(include.strip(' '))
#                     if notebook:
#                         includeContent = get_section_content_without_backup_from_another_notebook(notebook, includeID)
#                     else:
#                         includeContent = self.get_section_content_without_backup(includeID)
#                 except Exception:
#                     text = "<r>Error retrieving content for included sections</r>\n"+text 
#                     text = text.replace('\\include-folded{{{}}}'.format(include), '<r>\\include-folded{{{}}}</r>'.format(include))
#                     return text
#
#                 if notebook:
#                     sectionIndicator = '<a data-toggle="collapse" href="#included_section_fold_{1}_{2}" role="button" aria-expanded="false" aria-controls="included_section_fold_{1}_{2}"><span class="ml-2 badge badge-pill badge-dark">view</span></a><a href="/{3}/view_sections/{0}"><span class="badge badge-pill badge-info">section {0}</span></a><hr>'.format(includeID, ID, count, notebook)
#                 else:
#                     sectionIndicator = '<a data-toggle="collapse" href="#included_section_fold_{1}_{2}" role="button" aria-expanded="false" aria-controls="included_section_fold_{1}_{2}"><span class="ml-2 badge badge-pill badge-dark">view</span></a><a href="/{3}/view_sections/{0}"><span class="badge badge-pill badge-info">section {0}</span></a><hr>'.format(includeID, ID, count, self.notebookName)
#                 includeContent = sectionIndicator + '\\begin{included-section-marker-folded}\n' + includeContent + "\n\n" + '<hr>' + '\\end{included-section-marker-folded}' + '<br>'
#                 if notebook:
#                     text = text.replace('\\include-folded{{{}:{}}}'.format(notebook, includeID), includeContent)
#                 else:
#                     text = text.replace('\\include-folded{{{}}}'.format(includeID), includeContent)
#                 count += 1
#         return text
#
#
#
#     def replace_folding_markups(self, text, sectionID):
#         beginCounts = text.count("\\begin{fold}")
#         endCounts = text.count("\\end{fold}")
#
#         if beginCounts != endCounts:
#             text = "<r>Error: No matching numbers of begin and end folds</r>\n"+ text
#             return text
#
#         count = 1
#         while True: 
#             beginStartIDX = text.find('\\begin{fold}')
#
#             if beginStartIDX == -1:
#                 break
#
#             beginEndIDX = beginStartIDX + len('\\begin{fold}')
#
#             endStartIDX = text.find('\\end{fold}')
#             endEndIDX = endStartIDX + len('\\end{fold}')
#
#             foldText = text[beginEndIDX:endStartIDX]
#             title, *rest = foldText.split('\n')
#
#             foldText = '\n'.join(rest)
#
#             if title == '</p>':
#                 title = 'Unfold'
#             
#             newFoldText = """
# <a class="btn btn-outline-light text-white col-12" data-toggle="collapse" href="#subsection_fold_{3}_{0}" role="button" aria-expanded="false" aria-controls="subsection_fold_{3}_{0}">{2}</a>
# <div class='container-fluid'>
# <div class='row'>
# <div class='col-12'>
# <div class='collapse' id="subsection_fold_{3}_{0}">
# {1}
# </div>
# </div>
# </div>
# </div>
# """.format(count, foldText, title, sectionID)
#             text = text[:beginEndIDX] + newFoldText + text[endStartIDX:]
#             text = text.replace('\\begin{fold}', '', 1)
#             text = text.replace('\\end{fold}', '', 1)
#             count += 1
#         return text
#
#
#     def replace_included_section_marker(self, text):
#         beginCounts = text.count("\\begin{included-section-marker}")
#         endCounts = text.count("\\end{included-section-marker}")
#
#         if beginCounts != endCounts:
#             text = "<r>Error: No matching numbers of begin and end for included sections markers</r>\n"+ text
#             return text
#
#         while True: 
#             beginStartIDX = text.find('\\begin{included-section-marker}')
#
#             if beginStartIDX == -1:
#                 break
#
#             beginEndIDX = beginStartIDX + len('\\begin{included-section-marker}')
#
#             endStartIDX = text.find('\\end{included-section-marker}')
#             endEndIDX = endStartIDX + len('\\end{included-section-marker}')
#
#             foldText = text[beginEndIDX:endStartIDX]
#
#             newFoldText = """
# <div class='card-body' id='included-section-card-body'>
# {}
# </div>
# """.format(foldText)
#             text = text[:beginEndIDX] + newFoldText + text[endStartIDX:]
#             text = text.replace('\\begin{included-section-marker}', '', 1)
#             text = text.replace('\\end{included-section-marker}', '', 1)
#         return text
#
#
#     def replace_included_section_marker_folded(self, text, ID):
#         beginCounts = text.count("\\begin{included-section-marker-folded}")
#         endCounts = text.count("\\end{included-section-marker-folded}")
#
#         if beginCounts != endCounts:
#             text = "<r>Error: No matching numbers of begin and end for included sections markers</r>\n"+ text
#             return text
#
#         count = 1
#         while True: 
#             beginStartIDX = text.find('\\begin{included-section-marker-folded}')
#
#             if beginStartIDX == -1:
#                 break
#
#             beginEndIDX = beginStartIDX + len('\\begin{included-section-marker-folded}')
#
#             endStartIDX = text.find('\\end{included-section-marker-folded}')
#             endEndIDX = endStartIDX + len('\\end{included-section-marker-folded}')
#
#             foldText = text[beginEndIDX:endStartIDX]
#
#             newFoldText = """
# <div class='collapse' id="included_section_fold_{0}_{1}">
# <div class='card-body' id='included-section-card-body'>
# {2}
# </div>
# </div>
# """.format(ID, count, foldText)
#             text = text[:beginEndIDX] + newFoldText + text[endStartIDX:]
#             text = text.replace('\\begin{included-section-marker-folded}', '', 1)
#             text = text.replace('\\end{included-section-marker-folded}', '', 1)
#             count += 1
#         return text
#
#
#
#     def replace_various_markups(self, text, ID):
#         if '\\begin{fold}' in text:
#             text = self.replace_folding_markups(text, ID)
#         if '\\begin{included-section-marker}' in text:
#             text = self.replace_included_section_marker(text)
#         if '\\begin{included-section-marker-folded}' in text:
#             text = self.replace_included_section_marker_folded(text, ID)
#         if '<table>' in text:
#             text = text.replace('<table>', '<table class="table table-striped">')
#         if '\\table{' in text:
#             text = self.table(text, ID)
#         if '\\table_data{' in text:
#             text = self.table_data(text, ID)
#         if '\\book{' in text:
#             text = self.replace_book_markups(text)
#         if '\\button{' in text: 
#             try:
#                 text = self.replace_button_markups(text)
#             except Exception:
#                 text = "<r>Error replacing button markups</r>"+text
#         if '\\details{' in text:
#             text = self.replace_details_fold_markups(text)
#         if '\\btnimg{' in text: 
#             text = self.replace_button_image_markups(text)
#         if '\\imgs{' in text: 
#             text = self.replace_images_markups(text)
#         if '\\link{' in text: 
#             text = self.replace_link_markups(text)
#         if '\\script{' in text: 
#             text = self.replace_script_markups(text)
#         if '\\view-pdf{' in text:
#             text = self.replace_view_pdf_markups(text)
#         if '\\view-file{' in text:
#             text = self.replace_view_file_markups(text)
#         if '\\note{' in text:
#             text = text.replace('\\note{', '<div class="admonition note">')
#             text = text.replace('}', '</div>')
#         if '\\todo' in text:
#             text = text.replace('\\todo', '<img id="todoIcon" src="/static/icons/circle-regular.svg" alt="drawing" width="20"/>')
#         if '\\done' in text:
#             text = text.replace('\\done', '<img id="todoIcon" src="/static/icons/check-circle-regular.svg" alt="drawing" width="20"/>')
#         if '\\pdf' in text:
#             text = text.replace('\\pdf', '<img id="todoIcon" src="/static/icons/file-pdf-regular.svg" alt="drawing" width="20"/>')
#         if '\\script' in text:
#             text = text.replace('\\script', '<img id="todoIcon" src="/static/icons/file-code-regular.svg" alt="drawing" width="20"/>')
#         if '\\csv' in text:
#             text = text.replace('\\csv', '<img id="todoicon" src="/static/icons/file-csv-solid.svg" alt="drawing" width="20"/>')
#         # if '\\img' in text:
#         #     text = text.replace('\\img', '<img id="todoIcon" src="/static/icons/file-image-regular.svg" alt="drawing" width="20"/>')
#         if '\\file' in text:
#             text = text.replace('\\file', '<img id="todoIcon" src="/static/icons/file-alt-regular.svg" alt="drawing" width="20"/>')
#         if '\\bug' in text:
#             text = text.replace('\\bug', '<img id="todoIcon" src="/static/icons/bug-solid.svg" alt="drawing" width="20"/>')
#         if '\\error' in text:
#             text = text.replace('\\error', '<img id="todoIcon" src="/static/icons/bug-solid.svg" alt="drawing" width="20"/>')
#         if '\\header' in text:
#             text = text.replace('\\header', '<img id="todoIcon" src="/static/icons/bookmark-regular.svg" alt="drawing" width="20"/>')
#         if '\\result' in text:
#             text = text.replace('\\result', '<img id="todoIcon" src="/static/icons/flag-regular.svg" alt="drawing" width="20"/>')
#         # rq = research question
#         if '\\rq' in text:
#             text = text.replace('\\rq', '<img id="todoIcon" src="/static/icons/question-circle-solid.svg" alt="drawing" width="20"/>')
#         if '\\info' in text:
#             text = text.replace('\\info', '<img id="todoIcon" src="/static/icons/info-circle-solid.svg" alt="drawing" width="20"/>')
#         return text
#
#
#
#
#
#     def insert_tag_icon_annotations_to_section(self, tags, section):
#         iconTodo = '<img id="todoIcon" src="/static/icons/circle-regular.svg" alt="drawing" width="20"/>'
#         iconDone = '<img id="todoIcon" src="/static/icons/check-circle-regular.svg" alt="drawing" width="20"/>'
#         iconError = '<img id="todoIcon" src="/static/icons/bug-solid.svg" alt="drawing" width="20"/>'
#
#         if 'seen' in tags:
#             icon = '<img id="todoIcon" src="/static/icons/eye-solid.svg" alt="drawing" width="20"/>'
#             section = "{} {}".format(icon, section)
#
#         if 'todo' in tags: 
#             if iconTodo in section: 
#                 section = section.replace(iconTodo, '')
#
#             if iconDone in section: 
#                 section = section.replace(iconDone, '')
#
#             if iconError in section: 
#                 section = section.replace(iconError, '')
#
#             section = "{} {}".format(iconTodo, section)
#
#         if 'done' in tags:
#             if iconTodo in section: 
#                 section = section.replace(iconTodo, '')
#
#             if iconDone in section: 
#                 section = section.replace(iconDone, '')
#
#             if iconError in section: 
#                 section = section.replace(iconError, '')
#
#             section = "{} {}".format(iconDone, section)
#
#         if 'error' in tags:
#             if iconTodo in section: 
#                 section = section.replace(iconTodo, '')
#
#             if iconDone in section: 
#                 section = section.replace(iconDone, '')
#
#             if iconError in section: 
#                 section = section.replace(iconError, '')
#
#             section = "{} {}".format(iconError, section)
#
#         return section
#
#
#     def get_all_tags_from_DB(self):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT tags from knowledgebase
#                 """
#                 c.execute(query)
#                 results = c.fetchall()
#
#         tags = OrderedDict()
#         if results:
#             for res in results:
#                 tagList = res[0]
#                 if ',' in tagList:
#                     tagList = [x.strip(' ') for x in tagList.split(',')]
#                 else:
#                     tagList = [tagList]
#
#                 for tag in tagList:
#                     if not tags.get(tag, False):
#                         tags[tag] = True
#         if tags:
#             tags = [x for x in tags.keys()]
#         else:
#             tags = list()
#         return tags
#
#
#     # DEPRECATED
#     def replace_various_markups_for_section(self, section, content):
#         if '\error' in content:
#             return '<img id="todoIcon" src="/static/icons/bug-solid.svg" alt="drawing" width="20"/> {}'.format(section)
#         elif '\done' in content and not '\\todo' in content:
#             return '<img id="todoIcon" src="/static/icons/check-circle-regular.svg" alt="drawing" width="20"/> {}'.format(section)
#         elif '\\todo' in content:
#             return '<img id="todoIcon" src="/static/icons/circle-regular.svg" alt="drawing" width="20"/> {}'.format(section)
#         else:
#             return section
#         
#
#
#     def get_sections_from_DB_based_on_tags(self, tags, queryType):
#         md = markdown.Markdown(extensions=['mdx_math', 'tables', 'fenced_code', 'toc', 'admonition', 'sane_lists', 'nl2br', 'pymdownx.tasklist'])
#
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = "SELECT * FROM knowledgebase WHERE "
#
#                 if queryType == 'OR':
#                     if len(tags) == 1:
#                         query += 'tags LIKE "%{}%"'.format(tags[0])
#                     else:
#                         for i in range(len(tags)):
#                             if i != len(tags) - 1:
#                                 query += 'tags LIKE "%{}%" OR '.format(tags[i])
#                             else:
#                                 query += 'tags LIKE "%{}%"'.format(tags[i])
#                 else:
#                     if len(tags) == 1:
#                         query += 'tags LIKE "%{}%"'.format(tags[0])
#                     else:
#                         for i in range(len(tags)):
#                             if i != len(tags) - 1:
#                                 query += 'tags LIKE "%{}%" AND '.format(tags[i])
#                             else:
#                                 query += 'tags LIKE "%{}%"'.format(tags[i])
#
#                 c.execute(query)
#                 results = c.fetchall()
#
#         sections = self.convert_db_results_into_sections(results)
#             
#         return sections
#
#
#     def create_new_notebook(self):
#         """Creates new notebook"""
#         # Create notebook directory if it doesn't exist
#         if not os.path.exists(self.notebookDir):
#             os.system('mkdir {}'.format(self.notebookDir))
#
#         # Delete previous projects if notebook existed
#         if os.path.exists('{}'.format(self.docsDir)):
#             os.system('rm -rf {}'.format(self.docsDir))
#
#         # Delete previous database if notebook existed
#         if os.path.exists('{}'.format(self.db)):
#             os.system('rm {}'.format(self.db))
#
#         # Create projects folders
#         os.system('mkdir {}'.format(self.docsDir))
#
#         # Create database
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 CREATE TABLE knowledgebase(
#                 id INTEGER PRIMARY KEY,
#                 section TEXT,
#                 tags TEXT,
#                 content TEXT,
#                 visible INTEGER,
#                 folded INTEGER,
#                 creationDate TEXT
#                 )
#                 """
#
#                 c.execute(query)
#                 conn.commit()
#
#                 query = """
#                 CREATE TABLE chapters(
#                 id INTEGER PRIMARY KEY,
#                 project TEXT,
#                 chapter TEXT,
#                 sections TEXT
#                 )
#                 """
#
#                 c.execute(query)
#                 conn.commit()
#
#
#
#
#
#
#
#
#     def add_section_to_kb(self, section, tags, content):
#         """Adds new section without specifying chapter"""
#
#         today = datetime.today().strftime('%Y-%m-%d')
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 INSERT INTO knowledgebase 
#                 (section, tags, content, visible, folded, creationDate)
#                 VALUES (?,?,?,?,?,?)
#                 """
#
#                 c.execute(query, (section, tags, content, 1, 1, today))
#                 conn.commit()
#
#
#     def add_new_section(self, project, chapter):
#         """Adds new section to knowledgebase and assigns it to specific chapter"""
#
#         today = datetime.today().strftime('%Y-%m-%d')
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 INSERT INTO knowledgebase 
#                 (section, tags, content, visible, folded, creationDate)
#                 VALUES (?,?,?,?,?,?)
#                 """
#
#                 c.execute(query, ('New section', 'na', 'Section content', 1, 0, today))
#                 sectionID = c.lastrowid
#                 conn.commit()
#
#
#                 query = """
#                 SELECT sections FROM chapters 
#                 WHERE project == (?) AND chapter == (?)
#                 """
#
#                 c.execute(query, (project, chapter))
#                 sections = c.fetchone()[0]
#
#                 sections = json.loads(sections)
#                 sections.append(sectionID)
#
#                 query = """
#                 UPDATE chapters 
#                 SET sections=(?) 
#                 WHERE project == (?) AND chapter == (?)
#                 """
#
#                 c.execute(query, (json.dumps(sections), project, chapter))
#                 conn.commit()
#
#         return sectionID
#
#
#
#
#     def change_project_title(self, previousProjectTitle, newProjectTitle):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE chapters 
#                 SET project=(?) 
#                 WHERE project == (?)
#                 """
#
#                 c.execute(query, (newProjectTitle, previousProjectTitle))
#                 conn.commit()
#
#         if os.path.exists('{}/{}'.format(self.docsDir, previousProjectTitle)):
#             os.system('mv {}/{} {}/{}'.format(self.docsDir, previousProjectTitle, self.docsDir, newProjectTitle))
#
#
#
#     def change_chapter_title(self, projectTitle, previousChapterTitle, newChapterTitle):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE chapters 
#                 SET chapter=(?) 
#                 WHERE chapter == (?) AND project == (?)
#                 """
#
#                 c.execute(query, (newChapterTitle, previousChapterTitle, projectTitle))
#                 conn.commit()
#
#
#     def save_chapter_sections_order(self, project, chapter, sections):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE chapters 
#                 SET sections=(?) 
#                 WHERE project == (?) AND chapter == (?)
#                 """
#
#                 c.execute(query, (json.dumps(sections), project, chapter))
#                 conn.commit()
#
#
#
#
#
#
#
#     def get_all_sections_ids_for_chapter(self, project, chapter):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT sections FROM chapters 
#                 WHERE project=(?) AND chapter=(?)
#                 """
#                 c.execute(query, (project, chapter))
#                 sectionsIDs = c.fetchone()
#                 
#         if sectionsIDs:
#             sectionsIDs = json.loads(sectionsIDs[0])
#         else:
#             sectionsIDs = []
#         return sectionsIDs
#
#
#     def get_all_sections_ids_for_project(self, project):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT sections FROM chapters 
#                 WHERE project=(?)
#                 """
#                 c.execute(query, (project, ))
#                 results = c.fetchall()
#
#         sectionsIDs = []
#         if results:
#             for res in results:
#                 sectionsIDs.extend(json.loads(res[0]))
#         return sectionsIDs
#
#
#     
#     def get_section_content(self, ID):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT content FROM knowledgebase 
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (ID,))
#                 result = c.fetchone()
#         sectionContent = result[0]
#
#         # Backup content in case part of the previous section is lost
#         with open('{}/backup_of_last_modified_section.md'.format(self.notebookDir), 'w', encoding='utf-8') as outf:
#             print(sectionContent, file=outf)
#
#         return sectionContent
#
#
#     def get_section_content_without_backup(self, ID):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT content FROM knowledgebase 
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (ID,))
#                 result = c.fetchone()
#         sectionContent = result[0]
#
#         return sectionContent
#
#
#     def get_section_tags(self, ID):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT tags FROM knowledgebase 
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (ID,))
#                 result = c.fetchone()
#         sectionTags = result[0]
#
#         return sectionTags
#
#
#
#     def get_project_and_chapter_of_section(self, ID):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT project, chapter FROM knowledgebase
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (ID,))
#                 result = c.fetchone()
#         project, chapter = result
#         
#         return (project, chapter)
#
#
#
#     def save_section_title(self, ID, section):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE knowledgebase 
#                 SET section=(?) 
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (section, ID))
#                 conn.commit()
#
#
#     def save_section_tags(self, ID, tags):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE knowledgebase 
#                 SET tags=(?) 
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (tags, ID))
#                 conn.commit()
#
#
#
#     def save_section_content(self, ID, content):
#         # md = markdown.Markdown(extensions=['mdx_math', 'tables', 'fenced_code', 'toc', 'admonition', 'sane_lists', 'nl2br'])
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE knowledgebase 
#                 SET content=(?) 
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (content, ID))
#                 conn.commit()
#         # return md.convert(content)
#
#
#
#
#     def toggle_fold_state_of_section(self, ID):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE knowledgebase
#                 SET folded = CASE WHEN folded = 0 THEN 1 ELSE 0 END
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (ID,))
#                 conn.commit()
#
#
#     def toggle_hide_state_of_section(self, ID):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 UPDATE knowledgebase
#                 SET visible = CASE WHEN visible = 0 THEN 1 ELSE 0 END
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (ID,))
#                 conn.commit()
#
#
#     def delete_section(self, ID):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 DELETE FROM knowledgebase
#                 WHERE id=(?)
#                 """
#
#                 c.execute(query, (ID,))
#                 conn.commit()
#
#                 query = """
#                 SELECT project, chapter, sections FROM chapters
#                 """
#
#                 c.execute(query)
#                 results = c.fetchall()
#
#                 entriesToUpdate = list()
#                 for res in results:
#                     project, chapter, sections = res
#                     sections = json.loads(sections)
#                     if int(ID) in sections:
#                         sections.remove(int(ID))
#                         entriesToUpdate.append((json.dumps(sections), project, chapter))
#
#                 if entriesToUpdate:
#                     query = """
#                     UPDATE chapters 
#                     SET sections=(?) 
#                     WHERE project=(?) AND chapter=(?)
#                     """
#
#                     c.executemany(query, entriesToUpdate)
#                     conn.commit()
#
#
#     def delete_chapter_from_project(self, projectName, chapterName):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 DELETE FROM chapters
#                 WHERE project=(?) AND chapter=(?)
#                 """
#
#                 c.execute(query, (projectName, chapterName))
#                 conn.commit()
#
#
#     def delete_project(self, projectName):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 DELETE FROM chapters
#                 WHERE project=(?)
#                 """
#
#                 c.execute(query, (projectName,))
#                 conn.commit()
#
#
#     def get_sections_based_on_query(self, query):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 # TODO: temporary solution for executing a query that is not about SELECT with aggregator
#                 if 'SELECT' in query:
#                     c.execute(query)
#                     results = c.fetchall()
#                 else:
#                     c.execute(query)
#                     conn.commit()
#                     results = []
#
#         sections = self.convert_db_results_into_sections(results)
#
#         return sections
#
#
#     def get_sections_based_on_search_bar_query(self, queryTerm):
#         IDs = []
#         if queryTerm.startswith('tags:'):
#             lookupParts = ['tags']
#             queryTerm = queryTerm.replace('tags:', '')
#         elif queryTerm.startswith('section:'):
#             lookupParts = ['section']
#             queryTerm = queryTerm.replace('section:', '')
#         elif queryTerm.startswith('content:'):
#             lookupParts = ['content']
#             queryTerm = queryTerm.replace('content:', '')
#         elif queryTerm.startswith('id:'):
#             lookupParts = ['id']
#             queryTerm = queryTerm.replace('id:', '')
#         else:
#             lookupParts = ['section', 'tags', 'content']
#         if ',' not in queryTerm and '+' not in queryTerm:
#             with contextlib.closing(sqlite3.connect(self.db)) as conn:
#                 with contextlib.closing(conn.cursor()) as c:
#                     for part in lookupParts:
#                         if part == 'id':
#                             query = """
#                             SELECT id FROM knowledgebase 
#                             WHERE {}="{}"
#                             """.format(part, queryTerm)
#                         else:
#                             query = """
#                             SELECT id FROM knowledgebase 
#                             WHERE {} LIKE "%{}%"
#                             """.format(part, queryTerm)
#                         c.execute(query)
#                         results = c.fetchall()
#
#                         if results:
#                             IDs.extend([res[0] for res in results])
#         elif ',' in queryTerm:
#             terms = queryTerm.split(',')
#             terms = [t.strip(' ') for t in terms]
#             with contextlib.closing(sqlite3.connect(self.db)) as conn:
#                 with contextlib.closing(conn.cursor()) as c:
#                     foundTerms = dict()
#                     for part in lookupParts:
#                         for term in terms: 
#                             if part == 'id':
#                                 query = """
#                                 SELECT id FROM knowledgebase 
#                                 WHERE {}="{}"
#                                 """.format(part, term)
#                             else:
#                                 query = """
#                                 SELECT id FROM knowledgebase 
#                                 WHERE {} LIKE "%{}%"
#                                 """.format(part, term)
#                             c.execute(query)
#                             results = c.fetchall()
#
#                             if results:
#                                 for res in results:
#                                     ID = res[0]
#                                     if ID not in foundTerms.keys():
#                                         foundTerms[ID] = dict()
#                                     foundTerms[ID][term] = True
#             if foundTerms:
#                 for ID in foundTerms.keys():
#                     IDs.append(ID)
#         elif '+' in queryTerm:
#             terms = queryTerm.split('+')
#             terms = [t.strip(' ') for t in terms]
#             with contextlib.closing(sqlite3.connect(self.db)) as conn:
#                 with contextlib.closing(conn.cursor()) as c:
#                     foundTerms = dict()
#                     for part in lookupParts:
#                         for term in terms: 
#                             query = """
#                             SELECT id FROM knowledgebase 
#                             WHERE {} LIKE "%{}%"
#                             """.format(part, term)
#                             c.execute(query)
#                             results = c.fetchall()
#
#                             if results:
#                                 for res in results:
#                                     ID = res[0]
#                                     if ID not in foundTerms.keys():
#                                         foundTerms[ID] = dict()
#                                     foundTerms[ID][term] = True
#             if foundTerms:
#                 for ID in foundTerms.keys():
#                     numTems = sum([foundTerms[ID][t] for t in foundTerms[ID].keys()])
#                     if numTems == len(terms):
#                         IDs.append(ID)
#
#         sections = []
#         if IDs:
#             IDs = list(set(IDs))
#             sections = self.get_sections_based_on_IDs(IDs)
#
#         return sections
#
#
#     def get_sections_based_on_IDs(self, sectionsID):
#         if isinstance(sectionsID, list):
#             if len(sectionsID) > 1:
#                 sectionsID = ','.join([str(x) for x in sectionsID])
#             else:
#                 sectionsID = str(sectionsID[0])
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query = """
#                 SELECT * from knowledgebase 
#                 WHERE id in ({})
#                 """.format(sectionsID)
#
#                 c.execute(query)
#                 results = c.fetchall()
#
#         sections = self.convert_db_results_into_sections(results)
#
#         return sections
#
#
#     def export_md_content_by_id(self, sectionsIDs):
#         with contextlib.closing(sqlite3.connect(self.db)) as conn:
#             with contextlib.closing(conn.cursor()) as c:
#                 query="""
#                 SELECT section, content FROM knowledgebase 
#                 WHERE id IN ({vals})
#                 """.format(vals=','.join(['?']*len(sectionsIDs)))
#
#                 c.execute(query, sectionsIDs)
#                 results = c.fetchall()
#
#         try:
#             if results:
#                 with open('{}/markdown_export.md'.format(self.notebookDir), 'w') as outf:
#                     for section in results:
#                         title, content = section
#                         print('# {}'.format(title), file=outf)
#                         if '<r>' in content:
#                             content = content.replace('<r>', '\\textcolor{red}{').replace('</r>', '}')
#                         if '<g>' in content:
#                             content = content.replace('<g>', '\\textcolor{green}{').replace('</g>', '}')
#                         if '<o>' in content:
#                             content = content.replace('<o>', '\\textcolor{orange}{').replace('</o>', '}')
#                         print(content, file=outf)
#
#                         print('', file=outf)
#                         print('', file=outf)
#                 return 'DONE'
#             else:
#                 return 'EMPTY'
#         except Exception:
#             return 'ERROR'
#
