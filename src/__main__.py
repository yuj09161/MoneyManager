import os
import locale
import subprocess


ENCODING = locale.getpreferredencoding()
PROGRAM_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'

# for zipapp & launcher support
if not os.path.isfile('requirements.txt'):
    REQUIREMENTS_PATH = PROGRAM_DIR + 'requirements.txt'
    INSTALLER_PATH = PROGRAM_DIR + 'installer.py'
else:
    REQUIREMENTS_PATH = 'requirements.txt'
    INSTALLER_PATH = 'installer.py'


def main():
    with open(REQUIREMENTS_PATH, 'r', encoding='utf-8') as file:
        requirements = file.read()
    requirements = [name for name in requirements.split('\n') if name]

    installed = subprocess.run(
        ['pip', 'list'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW, check=False
    )
    to_install = [
        package for i, package in enumerate(requirements)
        if not package + ' ' in installed.stdout.decode(ENCODING)
    ]
    if to_install:
        # call installer
        if not subprocess.run(
            ['py', INSTALLER_PATH, *to_install],
            creationflags=subprocess.CREATE_NEW_CONSOLE, check=False
        ).returncode:
            run()
    else:
        run()


# Codes to run
def run():
    # pylint: disable = redefined-outer-name, import-outside-toplevel
    import main  # noqa: E402
    main.main()


if __name__ == '__main__':
    main()
