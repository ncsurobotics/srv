
from distutils.core import setup,Extension

setup(
    name='srv',
    version='0.1dev',
    author='Jacob Salzberg, Ben Fisher',
    author_email='bjfisher@ncsu.edu',
    description='Seawolf Router for Video library',

    py_modules=['srv', 'server', 'client', 'commands', 'nettools', 'source', 'srv_settings', 'StreamFinishedException', '__init__']
    #long_description=open('README.txt').read()
    #install_requires=['sys', 'cv2', 'socket', 'pickle', 'time']
    )
