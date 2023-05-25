from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
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
        if current_app.config['logging']:
            current_app.logger.error(error)
        flash('Error while creating project.', 'danger')
        return redirect(url_for("projects.index"))

    project = Path(projectPath).name
    flash('Project created successfully.', 'success')
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
                           sidebar=True,
                           search=False,
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
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while creating notebook.', 400

    return 'Notebook created.', 200


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
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while adding chapter.', 400
    return 'Chapter added successfully.', 200


@projects.route('/serve/<project>/<notebook>/<chapter>', methods=['GET', 'POST'])
def serve(project, notebook, chapter):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    if not notes.notebook_chapter_exist(notebook, chapter):
        flash('Notebook and chapter do not exist in database.', 'danger')
        return redirect(url_for("projects.load", project=project, notebook=None))

    sidebarData = notes.get_all_notebooks_and_chapters_for_sidebar()
    sections = notes.get_all_sections_for_chapter(notebook, chapter)

    return render_template('project.html', 
                           sidebar=True,
                           sidebarData=sidebarData,
                           project=project, 
                           notebook=notebook, 
                           chapter=chapter,
                           sections=sections)


@projects.route('/<project>/view/<sectionIDs>', methods=['GET', 'POST'])
def view(project, sectionIDs):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)

    if ',' in sectionIDs:
        sectionIDs = sectionIDs.split(',')
    else:
        sectionIDs = [sectionIDs]
    sectionIDs = [int(x) for x in sectionIDs]
    sections = notes.get_sections_based_on_IDs(sectionIDs)

    return render_template('project.html', 
                           sidebar=False,
                           search=False,
                           sidebarData=[],
                           project=project, 
                           notebook="", 
                           chapter="",
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
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while renaming notebook.', 400
    
    return 'Notebook renamed.', 200


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
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while renaming chapter.', 400
    
    return 'Chapter renamed.', 200


@projects.route('/upload_file/<project>/<notebook>/<chapter>', methods=['POST'])
def upload_file(project, notebook, chapter):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    pathToSave = Path(notes.projectUploads)

    try:
        for f in request.files.getlist('uploaded_files_for_project'):
            f.save(pathToSave.joinpath(f.filename))
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        flash('Error while uploading files.', 'danger')
        return redirect(url_for('projects.serve', project=project, notebook=notebook, chapter=chapter)) 

    flash('Files uploaded successfully', 'success')
    return redirect(url_for('projects.serve', project=project, notebook=notebook, chapter=chapter)) 


@projects.route('/<project>/delete_notebook_keep_sections/<notebook>', methods=['GET'])
def delete_notebook_keep_sections(project, notebook):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    try:
        notes.delete_notebook(notebook)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while deleting notebook.', 400
    return 'Notebook deleted.<br>Sections were kept.', 200


@projects.route('/<project>/delete_notebook_and_sections/<notebook>', methods=['GET'])
def delete_notebook_and_sections(project, notebook):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    sectionIDs = notes.get_all_sections_ids_for_notebook(notebook)
    try:
        notes.delete_notebook(notebook)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while deleting notebook.', 400
    if sectionIDs:
        for ID in sectionIDs:
            try:
                notes.delete_section(ID)
            except Exception as error:
                if current_app.config['logging']:
                    current_app.logger.error(error)
                return f'Error while deleting section: {ID}.', 400
    return 'Notebook and sections deleted.', 200


@projects.route('/<project>/delete_chapter_keep_sections/<notebook>/<chapter>', methods=['GET'])
def delete_chapter_keep_sections(project, notebook, chapter):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    try:
        notes.delete_chapter_from_notebook(notebook, chapter)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while deleting chapter.', 400
    return 'Chapter deleted.<br>Sections were kept.', 200


@projects.route('/<project>/delete_chapter_and_sections/notebook/chapter', methods=['GET'])
def delete_chapter_and_sections(project, notebook, chapter):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    sectionIDs = notes.get_all_sections_ids_for_chapter(notebook, chapter)
    try:
        notes.delete_chapter_from_notebook(notebook, chapter)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while deleting notebook.', 400
    if sectionIDs:
        for ID in sectionIDs:
            try:
                notes.delete_section(ID)
            except Exception as error:
                if current_app.config['logging']:
                    current_app.logger.error(error)
                return f'Error while deleting section: {ID}.', 400
    return 'Chapter and sections deleted.', 200


@projects.route('/<project>/<directory>/<path:filename>', methods=['GET'])
def get_path(project, directory, filename):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    filePath = Path(notes.config.get(notes.project, directory))
    # fileExtention = os.path.splitext(filename)[-1]
    # docExtensions = ['.docx', '.doc', '.xls', '.xlsx', '.csv', '.tsv', '.tex', '.bib']
    #
    # if fileExtention and fileExtention in docExtensions:
    #     if fileExtention == '.tex':
    #         os.system("gnome-terminal -- bash -c \"cd {} && nvim {}\" ".format(os.path.dirname(filePath), filePath))
    #     else:
    #         os.system(f'xdg-open {filePath}')
    #     return ('', 204)
    # else:
    #     return send_from_directory(notes.notebookDir, filename)
    return send_from_directory(filePath, filename)


@projects.route('/<project>/search', defaults={'sectionIDs': None}, methods=['GET', 'POST'])
@projects.route('/<project>/search/<sectionIDs>', methods=['GET', 'POST'])
def search(project, sectionIDs):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)

    sidebarData = notes.get_all_notebooks_and_chapters_for_sidebar()

    if request.method == "GET" and not sectionIDs:
        return render_template('project.html', 
                               sidebar=True,
                               search=True,
                               sidebarData=sidebarData,
                               project=project, 
                               notebook=None, 
                               chapter=None,
                               sections=[])
    elif request.method == 'POST' and not sectionIDs:
        data = request.get_json()
        query = data['query']
        sections = notes.get_sections_based_on_search_bar_query(query)
        if sections:
            return ",".join([str(sec['ID']) for sec in sections]), 200
        else:
            return "No sections found.", 400
    else:
        if ',' in sectionIDs:
            sectionIDs  = [int(x) for x in sectionIDs.split(",")]
        else:
            sectionIDs = [int(sectionIDs)]
        sections = notes.get_sections_based_on_IDs(sectionIDs)
        return render_template('project.html', 
                               sidebar=True,
                               search=True,
                               sidebarData=sidebarData,
                               project=project, 
                               notebook=None, 
                               chapter=None,
                               sections=sections)


@projects.route('/<project>/highlight/<directory>/<path:filename>', methods=['GET'])
def highlight_script(project, directory, filename):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    filePath = Path(notes.config.get(notes.project, directory)).joinpath(filename)
    scriptCode = open(filePath).read()
    return render_template('highlight_script_code.html', sidebar=False, sidebarData=[], scriptcode=scriptCode, project=project, filePath=filePath) 


@projects.route('/<project>/table/<directory>/<path:filename>/<delimiter>', methods=['GET'])
def view_table(project, directory, filename, delimiter):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)

    if delimiter == 'tab':
        delimiter = '\t'
    elif delimiter == 'comma':
        delimiter = ','
    elif delimiter == 'space':
        delimiter = ' '

    filePath = Path(notes.config.get(notes.project, directory)).joinpath(filename)
    contents = open(filePath, 'r').read().splitlines()
    columns = contents[0].split(delimiter)
    rows = [r.split(delimiter) for r in contents[1:] if r]
    return render_template('table_grid.html', project=project, tablePath=filePath, columns=columns, rows=rows)
