import requests, yaml, os
from datetime import datetime


def parse_main_arguments(arguments):
    config = {}
    if arguments and len(arguments) > 1:
        for arg in arguments[1:]:
            args = arg.split("=")
            config[args[0][2:]] = args[1]
    return config


def is_path_existed(path):
    return os.path.exists(path)


def read_file(file_path, is_yml, is_url=False, lines=False):
    # Read input file in .yml format, either the yml_path is a URL or or local path
    content = None
    if file_path:
        if is_url:
            resp = requests.get(file_path)
            if str(resp.status_code) == '200':
                content = yaml.load(resp.content) if is_yml else resp.content
        else:
            if is_path_existed(file_path):
                with open(file_path, "r") as value:
                    content = yaml.load(value) if is_yml else value.read()
        if lines and content:
            content = content.split("\n")
    return content


def prepare_field(arg, arguments, default=None):
    if arg in arguments and arguments.get(arg):
        return arguments.pop(arg)
    return default


def get_current_time():
    return str(datetime.now())[:-7]
