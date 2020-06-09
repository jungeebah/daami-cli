import click
import configparser
import os
import sys
import frontmatter

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

def all_files(folder_name:str):
    return [os.path.join(folder_name,x) for x in os.listdir(folder_name) 
                    if os.path.isfile(os.path.join(folder_name,x))]

def movie_present(movie_name:str, project_path: str):
    file_list = all_files(os.path.join(project_path,'_posts'))
    for file in file_list:
        with open(file) as f:
            movie_info = frontmatter.load(f)
            if movie_info['title'].lower() == movie_name.lower():
                return True
    return False

def does_contain(folder_name: str, required_folder: str):
    all_folder = [x for x in os.listdir(folder_name) 
                    if os.path.isdir(os.path.join(folder_name,x))]
    if required_folder in all_folder:
        return True
    return False

def check_setup():
    homde_dir = os.path.expanduser('~')
    if os.path.isfile(os.path.join(homde_dir,'.daamiReview')):
        return True
    return False

def folder_Present(dir_name):
    if os.path.isdir(dir_name):
        return True
    return False

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
@click.option('--language','-l', prompt=True,help='The language the movie is in')
@click.option('--time','-t',help='When the article is being written')

def review(title,movie,time,project,language):
    ''' Generates the review file in the _post folder of the project'''
    # check if setup file is there or not before proceeding
    if not check_setup():
        click.echo(click.style('Cannot find config file do run daami-cli setup', fg='red'))
        sys.exit(1)
    # get the project folder
    project_folder = get_project()
    api_key = get_api()
    # checks to make sure the project folder is present
    if not folder_Present(project_folder):
        click.echo(click.style('The project folder specified in setup is not present', fg='red'))
        sys.exit(1)
    # checks to make sure the project folder has _posts
    if not does_contain(project_folder,'_posts'):
        click.echo(click.style('The project folder doesn\'t look like a jekyll project', fg='red'))
        sys.exit(1)

    #read all other posts to check if that movie is present or not
    if movie_present(movie,project_folder):
        click.echo(click.style(f'The movie {movie} has already been reviewed', fg='red'))
        sys.exit(1)
