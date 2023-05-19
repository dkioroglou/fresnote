import click
from pathlib import Path
from fresnote.main import app

@click.command(name="main", help="Start flask server to view projects notebooks.")
@click.option('--config', '-c', required=True, help='Config file to project details.')
@click.option('--port', '-p', default=5000, show_default=True, help='Port to run flask server.')
def main(config, port):
    config = Path(config)
    if not config.exists():
        exit("Passed config filepath does not exist.")
    app.config['projects_config'] = config
    app.run(debug=True, port=port)

if __name__ == '__main__':
    main()
