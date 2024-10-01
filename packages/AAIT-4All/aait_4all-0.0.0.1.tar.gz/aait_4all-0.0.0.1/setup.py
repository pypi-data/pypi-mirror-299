from setuptools import setup
from setuptools.command.install import install
import os

# Nom du package PyPI ('pip install NAME')
NAME = "AAIT_4All"

# Version du package PyPI
VERSION = "0.0.0.1"  # la version doit être supérieure à la précédente sinon la publication sera refusée

# Facultatif / Adaptable à souhait
AUTHOR = "Community"
AUTHOR_EMAIL = ""
URL = ""
DESCRIPTION = "Installation de 4All"
LICENSE = ""

# Dépendances
INSTALL_REQUIRES = ["gpt4all-pypi-part11"]


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # You can run any command or script here
        print("Running post-install script...")

        # Example: Execute an external script
        py_path = os.path.join(sys.executable, "Lib", "site-packages", "orangecontrib", "AAIT", "utils", "concat_gpt4all.py")
        os.system(py_path)  # Replace with your script

        # Continue with the normal installation
        install.run(self)


setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      description=DESCRIPTION,
      license=LICENSE,
      install_requires=INSTALL_REQUIRES,
      cmdclass={"install": PostInstallCommand,},
      )
