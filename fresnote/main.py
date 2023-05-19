from flask import Flask

app = Flask(__name__)
# SECRET_KEY is necessary for the flash message that use the "session"
app.config['SECRET_KEY'] = '490FJLKWJE493'

from fresnote.routes.projects import projects
# from routes.notebook_route import notebook
# from routes.section_route import section
#
# # Register routes
app.register_blueprint(projects)
# app.register_blueprint(notebook)
# app.register_blueprint(section)
