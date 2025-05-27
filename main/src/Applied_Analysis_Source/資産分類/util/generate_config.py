import argparse
import yaml
from pathlib import Path

def generate_config(args):
    config = {
        'model': {
            'name': 'microsoft/codebert-base',
            'threshold': 0.9,
            'max_length': 512
        },
        'ai_services': {
            'openai': {
                'api_key': args.openai_key,
                'model': 'gpt-4',
                'endpoint': 'https://api.openai.com/v1/chat/completions'
            },
            'anthropic': {
                'api_key': args.anthropic_key,
                'model': 'claude-3-opus-20240229',
                'endpoint': 'https://api.anthropic.com/v1/complete'
            }
        },
        'databases': {
            'asset_db': {
                'host': args.db_host,
                'port': args.db_port,
                'database': args.db_name,
                'user': args.db_user,
                'password': args.db_pass,
                'ssl_mode': 'require'
            }
        },
        'cloud_services': {
            'azure': {
                'connection_string': args.azure_conn_str,
                'container': 'code-repository'
            },
            'aws': {
                's3_bucket': 'asset-analysis',
                'region': 'ap-northeast-1',
                'access_key': args.aws_access_key,
                'secret_key': args.aws_secret_key
            }
        }
    }

    with open(Path(__file__).parent.parent / 'config.yml', 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--openai-key", required=True)
    parser.add_argument("--anthropic-key", required=True)
    parser.add_argument("--db-host", required=True)
    parser.add_argument("--db-port", required=True)
    parser.add_argument("--db-name", required=True)
    parser.add_argument("--db-user", required=True)
    parser.add_argument("--db-pass", required=True)
    parser.add_argument("--azure-conn-str", required=True)
    parser.add_argument("--aws-access-key", required=True)
    parser.add_argument("--aws-secret-key", required=True)
    
    args = parser.parse_args()
    generate_config(args)
