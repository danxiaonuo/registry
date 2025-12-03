#!/usr/bin/env python3
"""
从环境变量生成 Docker Registry 配置文件
支持将环境变量转换为 YAML 格式的配置文件
"""

import os
import yaml
import sys
from typing import Any, Dict, List

def parse_env_value(value: str) -> Any:
    """解析环境变量值，支持布尔值、数字、列表等类型"""
    if value == '':
        return None

    # 布尔值
    if value.lower() in ('true', 'yes', '1', 'on'):
        return True
    if value.lower() in ('false', 'no', '0', 'off'):
        return False

    # 数字
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass

    # 列表（逗号分隔）
    if ',' in value:
        return [item.strip() for item in value.split(',')]

    return value

def set_nested_value(config: Dict, path: str, value: Any):
    """在嵌套字典中设置值，路径用下划线分隔"""
    keys = path.lower().split('_')
    current = config

    # 跳过 'registry' 前缀
    if keys[0] == 'registry':
        keys = keys[1:]

    # 遍历路径，创建嵌套字典
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]

    # 设置最终值
    final_key = keys[-1]
    parsed_value = parse_env_value(value) if isinstance(value, str) else value

    if parsed_value is not None:
        current[final_key] = parsed_value

def generate_config_from_env() -> Dict:
    """从环境变量生成配置字典"""
    config = {}

    # 获取所有 REGISTRY_ 开头的环境变量
    registry_env_vars = {
        k: v for k, v in os.environ.items()
        if k.startswith('REGISTRY_')
    }

    for env_key, env_value in registry_env_vars.items():
        # 移除 REGISTRY_ 前缀并转换为配置路径
        config_path = env_key[len('REGISTRY_'):]
        set_nested_value(config, config_path, env_value)

    return config

def merge_with_defaults(config: Dict) -> Dict:
    """合并默认配置"""
    defaults = {
        'version': '0.1',
        'log': {
            'accesslog': {
                'disabled': True
            },
            'level': 'info',
            'formatter': 'text',
            'fields': {
                'service': 'registry',
                'environment': 'staging'
            }
        },
        'storage': {
            'cache': {
                'blobdescriptor': 'inmemory'
            },
            'filesystem': {
                'rootdirectory': '/var/lib/registry'
            },
            'maintenance': {
                'uploadpurging': {
                    'enabled': False
                }
            },
            'tag': {
                'concurrencylimit': 8
            },
            'delete': {
                'enabled': True
            }
        },
        'http': {
            'addr': ':5000',
            'headers': {
                'X-Content-Type-Options': ['nosniff'],
                'Access-Control-Allow-Origin': ['*'],
                'Access-Control-Allow-Methods': ['HEAD', 'GET', 'OPTIONS', 'DELETE'],
                'Access-Control-Allow-Headers': ['Authorization', 'Accept', 'Cache-Control'],
                'Access-Control-Max-Age': [1728000],
                'Access-Control-Allow-Credentials': [True],
                'Access-Control-Expose-Headers': ['Docker-Content-Digest']
            }
        },
        'health': {
            'storagedriver': {
                'enabled': True,
                'interval': '10s',
                'threshold': 3
            }
        },
        'proxy': {
            'remoteurl': 'https://registry-1.docker.io',
            'username': '',
            'password': '',
            'ttl': '168h'
        }
    }

    def deep_merge(base: Dict, override: Dict) -> Dict:
        """深度合并字典"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # 特殊处理：如果是 headers 字典，需要合并而不是替换
                if key == 'headers' and 'headers' in result:
                    result[key] = {**result[key], **value}
                else:
                    result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    return deep_merge(defaults, config)

def main():
    """主函数"""
    output_file = os.environ.get('REGISTRY_CONFIG_PATH', '/etc/docker/registry/config.yml')

    # 从环境变量生成配置
    env_config = generate_config_from_env()

    # 合并默认配置
    config = merge_with_defaults(env_config)

    # 确保版本号
    if 'version' not in config:
        config['version'] = '0.1'

    # 写入配置文件
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"配置文件已生成: {output_file}", file=sys.stderr)
    except Exception as e:
        print(f"错误: 无法写入配置文件 {output_file}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
