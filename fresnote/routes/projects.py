from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from pathlib import Path
from fresnote.classes import Projects
from fresnote.classes import Notebook

projects = Blueprint('projects', __name__)

"""
NOTES: 
     When calling a route with javascript, the flask redirect is not working.
     Do a redirect whithin the javascript function.
"""

@projects.route('/', methods=['GET'])
def index():
    config = current_app.config['projects_config']
    projects = Projects(config)
    return render_template('index.html', data={'projects': projects.projectsList})


@projects.route('/create', methods=['POST'])
def create():
    config = current_app.config['projects_config']
    projects = Projects(config)

    projectPath = request.form.get("newProjectPath")
    if Path(projectPath).exists():
        flash('Project path already exists.', 'danger')
        return redirect(url_for("projects.index"))

    try:
        projects.create_project(projectPath)
    except Exception as error:
        print(error)
        flash('Error while creating project.', 'danger')
        return redirect(url_for("projects.index"))

    project = Path(projectPath).name
    return redirect(url_for("projects.load", project=project))


@projects.route('/select', methods=['POST'])
def select():
    project = request.form.getlist('project')[0]
    return redirect(url_for('projects.load', project=project))


@projects.route('/load/<project>', defaults={'notebook': None}, methods=['GET'])
@projects.route('/load/<project>/<notebook>', methods=['GET'])
def load(project, notebook):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    sidebarData = notes.get_all_notebooks_and_chapters_for_sidebar()
    return render_template('project.html', 
                           sidebarData=sidebarData,
                           project=project, 
                           notebook=notebook, 
                           chapter=None,
                           sections=[])



