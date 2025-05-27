
import subprocess
import os




def open_file(filename):
    directory = '/Users/parsashemirani/main/firstmacbase'
    file_path = os.path.join(directory, filename)
    subprocess.run(['open', file_path])