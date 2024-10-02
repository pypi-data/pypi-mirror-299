from typing import List, Dict
from ai_git_cli.ai_client import get_ai_client
from ai_git_cli.config import load_config
from ai_git_cli.prompts import create_commit_message_prompt
import json

# // Test

def generate_commit_message(groups: List[List[Dict]], config: Dict) -> List[Dict]:
    ai_client = get_ai_client(config)
    temperature = config['commit_style'].get('temperature', 0.7)
    user_feedback = config['custom_instructions'].get('user_feedback', "")
    commit_style = config['commit_style']
    commit_messages = []

    for group in groups:
        prompt = create_commit_message_prompt(group, user_feedback, commit_style)
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates Git commit messages in JSON format."},
            {"role": "user", "content": prompt}
        ]
        response = ai_client.get_response(messages, temperature=temperature)
        
        try:
            commit_data = json.loads(response.strip())
            message = f"{commit_data['type']}: {commit_data['subject']}"
        except json.JSONDecodeError:
            # Fallback if AI does not return valid JSON
            message = response.strip().replace('```json\n', '').replace('\n```', '')
            if message.startswith('{') and message.endswith('}'):
                try:
                    commit_data = json.loads(message)
                    message = f"{commit_data['type']}: {commit_data['subject']}"
                except json.JSONDecodeError:
                    pass  # Keep the stripped message as is

        commit_messages.append({
            'message': message,
            'files': [change['path'] for change in group]
        })

    return commit_messages
