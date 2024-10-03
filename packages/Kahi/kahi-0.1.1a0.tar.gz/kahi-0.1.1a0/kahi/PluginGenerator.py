from kahi import templates
from shutil import copytree, move, rmtree
import pathlib
import os


class PluginGenerator:
    """
    Class to generate a kahi plugin from the template.
    The generated plugin is a python package ready to install with pip and it can be deployed in pipy.
    """

    def __init__(self, name: str, prefix: str = "Kahi"):
        """
        Initializes the class with a given name and prefix. The default prefix is "Kahi".

        Parameters:
        ____________
        name:str
            plugin name for the new project
        prefix:str
            prefix for the generated project, default is Kahi
        """
        self.name = name
        self.tname = "template"
        self.prefix = prefix
        self.template_path = os.path.join(
            str(pathlib.Path(templates.__file__).parent.absolute()), "plugin")
        self.template_path = os.path.join(
            self.template_path, "Kahi_template")

    def replace(self, filename, old, new):
        """
        Replaces all occurrences of old with new in a given file.

        Parameters:
        ____________
        filename:str
            filename to replace the string
        old:str
            string to be replaced
        new:str
            new string to write
        """
        content = ""
        with open(filename, "r") as file:
            content = file.read()
            content = content.replace(old, new)
            file.close()
        with open(filename, "w") as file:
            file.write(str(content))
            file.close()

    def generate(self, path: str = os.getcwd()):
        """
        Generates the plugin in a given path. Copies the template to the output path,
        renames the package folder, and replaces the template name with the plugin name in the README.md,
        setup.py, and MANIFEST.in files.

        Parameters:
        ____________
        path:str
            path to save the plugin project.
        """
        output_path = os.path.join(os.getcwd(), f"{self.prefix}_{self.name}")
        readme = os.path.join(output_path, "README.md")
        setup = os.path.join(output_path, "setup.py")
        manifest = os.path.join(output_path, "MANIFEST.in")
        package_folder_old = os.path.join(output_path, "kahi_template")
        package_folder_new = os.path.join(
            output_path, f"{self.prefix}_{self.name}".lower())
        package_file_old = os.path.join(
            package_folder_new, f"{self.prefix}_{self.tname}.py")
        package_file_new = os.path.join(
            package_folder_new, f"{self.prefix}_{self.name}.py")

        copytree(self.template_path, output_path)
        move(package_folder_old, package_folder_new)

        rmtree(os.path.join(output_path, "__pycache__"), ignore_errors=True)
        rmtree(os.path.join(package_folder_new,
               "__pycache__"), ignore_errors=True)

        os.rename(package_file_old, package_file_new)

        self.replace(package_file_new, self.tname, self.name)
        self.replace(readme, self.tname, self.name)
        self.replace(setup, self.tname, self.name)
        self.replace(manifest, self.tname, self.name)
