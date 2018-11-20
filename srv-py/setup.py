from distutils.core import setup,Extension
from os import listdir
from os.path import isfile, join
from setuptools import find_packages

setup(
    name='srv',
    version='0.1dev',
    author='Jacob Salzberg, Ben Fisher',
    author_email='bjfisher@ncsu.edu',
    description='Seawolf Router for Video library',
    include_package_data=True,

    packages=find_packages()
    #py_modules=map(lambda x: "srv/" + f, ['srv', 'server', 'client', 'net_commands', 'nettools', 'source', 'srv_settings', 'StreamFinishedException', f for f in listdir("srv") if isfile(join("srv", f))])
    #long_description=open('README.txt').read()
    #install_requires=['sys', 'cv2', 'socket', 'pickle', 'time']
    )