@projects.route('/<project>/add_notebook', methods=['POST'])
def add_notebook(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    notebook = data['notebook']

    try:
        notes.add_notebook(notebook)
    except Exception:
        return '', 400

    return '', 200


@projects.route('/<project>/add_chapter', methods=['POST'])
def add_chapter(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    notebook = data['notebook']
    chapter = data['chapter']

    try:
        notes.add_chapter(notebook, chapter)
    except Exception as error:
        return '', 400
    return '', 200


@projects.route('/serve/<project>/<notebook>/<chapter>', methods=['GET', 'POST'])
def serve(project, notebook, chapter):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    sidebarData = notes.get_all_notebooks_and_chapters_for_sidebar()
    sections = notes.get_all_sections_for_chapter(notebook, chapter)

    return render_template('project.html', 
                           sidebarData=sidebarData,
                           project=project, 
                           notebook=notebook, 
                           chapter=chapter,
                           sections=sections)


@projects.route('/<project>/change_notebook_title', methods=['POST'])
def change_notebook_title(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    previousNotebookTitle = data['previousNotebookTitle']
    newNotebookTitle = data['newNotebookTitle']

    try:
        notes.change_notebook_title(previousNotebookTitle, newNotebookTitle)
    except Exception as error:
        return '', 400
    
    return '', 200


@projects.route('/<project>/change_chapter_title', methods=['POST'])
def change_chapter_title(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    previousChapterTitle = data['previousChapterTitle']
    newChapterTitle = data['newChapterTitle']
    notebook = data['notebook']

    try:
        notes.change_chapter_title(notebook, previousChapterTitle, newChapterTitle)
    except Exception:
        return '', 400
    
    return '', 200


@projects.route('/<project>/search', methods=['GET', 'POST'])
def search(project):
    return "This is search bar"


# @project.route('/<project>/search', methods=['GET', 'POST'])
# def search_func(project):
#     notes = project(project)
#
#     if request.method == 'POST':
#         query = request.form.get("searchBarQuery")
#         sections = notes.get_sections_based_on_search_bar_query(query)
#
#         sidebarData = notes.get_all_projects_and_chapters_for_sidebar()
#
#         if sections:
#             return render_template('search_bar.html', data={'sidebarData':sidebarData, 'sections':sections}, project=project)
#         else:
#             flash('No sections found', 'danger')
#             return render_template('search_bar.html', data={'sidebarData':sidebarData, 'sections':[]}, project=project)
#     else:
#         sidebarData = notes.get_all_projects_and_chapters_for_sidebar()
#
#         sections = []
#         if sections:
#             return render_template('search_bar.html', data={'sidebarData':sidebarData, 'sections':sections}, project=project)
#         else:
#             return render_template('search_bar.html', data={'sidebarData':sidebarData, 'sections':[]}, project=project)
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @project.route('/<project>/view_sections/<sectionsID>', methods=['GET'])
# def view_sections(project, sectionsID):
#     notes = project(project)
#     sidebarData = notes.get_all_projects_and_chapters_for_sidebar()
#     sections = notes.get_sections_based_on_IDs(sectionsID)
#
#     if sections:
#         return render_template('view_sections.html', data={'sidebarData':sidebarData, 'sections':sections}, project=project)
#     else:
#         flash('No sections found', 'danger')
#         return render_template('view_sections.html', data={'sidebarData':sidebarData, 'sections':[]}, project=project)
#
#

@projects.route('/upload_file/<project>', methods=['POST'])
def upload_file(project):
    return "Upload file to project"

# @project.route('/upload_file/<project>/<project>/<chapter>', methods=['POST'])
# def upload_file_func(project, project, chapter):
#     notes = project(project)
#     pathToSave = os.path.join(notes.docsDir, 'uploads')
#
#     try:
#         for f in request.files.getlist('uploaded_files_for_project'):
#             f.save(os.path.join(pathToSave, f.filename))
#     except Exception as error:
#         flash('Error while uploading files.', 'danger')
#         return redirect(url_for('project.serve_project_func', project=project, project=project, chapter=chapter)) 
#
#     flash('Files uploaded successfully', 'success')
#     return redirect(url_for('project.serve_project_func', project=project, project=project, chapter=chapter)) 
#
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @project.route('/<project>/view_table/<path:filename>/<delimiter>', methods=['GET'])
# def view_table(project, filename, delimiter):
#     print(filename)
#     notes = project(project)
#     if not delimiter:
#         delimiter = 'tab'
#
#     if delimiter == 'tab':
#         delimiter = '\t'
#     elif delimiter == 'comma':
#         delimiter = ','
#     elif delimiter == 'space':
#         delimiter = ' '
#
#     filePath = '{}/{}'.format(notes.projectDir, filename)
#     contents = open(filePath, 'r').read().splitlines()
#     columns = contents[0].split(delimiter)
#     rows = [r.split(delimiter) for r in contents[1:]]
#     return render_template('table_grid.html', columns=columns, rows=rows)
#
#
#
# """
# NOTES:
#     STAYS - CHANGED
# """
# @project.route('/<project>/highlight/<path:filename>', methods=['GET'])
# def highlight_script(project, filename):
#     notes = project(project)
#     sidebarData = notes.get_all_projects_and_chapters_for_sidebar()
#     filePath = '{}/{}'.format(notes.projectDir, filename)
#     scriptCode = open(filePath).read()
#     return render_template('highlight_script_code.html', data={'sidebarData':sidebarData, 'sections':[]}, scriptcode=scriptCode, project=project) 
#
#
# @project.route('/<project>/delete_chapter_keep_sections/<projectName>/<chapterName>', methods=['GET'])
# def delete_chapter_keep_sections(project, projectName, chapterName):
#     notes = project(project)
#     try:
#         notes.delete_chapter_from_project(projectName, chapterName)
#     except Exception:
#         return '', 400
#     return '', 200
#
#
# @project.route('/<project>/delete_chapter_and_sections/<projectName>/<chapterName>', methods=['GET'])
# def delete_chapter_and_sections(project, projectName, chapterName):
#     notes = project(project)
#     sectionIDs = notes.get_all_sections_ids_for_chapter(projectName, chapterName)
#     try:
#         notes.delete_chapter_from_project(projectName, chapterName)
#         for ID in sectionIDs:
#             notes.delete_section(ID)
#     except Exception:
#         return '', 400
#     return '', 200
#
#
# @project.route('/<project>/delete_project_keep_sections/<projectName>', methods=['GET'])
# def delete_project_keep_sections(project, projectName):
#     notes = project(project)
#     try:
#         notes.delete_project(projectName, chapterName)
#     except Exception:
#         return '', 400
#     return '', 200
#
#
# @project.route('/<project>/delete_project_and_sections/<projectName>', methods=['GET'])
# def delete_project_and_sections(project, projectName):
#     notes = project(project)
#     sectionIDs = notes.get_all_sections_ids_for_project(projectName)
#     try:
#         notes.delete_project(projectName)
#         for ID in sectionIDs:
#             notes.delete_section(ID)
#     except Exception:
#         return '', 400
#     return '', 200
