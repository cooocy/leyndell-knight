import os.path

from config.loader import load_yaml_configurations

dir_name = os.path.dirname(__file__)
app_cfs = load_yaml_configurations(f'{dir_name}/app.yaml')
disk_cleaner_cfs = app_cfs['disk_cleaner']

__all__ = ['app_cfs', 'disk_cleaner_cfs']
