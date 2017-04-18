from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
import os

class Templater():
    def __init__(self, path):
        self.env = Environment(
            loader = FileSystemLoader(os.path.join(path,'templates')),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def get_template(self, template_name, data_dict):
        template = self.env.get_template(template_name)
        return template.render(data_dict)
