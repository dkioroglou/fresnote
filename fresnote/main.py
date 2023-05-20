from flask import Flask

app = Flask(__name__)
# SECRET_KEY is necessary to flash messages that use the "session"
app.config['SECRET_KEY'] = '490FJLKWJE493'

from fresnote.routes.projects import projects
from fresnote.routes.sections import sections

# # Register routes
app.register_blueprint(projects)
app.register_blueprint(sections)
