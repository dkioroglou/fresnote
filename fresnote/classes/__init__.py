from pathlib import Path
import os
import contextlib
import sqlite3
import json
from collections import OrderedDict
from datetime import datetime
import configparser
from fresnote.classes.renderer import Renderer


class Projects:

    def __init__(self, configPath):
        self.configPath = configPath
        self.config = configparser.ConfigParser()
        self.config.read(self.configPath)
        self.projectsList = self.config.sections()

    def create_project(self, projectPath):
        projectPath = Path(projectPath)

        project = projectPath.name
        docsPath = projectPath.joinpath('docs')
        uploadsPath = projectPath.joinpath('uploads')
        sectionsPath = projectPath.joinpath('sections')

        projectPath.mkdir(parents=True)
        docsPath.mkdir(parents=True)
        uploadsPath.mkdir(parents=True)
        sectionsPath.mkdir(parents=True)
        dbPath = projectPath.joinpath('project.db')

        self.config[project] = {
                'path': projectPath,
                'docs': docsPath,
                'uploads': uploadsPath,
                'sections': sectionsPath,
                'db': dbPath
                }

        with open(self.configPath,"w") as outf:
            self.config.write(outf)

        with contextlib.closing(sqlite3.connect(dbPath)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                CREATE TABLE notebooks(
                id INTEGER PRIMARY KEY,
                notebook TEXT,
                chapter TEXT,
                sections TEXT,
                date TEXT
                )
                """

                c.execute(query)
                conn.commit()

                query = """
                CREATE TABLE sections(
                id INTEGER PRIMARY KEY,
                section TEXT,
                tags TEXT,
                content TEXT,
                folded INTEGER,
                date TEXT
                )
                """

                c.execute(query)
                conn.commit()


class Notebook:

    def __init__(self, project, config):
        self.config = configparser.ConfigParser()
        self.config.read(config)

        self.project = project
        self.projectPath     = Path(self.config.get(self.project, 'path'))
        self.projectDocs     = Path(self.config.get(self.project, 'docs'))
        self.projectUploads  = Path(self.config.get(self.project, 'uploads'))
        self.projectSections = Path(self.config.get(self.project, 'sections'))
        self.projectDB       = Path(self.config.get(self.project, 'db'))


    def get_all_notebooks_and_chapters_for_sidebar(self):
        """Gets all notebook names and chapters for project."""

        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                SELECT id, notebook, chapter from notebooks
                WHERE notebook IS NOT NULL
                """
                c.execute(query)
                results =  c.fetchall()

        sidebarData = OrderedDict()
        if results:
            for res in results:
                ID, notebook, chapter = res
                if not sidebarData.get(notebook, False):
                    sidebarData[notebook] = OrderedDict()
                    sidebarData[notebook]['chapters'] = list()
                    # Notebook takes the ID from the first chapter.
                    # This will make each notebook to have a unique ID in the sidebar.
                    sidebarData[notebook]['notebookID'] = ID

                sidebarData[notebook]['chapters'].append(chapter)

        if sidebarData:
            # Due to multiple sections, a chapter may repeat multiple times in the database.
            for notebook in sidebarData.keys():
                sidebarData[notebook]['chapters'] = list(set(sidebarData[notebook]['chapters']))
        return sidebarData


    def add_notebook(self, notebook):
        today = datetime.today().strftime('%Y-%m-%d')
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                INSERT INTO notebooks
                (notebook, chapter, sections, date)
                VALUES (?,?,?,?)
                """
                c.execute(query, (notebook, 'First chapter', json.dumps([]), today))
                conn.commit()


    def add_chapter(self, notebook, chapter):
        today = datetime.today().strftime('%Y-%m-%d')
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                INSERT INTO notebooks
                (notebook, chapter, sections, date)
                VALUES (?,?,?,?)
                """
                c.execute(query, (notebook, chapter, json.dumps([]), today))
                conn.commit()


    def change_notebook_title(self, previousNotebookTitle, newNotebookTitle):
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                UPDATE notebooks 
                SET notebook=(?) 
                WHERE notebook == (?)
                """

                c.execute(query, (newNotebookTitle, previousNotebookTitle))
                conn.commit()


    def change_chapter_title(self, notebook, previousChapterTitle, newChapterTitle):
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                UPDATE notebooks 
                SET chapter=(?) 
                WHERE chapter == (?) AND notebook == (?)
                """

                c.execute(query, (newChapterTitle, previousChapterTitle, notebook))
                conn.commit()


    def add_new_section(self, notebook, chapter):
        today = datetime.today().strftime('%Y-%m-%d')
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                INSERT INTO sections 
                (section, tags, content, folded, date)
                VALUES (?,?,?,?,?)
                """
                c.execute(query, ('New section', 'na', 'Section content', 0, today))
                sectionID = c.lastrowid
                conn.commit()

                query = """
                SELECT sections FROM notebooks 
                WHERE notebook == (?) AND chapter == (?)
                """
                c.execute(query, (notebook, chapter))
                sections = c.fetchone()[0]

                sections = json.loads(sections)
                sections.append(sectionID)

                query = """
                UPDATE notebooks 
                SET sections=(?) 
                WHERE notebook == (?) AND chapter == (?)
                """
                c.execute(query, (json.dumps(sections), notebook, chapter))
                conn.commit()

        return sectionID


    def check_sections_ids_exist(self, sectionsIDs):
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                SELECT COUNT(*) FROM sections 
                WHERE id IN ({}) 
                """.format(','.join([str(x) for x in sectionsIDs]))
                c.execute(query)
                result = c.fetchone()
        if not result:
            return False
        if result[0] != len(sectionsIDs):
            return False
        return True


    def save_chapter_sections_order(self, notebook, chapter, sections):
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                UPDATE notebooks 
                SET sections=(?) 
                WHERE notebook == (?) AND chapter == (?)
                """

                c.execute(query, (json.dumps(sections), notebook, chapter))
                conn.commit()


    def get_all_sections_for_chapter(self, notebook, chapter):
        with contextlib.closing(sqlite3.connect(self.projectDB)) as conn:
            with contextlib.closing(conn.cursor()) as c:
                query = """
                SELECT sections FROM notebooks 
                WHERE notebook=(?) AND chapter=(?)
                """
                c.execute(query, (notebook, chapter))
                sectionsIDs = c.fetchone()
                
                # Specifies also sections order
                if sectionsIDs:
                    sectionsIDs = json.loads(sectionsIDs[0])
                    query = """
                    SELECT * FROM sections 
                    WHERE id IN ({0})
                    """.format(', '.join('?' for _ in sectionsIDs))
                    c.execute(query, sectionsIDs)
                    sectionsResults = c.fetchall()
                else:
                    sectionsResults = []

        if sectionsResults:
            render = Renderer()
            sections = render.convert_db_results_into_sections(notebook,
                                                             chapter,
                                                             sectionsResults,
                                                             sectionsIDs,
                                                             self.projectDB)
        else:
            sections = []
        return sections


