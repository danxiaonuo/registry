# Docker Registry 环境变量配置

本项目实现了 Docker Registry 通过环境变量进行配置的功能，无需手动编写 YAML 配置文件。

## 功能特性

- ✅ 支持通过环境变量配置所有 Registry 选项
- ✅ 自动从环境变量生成 YAML 配置文件
- ✅ 支持默认配置值
- ✅ 支持布尔值、数字、列表等类型自动转换
- ✅ 兼容原有配置文件方式

## 快速开始

### 构建镜像

#### 方式一：使用默认端口（5000）

```bash
docker build -t registry:custom .
```

#### 方式二：根据 REGISTRY_HTTP_ADDR 环境变量自动提取端口

```bash
# 设置环境变量
export REGISTRY_HTTP_ADDR=:8080

# 使用构建脚本（自动提取端口）
./build.sh

# 或手动指定端口
docker build --build-arg REGISTRY_PORT=8080 -t registry:custom .
```

#### 方式三：直接指定构建参数

```bash
docker build --build-arg REGISTRY_PORT=8080 -t registry:custom .
```

**注意**：`EXPOSE` 是构建时指令，如果运行时通过 `REGISTRY_HTTP_ADDR` 改变了端口，需要重新构建镜像或使用构建参数来匹配。

### 运行容器

```bash
docker run -d \
  -p 5000:5000 \
  -e REGISTRY_HTTP_ADDR=:5000 \
  -e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
  -e REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io \
  -v registry-data:/var/lib/registry \
  registry:custom
```

### 使用 docker-compose

```bash
docker-compose -f docker-compose.example.yml up -d
```

## 环境变量配置

详细的环境变量映射请参考 [ENV_VARS_MAPPING.md](ENV_VARS_MAPPING.md)

### 常用环境变量

```bash
# 日志级别
REGISTRY_LOG_LEVEL=info

# HTTP 监听地址
REGISTRY_HTTP_ADDR=:5000

# 存储目录
REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry

# 代理配置
REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io
REGISTRY_PROXY_TTL=168h

# 启用删除功能
REGISTRY_STORAGE_DELETE_ENABLED=true
```

## 配置说明

### 默认配置

项目包含以下默认配置（对应您提供的配置）：

- 版本: `0.1`
- 日志: 禁用访问日志，级别为 `info`
- 存储: 使用文件系统，blob 描述符缓存为 `inmemory`
- HTTP: 监听 `:5000`，配置了 CORS 头
- 健康检查: 启用存储驱动健康检查
- 代理: 默认代理到 `https://registry-1.docker.io`

### 环境变量覆盖

所有环境变量都会覆盖默认配置。如果某个环境变量未设置，将使用默认值。

### 强制重新生成配置

设置 `REGISTRY_GENERATE_CONFIG=true` 可以强制重新生成配置文件：

```bash
docker run -e REGISTRY_GENERATE_CONFIG=true ...
```

## 文件说明

- `generate-config.py`: 从环境变量生成配置文件的 Python 脚本
- `entrypoint.sh`: 容器入口脚本，负责生成配置并启动 Registry
- `extract-port.sh`: 从 `REGISTRY_HTTP_ADDR` 环境变量中提取端口号的辅助脚本
- `build.sh`: 构建脚本，自动从 `REGISTRY_HTTP_ADDR` 提取端口并构建镜像
- `Dockerfile`: 构建自定义 Registry 镜像的 Dockerfile（支持通过 `REGISTRY_PORT` ARG 指定 EXPOSE 端口）
- `ENV_VARS_MAPPING.md`: 详细的环境变量映射文档
- `docker-compose.example.yml`: Docker Compose 示例文件

## 注意事项

1. 需要 Python3 和 PyYAML 库（已在 Dockerfile 中安装）
2. 配置文件默认路径为 `/etc/docker/registry/config.yml`
3. 环境变量名称使用下划线分隔，对应 YAML 配置的层级结构
4. 列表值使用逗号分隔的字符串表示
5. **EXPOSE 端口设置**：
   - `EXPOSE` 是构建时指令，默认端口为 5000
   - 如果运行时通过 `REGISTRY_HTTP_ADDR` 改变了端口，需要重新构建镜像
   - 构建时可以通过 `--build-arg REGISTRY_PORT=<port>` 指定 EXPOSE 端口
   - 或使用 `./build.sh` 脚本，它会自动从 `REGISTRY_HTTP_ADDR` 环境变量提取端口

## 故障排查

### 查看生成的配置文件

```bash
docker exec <container_id> cat /etc/docker/registry/config.yml
```

### 查看容器日志

```bash
docker logs <container_id>
```

### 手动运行配置生成

```bash
docker exec <container_id> python3 /usr/local/bin/generate-config.py
```

## 许可证

Apache-2.0

