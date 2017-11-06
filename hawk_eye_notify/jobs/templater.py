from jinja2 import Environment, FileSystemLoader, select_autoescape
from yaml_reader import get_config
import os

"""
Templater requires a dict setting called 'templater' which contains a
product_template_map dict and a template_location setting
"""
_template_settings = 'templater'
_template_location = 'template_location'
_map_conf = 'product_template_map'

_fail_template = 'failed_v1'

def get_template(data_dict, config_file_path):
    print("Templace config_file_path: " ,config_file_path)
    config = get_config(config_file_path, _template_settings)
    env = Environment(
        loader = FileSystemLoader(os.path.abspath(config[_template_location])),
        autoescape=select_autoescape(['html', 'xml']))
    source = get_template_source(data_dict.get('source', _fail_template),config)
    template = env.get_template(source)
    print("Template found: ", template.name)
    return template.render(data_dict)

def get_template_source(source, config):
    #magic ints
    src = 0
    ver = 1

    #source is in name_version format
    source_ver = source.split('_')
    template_name = config[_map_conf].get(source_ver[src], {}).get(source_ver[ver], None)
    return template_name
