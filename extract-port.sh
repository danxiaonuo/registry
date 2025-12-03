#!/bin/sh
# 从 REGISTRY_HTTP_ADDR 环境变量中提取端口号
# 支持格式: :5000, 0.0.0.0:5000, localhost:8080 等

extract_port() {
    local addr="${REGISTRY_HTTP_ADDR:-:5000}"

    # 移除所有空格
    addr=$(echo "$addr" | tr -d ' ')

    # 如果包含冒号，提取冒号后的部分
    if echo "$addr" | grep -q ':'; then
        port=$(echo "$addr" | sed 's/.*://')
        # 移除所有非数字字符（只保留端口号）
        port=$(echo "$port" | sed 's/[^0-9]//g')
    else
        # 如果没有冒号，假设整个值就是端口号
        port=$(echo "$addr" | sed 's/[^0-9]//g')
    fi

    # 如果没有提取到端口号，使用默认值 5000
    if [ -z "$port" ] || [ "$port" = "" ]; then
        port=5000
    fi

    echo "$port"
}

extract_port
