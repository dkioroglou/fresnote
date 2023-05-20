from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_from_directory, current_app
import json
from pathlib import Path
from fresnote.classes import Projects
from fresnote.classes import Notebook

sections = Blueprint('sections', __name__)


@sections.route('/add_new_section/<project>/<notebook>/<chapter>', methods=['POST'])
def add_new_section(project, notebook, chapter):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    try:
        newSectionID = notes.add_new_section(notebook, chapter)
    except Exception as error:
        return '', 400
    return str(newSectionID), 200


@sections.route('/<project>/save_chapter_sections_order', methods=['POST'])
def save_chapter_sections_order(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    notebook = data['notebook']
    chapter = data['chapter']
    sectionsOrder = data['sections']

    if '\n' in sectionsOrder:
        sectionsOrder = sectionsOrder.split('\n')
    else:
        sectionsOrder = [sectionsOrder.strip(' ')]

    sections = list()
    for sec in sectionsOrder:
        if sec:
            if '-' in sec:
                sections.append(int(sec.split('-')[0].strip(' ')))
            else:
                sections.append(int(sec.strip(' ')))

    sectionsExist = notes.check_sections_ids_exist(sections)
    if not sectionsExist:
        return 'IDs not found.<br>Make sure IDs exist.<br>Order not updated.', 400
    try:
        notes.save_chapter_sections_order(notebook, chapter, sections)
    except Exception:
        return 'Error while saving sections order.', 400
    return 'Sections order have updated.', 200


# @section.route('/<notebook>/save_section_title', methods=['POST'])
# def save_section_title_func(notebook):
#     notes = Notebook(notebook)
#     data = request.get_json()
#     sectionID = data['sectionID']
#     sectionTitle = data['sectionTitle']
#
#     try:
#         notes.save_section_title(sectionID, sectionTitle)
#     except Exception:
#         return '', 400
#     return '', 200
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/<notebook>/save_section_tags', methods=['POST'])
# def save_section_tags_func(notebook):
#     notes = Notebook(notebook)
#     data = request.get_json()
#     sectionID = data['sectionID']
#     sectionTags = data['sectionTags']
#
#     try:
#         notes.save_section_tags(sectionID, sectionTags)
#     except Exception:
#         return '', 400
#     return '', 200
#
#
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/<notebook>/tags/<ID>', methods=['GET'])
# def tags_func(notebook, ID):
#     notes = Notebook(notebook)
#     tags = notes.get_section_tags(ID)
#
#     return tags
#
#
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/<notebook>/content/<ID>', methods=['GET'])
# def content_func(notebook, ID):
#     notes = Notebook(notebook)
#     content = notes.get_section_content(ID)
#     return content
#
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/<notebook>/save_section_content', methods=['POST'])
# def save_section_content_func(notebook):
#     notes = Notebook(notebook)
#     data = request.get_json()
#     sectionID = data['sectionID']
#     sectionContent = data['sectionContent']
#     
#     try:
#         notes.save_section_content(sectionID, sectionContent)
#     except Exception:
#         return '', 400
#     return '', 200
#
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/add_new_section/<notebook>/<project>/<chapter>', methods=['POST'])
# def add_new_section_func(notebook, project, chapter):
#     notes = Notebook(notebook)
#     try:
#         newSectionID = notes.add_new_section(project, chapter)
#     except Exception as error:
#         print(error)
#         return '', 400
#     return str(newSectionID), 200
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/<notebook>/toggle_fold_state/<ID>', methods=['GET'])
# def toggle_fold_state_func(notebook, ID):
#     notes = Notebook(notebook)
#     notes.toggle_fold_state_of_section(ID)
#     return '', 204
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/<notebook>/delete_section/<ID>', methods=['GET'])
# def delete_section_func(notebook, ID):
#     notes = Notebook(notebook)
#     try:
#         notes.delete_section(ID)
#     except Exception:
#         return '', 400
#     # empty response
#     return '', 200
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# # This route is for serving protected static files
# @section.route('/protected/<path:filename>')
# def protected(filename):
#     return send_from_directory('protected', filename)
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @section.route('/<notebook>/<path:filename>', methods=['GET'])
# def docs_func(notebook, filename):
#     notes = Notebook(notebook)
#     filePath = os.path.join(notes.notebookDir, filename)
#     fileExtention = os.path.splitext(filename)[-1]
#     docExtensions = ['.docx', '.doc', '.xls', '.xlsx', '.csv', '.tsv', '.tex', '.bib']
#
#     if fileExtention and fileExtention in docExtensions:
#         if fileExtention == '.tex':
#             os.system("gnome-terminal -- bash -c \"cd {} && nvim {}\" ".format(os.path.dirname(filePath), filePath))
#         else:
#             os.system(f'xdg-open {filePath}')
#         return ('', 204)
#     else:
#         return send_from_directory(notes.notebookDir, filename)
#
#
# @section.route('/<notebook>/diagram/<path:filename>')
# def diagram(notebook, filename):
#     notes = Notebook(notebook)
#     filePath = '{}/{}'.format(notes.notebookDir, filename)
#
#     if not os.path.exists(filePath):
#         initialDiagram = { "class": "go.GraphLinksModel",
#                            "nodeKeyProperty": "id",
#                            "linkKeyProperty": "id",
#                            "nodeDataArray": [
#                                 { "id": 1, "loc": "120 120", "text": "Initial" }
#                            ],
#                            "linkDataArray": [
#                            ]
#                           }
#         with open(filePath, 'w') as outf:
#             json.dump(initialDiagram, outf)
#
#     return render_template('diagram_template.html', notebook=notebook, filename="/{}/{}".format(notebook, filename)) 
#
#
# @section.route('/<notebook>/tree_diagram/<path:filename>')
# def tree_diagram(notebook, filename):
#     notes = Notebook(notebook)
#     filePath = '{}/{}'.format(notes.notebookDir, filename)
#
#     if not os.path.exists(filePath):
#         initialDiagram = { "class": "go.GraphLinksModel",
#                            "nodeKeyProperty": "id",
#                            "linkKeyProperty": "id",
#                            "nodeDataArray": [
#                                 { "id": 1, "loc": "120 120", "text": "Initial" }
#                            ],
#                            "linkDataArray": [
#                            ]
#                           }
#         with open(filePath, 'w') as outf:
#             json.dump(initialDiagram, outf)
#
#     return render_template('tree_diagram_template.html', notebook=notebook, filename="/{}/{}".format(notebook, filename)) 
#
#
# @section.route('/<notebook>/regular_diagram/<path:filename>')
# def regular_diagram(notebook, filename):
#     notes = Notebook(notebook)
#     filePath = '{}/{}'.format(notes.notebookDir, filename)
#
#     if not os.path.exists(filePath):
#         initialDiagram = { "class": "go.GraphLinksModel",
#                            "nodeKeyProperty": "id",
#                            "linkKeyProperty": "id",
#                            "nodeDataArray": [
#                                 { "id": 1, "loc": "120 120", "text": "Initial" }
#                            ],
#                            "linkDataArray": [
#                            ]
#                           }
#         with open(filePath, 'w') as outf:
#             json.dump(initialDiagram, outf)
#
#     return render_template('regular_diagram_template.html', notebook=notebook, filename="/{}/{}".format(notebook, filename)) 
#
#
# @section.route('/<notebook>/store_diagram', methods=['POST'])
# def store_diagram(notebook):
#     notes = Notebook(notebook)
#     data = request.get_json()
#     filename = data['filename'].replace('/{}/'.format(notebook), '')
#     diagram = data['diagram']
#
#     # filename starts with '/' which was introduced in the javascript
#     filePath = '{}/{}'.format(notes.notebookDir, filename)
#
#     with open(filePath, 'w') as outf:
#         json.dump(diagram, outf)
#         
#     return '', 200
#
