#!/bin/sh
# 构建脚本：自动从 REGISTRY_HTTP_ADDR 环境变量提取端口并构建镜像

set -e

# 默认值
DEFAULT_PORT=5000
IMAGE_NAME="${IMAGE_NAME:-registry:custom}"

# 从 REGISTRY_HTTP_ADDR 提取端口
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

    # 如果没有提取到端口号，使用默认值
    if [ -z "$port" ] || [ "$port" = "" ]; then
        port="$DEFAULT_PORT"
    fi

    echo "$port"
}

# 提取端口
REGISTRY_PORT=$(extract_port)

echo "从 REGISTRY_HTTP_ADDR=${REGISTRY_HTTP_ADDR:-:5000} 提取端口: $REGISTRY_PORT"
echo "构建镜像: $IMAGE_NAME"
echo "EXPOSE 端口: $REGISTRY_PORT"
echo ""

# 构建镜像
docker build \
    --build-arg REGISTRY_PORT="$REGISTRY_PORT" \
    -t "$IMAGE_NAME" \
    "$@"

echo ""
echo "构建完成！"
echo "镜像: $IMAGE_NAME"
echo "EXPOSE 端口: $REGISTRY_PORT"

