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
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while adding section to database.', 400

    # function returns False if directory exists, otherwise it returns True 
    if not notes.create_new_section_directory(str(newSectionID)):
        return f'Section directory {newSectionID} exists.', 400
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
    if sectionsOrder:
        try:
            for sec in sectionsOrder:
                if sec:
                    if '-' in sec:
                        sections.append(int(sec.split('-')[0].strip(' ')))
                    else:
                        sections.append(int(sec.strip(' ')))
        except Exception as error:
            if current_app.config['logging']:
                current_app.logger.error(error)
            return 'Error while parsing section IDs.', 400

        sectionsExist = notes.check_sections_ids_exist(sections)
        if not sectionsExist:
            return 'IDs not found.<br>Make sure IDs exist.<br>Order not updated.', 400
    try:
        notes.save_chapter_sections_order(notebook, chapter, sections)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while saving sections order.', 400
    return 'Sections order have updated.', 200


@sections.route('/<project>/save_section_title', methods=['POST'])
def save_section_title(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    sectionID = data['sectionID']
    sectionTitle = data['sectionTitle']

    try:
        notes.save_section_title(sectionID, sectionTitle)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while saving section title.', 400
    return 'Section title saved.', 200

@sections.route('/<project>/toggle_fold_state/<ID>', methods=['GET'])
def toggle_fold_state(project, ID):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    notes.toggle_fold_state_of_section(ID)
    return '', 200


@sections.route('/<project>/delete_section/<ID>', methods=['GET'])
def delete_section(project, ID):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    try:
        notes.delete_section(ID)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while deteting section from database.', 400
    # function return False if deleting fails otherwise it returns True
    if not notes.delete_section_directory(ID):
        return 'Error while deleting section directory.', 400
    return 'Section deleted.', 200


@sections.route('/<project>/get_tags/<ID>', methods=['GET'])
def get_tags(project, ID):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    try:
        tags = notes.get_section_tags(ID)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error getting tags.'
    return tags


@sections.route('/<project>/save_section_tags', methods=['POST'])
def save_section_tags(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    sectionID = data['sectionID']
    sectionTags = data['sectionTags']
    try:
        notes.save_section_tags(sectionID, sectionTags)
    except Exception:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return 'Error while saving tags.', 400
    return 'Tags saved.', 200


@sections.route('/<project>/get_content/<ID>', methods=['GET'])
def get_content(project, ID):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    try:
        content = notes.get_section_content(ID)
    except Exception as error:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return '', 400
    return content


@sections.route('/<project>/save_section_content', methods=['POST'])
def save_section_content(project):
    config = current_app.config['projects_config']
    notes = Notebook(project, config)
    data = request.get_json()
    sectionID = data['sectionID']
    sectionContent = data['sectionContent']
    try:
        notes.save_section_content(sectionID, sectionContent)
    except Exception:
        if current_app.config['logging']:
            current_app.logger.error(error)
        return '', 400
    return '', 200

