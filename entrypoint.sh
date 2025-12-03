#!/bin/sh
set -e

# 如果配置文件不存在或需要从环境变量生成，则生成配置文件
if [ ! -f "${REGISTRY_CONFIG_PATH:-/etc/docker/registry/config.yml}" ] || [ "${REGISTRY_GENERATE_CONFIG:-false}" = "true" ]; then
    echo "从环境变量生成配置文件..."

    # 检查是否有 Python3
    if command -v python3 >/dev/null 2>&1; then
        python3 /usr/local/bin/generate-config.py
    elif command -v python >/dev/null 2>&1; then
        python /usr/local/bin/generate-config.py
    else
        echo "警告: 未找到 Python，将使用默认配置或现有配置文件"
    fi
fi

# 如果没有传递参数，使用默认的 serve 命令
if [ $# -eq 0 ]; then
    exec registry serve "${REGISTRY_CONFIG_PATH:-/etc/docker/registry/config.yml}"
else
    # 执行传递的命令
    exec registry "$@"
fi
