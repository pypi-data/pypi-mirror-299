from os.path import join, exists
from os import makedirs, getcwd
from bomiot.settings import APP_DEBUG
import subprocess

def init(folder):
    """
    init workspace
    :param folder:
    :return:
    """
    # execute path
    execute_path = getcwd()
    folder_path = join(execute_path, folder)

    cmd = "bomiot makemigrations"
    subprocess.run(cmd, shell=True)

    # make dir of logs
    # logs_folder = join(folder_path, LOGS_FOLDER)
    # exists(logs_folder) or makedirs(logs_folder)
    print('Initialized workspace %s' % folder)
