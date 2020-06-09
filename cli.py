import click
import configparser
import os

def get_info(key):
    homde_dir = os.path.expanduser('~')
    config = configparser.ConfigParser()
    config.read(os.path.join(homde_dir,'.daamiReview'))
    try:
        return config['info'][key]
    except:
        return 

def get_project():
    return get_info('project')

def get_api():
    return get_info('api')

@click.group(help='Will help to aid in creating files for daamireview')
def cli():
    pass

@cli.command()
@click.option('--project', '-p', prompt=True,
              default=get_project(), type=click.Path())
@click.option('--api_key', '-p', prompt=True,
              default=get_api(), help='Api key to do google search check the channel to get one')

def setup(project,api_key):
    '''Setup daami-cli to point to the given project'''
    homde_dir = os.path.expanduser('~')
    config = configparser.ConfigParser()
    config['info'] = {'project': project, 'api': api_key}
    with open(os.path.join(homde_dir,'.daamiReview'), 'w') as configfile:
        config.write(configfile)

@cli.command()
@click.option('--project', '-p',help='The location of the project')
@click.option('--title','-T', prompt=True, help='title of the article')
@click.option('--movie','-m', prompt=True,help='Name of the movie being reviewed')
@click.option('--time','-t',help='When the article is being written')
def review(title,movie,time,project):
    ''' Generates the review file in the _post folder of the project'''
    print('YUP')