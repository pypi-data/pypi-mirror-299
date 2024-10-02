import os
import logging

def substitute_env_variables(config):
    for key, value in config.items():
        if isinstance(value, dict):
            config[key] = substitute_env_variables(value)
        elif isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            config[key] = os.getenv(env_var, value)
    return config

def setup_logging(config):
    logging_config = config.get('logging', {})
    level = logging_config.get('level', 'INFO')
    file = logging_config.get('file', 'ai_git_commit.log')
    enable_console = logging_config.get('enable_console', True)

    logging.basicConfig(level=level, filename=file, filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger('').addHandler(console_handler)