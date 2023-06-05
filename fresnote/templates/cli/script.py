import click
import logging
from pathlib import Path
from fresnote.main import app

@click.command(name="main", help="Start flask server to view projects notebooks.")
@click.option('--config', '-c', required=True, help='Config file to project details.')
@click.option('--port', '-p', default=5000, show_default=True, help='Port to run flask server.')
@click.option('--logger', is_flag=True, help='Flag for turning on logging.')
def main(config, port, logger):

    config = Path(config)
    if not config.exists():
        exit("Passed config filepath does not exist.")

    app.config['projects_config'] = config

    if logger:
        app.config['logging'] = True
        logging.basicConfig(filename='fresnote.log')
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    else:
        app.config['logging'] = False

    app.run(debug=True, port=port)

if __name__ == '__main__':
    main()
