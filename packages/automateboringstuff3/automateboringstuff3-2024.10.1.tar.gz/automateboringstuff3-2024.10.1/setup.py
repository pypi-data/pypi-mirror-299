import io
import os
import re
from setuptools import setup, find_packages

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open("src/automateboringstuff3/__init__.py", "r") as fileObj:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    ).group(1)

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fileObj:
    long_description = fileObj.read()

setup(
    name='automateboringstuff3',
    version=version,
    url='https://github.com/asweigart/automateboringstuff3',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('This package installs the modules used in "Automate the Boring Stuff with Python", 3rd Edition.'),
    long_description=long_description,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license='BSD',
    install_requires=[
        #'imapclient==2.3.1', # Removed from 3rd edition, not updated since Jul 2022
        #'pyzmail36==1.0.4', # Removed from 3rd edition
        #'twilio', # Removed from 3rd edition since SMS texting has become much more complicated.
        'beautifulsoup4==4.12.3',
        'matplotlib==3.9.2',
        'openpyxl==3.1.5',
        'pdfminer.six==20240706',
        'pillow==10.4.0', # 9.0.0 dropped support for 3.6
        'playsound==1.3.0',
        'playwright==1.47.0',
        'PyPDF==5.0.1',
        'python-docx==1.1.2', # not updated since May 2021
        'pyttsx3==2.98',
        'PyYAML==6.0.2',
        'requests==2.32.3',
        'selenium==4.25.0',
        'tomli_w==1.0.0',
        'xmltodict==0.13.0',

        # These are note included since they are rather large:
        #'pytesseract==0.3.10',
        #'numpy<2',  # Version prior to Numpy 2 required for openai-whisper.
        #'openai-whisper==20231117',

        # These modules always have the latest version installed.
        'bext',
        'ezgmail',
        'ezsheets',
        'humre',
        'pyautogui',
        'pymsgbox',
        'pyperclip',
        'pyperclipimg',
        'yt-dlp',

    ],
    keywords="automate boring stuff python",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

    ],
)

