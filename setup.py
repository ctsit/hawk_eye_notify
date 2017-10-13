
from setuptools import setup

#bring in __version__ from sourcecode
#per https://stackoverflow.com/a/17626524
#and https://stackoverflow.com/a/2073599

with open('hawk_eye_notify/version.py') as ver:
    exec(ver.read())

setup(name='hawk_eye_notify',
      version=__version__,
      description='Hawk_eye_notify watches a directory and sends alerts on change',
      url='https://github.com/ctsit/hawk_eye_notify',
      author='Matthew J. McConnell',
      author_email='devmattm@gmail.com',
      license='Apache License 2.0',
      packages=['hawk_eye_notify'],
      entry_points={
          'console_scripts': [
              'hawk_eye_notify = hawk_eye_notify.__main__:cli_run',
          ],
      },
      install_requires=['jinja2==2.9.6',
                        'pyinotify==0.9.6',
                        'docopt==0.6.2',
                        'pyyaml==3.12'],
      zip_safe=False)
