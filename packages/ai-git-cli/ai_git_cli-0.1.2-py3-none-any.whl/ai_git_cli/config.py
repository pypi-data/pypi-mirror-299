import os
import yaml
from string import Template
import logging
from dotenv import load_dotenv

def load_config(config_path: str = 'configs/config.yaml') -> dict:
    load_dotenv()  # Load environment variables from .env file
    default_config = {
        'ai_provider': {
            'name': 'openai',
            'model': 'gpt-4',
            'api_key': os.getenv('OPENAI_API_KEY')
        },
        'commit_style': {
            'format': 'conventional',
            'conventional_prefixes': {
                'feat': 'Features',
                'fix': 'Bug Fixes',
                'docs': 'Documentation',
                'style': 'Code Style',
                'refactor': 'Code Refactoring',
                'test': 'Tests',
                'chore': 'Chores'
            },
            'length': 'short',
            'emoji': False,
            'temperature': 0.7
        },
        'grouping': {
            'max_files_per_commit': 5,
            'combine_similar_changes': True
        },
        'git': {
            'user_name': 'Your Name',
            'user_email': 'your.email@example.com'
        },
        'custom_instructions': {
            'grouping': "Group changes logically, focusing on related functionality.",
            'message_style': "Use concise, descriptive language. Start with a verb in imperative mood.",
            'user_feedback': ""
        }
    }
    
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        config = substitute_env_variables(config)
    except FileNotFoundError:
        print(f"Config file not found at {config_path}. Using default configuration.")
        config = default_config
    
    setup_logging(config)
    return config

def substitute_env_variables(config):
    if isinstance(config, dict):
        return {k: substitute_env_variables(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [substitute_env_variables(i) for i in config]
    elif isinstance(config, str):
        template = Template(config)
        try:
            return template.substitute(os.environ)
        except KeyError as e:
            raise ValueError(f"Missing environment variable for config: {e}")
    else:
        return config

def setup_logging(config):
    logging_config = config.get('logging', {})
    level = getattr(logging, logging_config.get('level', 'INFO').upper(), logging.INFO)
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    handlers = []
    if logging_config.get('file'):
        file_handler = logging.FileHandler(logging_config['file'])
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    if logging_config.get('enable_console', False):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(console_handler)
    
    if handlers:
        logging.basicConfig(level=level, handlers=handlers)
    else:
        logging.basicConfig(level=level, format=log_format)
