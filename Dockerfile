FROM registry:2

LABEL maintainer="xiaonuo danxiaonuo@danxiaonuo.me"

# 安装 Python3 和 PyYAML（如果基础镜像没有）
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir pyyaml || \
    (apk add --no-cache py3-yaml || true)

# 复制配置生成脚本
COPY generate-config.py /usr/local/bin/generate-config.py
RUN chmod +x /usr/local/bin/generate-config.py

# 复制 entrypoint 脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 设置入口点
# entrypoint.sh 会处理无参数的情况，自动使用默认配置
ENTRYPOINT ["/entrypoint.sh"]
