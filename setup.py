#!/usr/bin/env python
"""The setup script for the ``prettyplots`` library.
"""



#####################################
## Load libraries/packages/modules ##
#####################################

# To get version of Python, to extract command line arguments, and to exit
# script abruptly if necessary.
import sys

# For directory operations, e.g. to check if a directory exists.
import os

# To run git commands and retrieve corresponding output.
import subprocess



# For setting up prettyplots package.
from setuptools import setup, find_packages, Command



############################
## Authorship information ##
############################

__author__     = "Matthew Fitzpatrick"
__copyright__  = "Copyright 2019"
__credits__    = ["Matthew Fitzpatrick"]
__maintainer__ = "Matthew Fitzpatrick"
__email__      = "mrfitzpa@sfu.ca"
__status__     = "Development"



####################################
## Define functions and constants ##
####################################

major_python_revision = 3
minimum_minor_python_revision = 0
minimum_python_version = (major_python_revision, minimum_minor_python_revision)

if not sys.version_info >= minimum_python_version:
    print("ERROR: prettyplots requires Python version >= ",
          major_python_revision, ".", minimum_minor_python_revision,
          ", the script got called by:\n", sys.version, ".", sep="")
    sys.exit(1)


    
# Hard-codd version for people without git. Current non-production version.
MAJOR = 0
MINOR = 1
MICRO = 0
RELEASED = False
VERSION = '{0:d}.{1:d}.{2:d}'.format(MAJOR, MINOR, MICRO)



def get_git_revision():
    """Get revision hash of ``prettyplots`` from git.

    Parameters
    ----------

    Returns
    -------
    revision : `str`
        Git revision hash of ``prettyplots``.
    """
    if not os.path.exists('.git'):
        revision = "unknown"
    else:
        try:
            parsed_cmd = ['git', 'rev-parse', 'HEAD']
            cwd = os.path.dirname(os.path.abspath(__file__))
            stderr = subprocess.STDOUT

            cmd_output = subprocess.check_output(parsed_cmd,
                                                 cwd=cwd,
                                                 stderr=stderr)
            revision = cmd_output.decode().strip()
            
        except:
            revision = "unknown"
            
    return revision



def get_version_info():
    """Get version of ``prettyplots`` from git.

    Parameters
    ----------

    Returns
    -------
    full_version : `str`
        Full version of ``prettyplots``.
    """
    full_version = VERSION
    git_revision = get_git_revision()
    
    if not RELEASED:
        full_version += '.dev0+' + git_revision[:7]
    return full_version, git_revision



def write__version_py(full_version,
                      git_revision,
                      filename="prettyplots/_version.py"):
    """Write the version during compilation to file.

    Parameters
    ----------
    full_version : `str`
        Full of version of ``prettyplots``.
    git_revision : `str`
        Git revision hash of ``prettyplots``.
    filename : `str`, optional
        Filename of file containing information about the version of ``prettyplots``
        currently being compiled.

    Returns
    -------
    """
    content = ("#!/usr/bin/env python\n"
               + "# This file was generated from setup.py. It contains "
               + "information about the\n# version of prettyplots currently "
               + "installed on machine.\n\n\n\n"
               + "############################\n"
               + "## Authorship information ##\n"
               + "############################\n\n"
               + "__author__     = \"Matthew Fitzpatrick\"\n"
               + "__copyright__  = \"Copyright 2019\"\n"
               + "__credits__    = [\"Matthew Fitzpatrick\"]\n"
               + "__maintainer__ = \"Matthew Fitzpatrick\"\n"
               + "__email__      = \"mrfitzpa@sfu.ca\"\n"
               + "__status__     = \"Development\"\n\n\n\n"
               + "#########################\n"
               + "## Version information ##\n"
               + "#########################\n\n"
               + "version = '{version!s}'\n"
               + "short_version = 'v' + version\n"
               + "released = {released!s}\n"
               + "full_version = '{full_version!s}'\n"
               + "git_revision = '{git_revision!s}'\n")
        
    content = content.format(version=VERSION,
                             full_version=full_version,
                             released=RELEASED,
                             git_revision=git_revision)

    with open(filename, 'w') as file_obj:
        print(filename)
        file_obj.write(content)

    return None



def read_requirements_file(filename):
    """Read requirements file and extract a set of library requirements.

    Parameters
    ----------
    filename : `str`
        Filename of requirements file.

    Returns
    -------
    requirements : array_like(`str`, ndim=1)
        Extracted set of library requirements.
    """
    with open(filename, 'r') as file_obj:
        requirements = file_obj.readlines()

    requirements = [line.strip() for line in requirements if line.strip()]
        
    return requirements


def read_extra_requirements():
    """Extract set of extra library requirements from the requirement files.

    Parameters
    ----------

    Returns
    -------
    extra_requirements : `dict` [`str`, array_like(`str`, ndim=1)]
        Extracted set of library requirements.
    """
    extra_requirements = {'doc': read_requirements_file('requirements-doc.txt')}
    extra_requirements['all'] = [requirement for requirement_subset
                                 in extra_requirements.values()
                                 for requirement in requirement_subset]
    
    return extra_requirements



class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system("rm -vrf ./build ./dist ./*.pyc "
                  "./*.tgz ./*.egg-info ./ostfic/_version.py")



def setup_package():
    """Setup ``prettyplots`` package.

    Parameters
    ----------

    Returns
    -------
    """
    # Change directory to root path of the repository.
    src_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(src_path)

    full_version, git_revision = get_version_info()
    write__version_py(full_version, git_revision)

    extras_require = read_extra_requirements()

    setup_requires = ['setuptools']

    description = ("For creating plots in accordance to the tastes of the "
                   "author.")

    setup(name="prettyplots",
          description=description,
          author="Matthew Fitzpatrick",
          author_email="mrfitzpa@sfu.ca",
          packages=find_packages(),
          version=full_version,
          setup_requires=setup_requires,
          install_requires=read_requirements_file('requirements.txt'),
          extras_require=extras_require,
          cmdclass={'clean': CleanCommand})


    
if __name__ == "__main__":
    setup_package()
