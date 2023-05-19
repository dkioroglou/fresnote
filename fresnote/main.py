from flask import Flask

app = Flask(__name__)

from fresnote.routes.projects import projects
# from routes.notebook_route import notebook
# from routes.section_route import section
#
# # Register routes
app.register_blueprint(projects)
# app.register_blueprint(notebook)
# app.register_blueprint(section)
