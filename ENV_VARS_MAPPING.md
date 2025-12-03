# Docker Registry 环境变量配置映射

本文档说明如何通过环境变量配置 Docker Registry，而不是使用传统的 YAML 配置文件。

## 使用方法

### 方式一：使用环境变量（推荐）

设置环境变量后，容器启动时会自动生成配置文件：

```bash
docker run -d \
  -e REGISTRY_LOG_LEVEL=info \
  -e REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry \
  -e REGISTRY_HTTP_ADDR=:5000 \
  -e REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io \
  -p 5000:5000 \
  registry:custom
```

### 方式二：使用 docker-compose

```yaml
version: '3.8'
services:
  registry:
    image: registry:custom
    ports:
      - "5000:5000"
    environment:
      - REGISTRY_LOG_LEVEL=info
      - REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry
      - REGISTRY_HTTP_ADDR=:5000
      - REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io
      - REGISTRY_PROXY_USERNAME=
      - REGISTRY_PROXY_PASSWORD=
      - REGISTRY_PROXY_TTL=168h
    volumes:
      - registry-data:/var/lib/registry
volumes:
  registry-data:
```

## 环境变量映射表

### 基础配置

| 环境变量 | YAML 路径 | 默认值 | 说明 |
|---------|----------|--------|------|
| `REGISTRY_VERSION` | `version` | `0.1` | 配置版本 |

### 日志配置

| 环境变量 | YAML 路径 | 默认值 | 说明 |
|---------|----------|--------|------|
| `REGISTRY_LOG_ACCESSLOG_DISABLED` | `log.accesslog.disabled` | `true` | 禁用访问日志 |
| `REGISTRY_LOG_LEVEL` | `log.level` | `info` | 日志级别 (debug, info, warn, error) |
| `REGISTRY_LOG_FORMATTER` | `log.formatter` | `text` | 日志格式 (text, json) |
| `REGISTRY_LOG_FIELDS_SERVICE` | `log.fields.service` | `registry` | 服务名称 |
| `REGISTRY_LOG_FIELDS_ENVIRONMENT` | `log.fields.environment` | `staging` | 环境名称 |

### 存储配置

| 环境变量 | YAML 路径 | 默认值 | 说明 |
|---------|----------|--------|------|
| `REGISTRY_STORAGE_CACHE_BLOBDESCRIPTOR` | `storage.cache.blobdescriptor` | `inmemory` | Blob 描述符缓存类型 |
| `REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY` | `storage.filesystem.rootdirectory` | `/var/lib/registry` | 文件系统存储根目录 |
| `REGISTRY_STORAGE_MAINTENANCE_UPLOADPURGING_ENABLED` | `storage.maintenance.uploadpurging.enabled` | `false` | 启用上传清理 |
| `REGISTRY_STORAGE_TAG_CONCURRENCYLIMIT` | `storage.tag.concurrencylimit` | `8` | 标签并发限制 |
| `REGISTRY_STORAGE_DELETE_ENABLED` | `storage.delete.enabled` | `true` | 启用删除功能 |

### HTTP 配置

| 环境变量 | YAML 路径 | 默认值 | 说明 |
|---------|----------|--------|------|
| `REGISTRY_HTTP_ADDR` | `http.addr` | `:5000` | HTTP 监听地址 |
| `REGISTRY_HTTP_HEADERS_X_CONTENT_TYPE_OPTIONS` | `http.headers.X-Content-Type-Options` | `nosniff` | 安全头 |
| `REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_ORIGIN` | `http.headers.Access-Control-Allow-Origin` | `*` | CORS 允许来源 |
| `REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_METHODS` | `http.headers.Access-Control-Allow-Methods` | `HEAD,GET,OPTIONS,DELETE` | CORS 允许方法（逗号分隔） |
| `REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_HEADERS` | `http.headers.Access-Control-Allow-Headers` | `Authorization,Accept,Cache-Control` | CORS 允许头（逗号分隔） |
| `REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_MAX_AGE` | `http.headers.Access-Control-Max-Age` | `1728000` | CORS 最大年龄 |
| `REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_CREDENTIALS` | `http.headers.Access-Control-Allow-Credentials` | `true` | CORS 允许凭证 |
| `REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_EXPOSE_HEADERS` | `http.headers.Access-Control-Expose-Headers` | `Docker-Content-Digest` | CORS 暴露头 |

### 健康检查配置

| 环境变量 | YAML 路径 | 默认值 | 说明 |
|---------|----------|--------|------|
| `REGISTRY_HEALTH_STORAGEDRIVER_ENABLED` | `health.storagedriver.enabled` | `true` | 启用存储驱动健康检查 |
| `REGISTRY_HEALTH_STORAGEDRIVER_INTERVAL` | `health.storagedriver.interval` | `10s` | 健康检查间隔 |
| `REGISTRY_HEALTH_STORAGEDRIVER_THRESHOLD` | `health.storagedriver.threshold` | `3` | 健康检查阈值 |

### 代理配置

| 环境变量 | YAML 路径 | 默认值 | 说明 |
|---------|----------|--------|------|
| `REGISTRY_PROXY_REMOTEURL` | `proxy.remoteurl` | `https://registry-1.docker.io` | 远程代理 URL |
| `REGISTRY_PROXY_USERNAME` | `proxy.username` | `` | 代理用户名 |
| `REGISTRY_PROXY_PASSWORD` | `proxy.password` | `` | 代理密码 |
| `REGISTRY_PROXY_TTL` | `proxy.ttl` | `168h` | 代理 TTL |

## 特殊配置

### 列表值

对于列表类型的配置（如 HTTP headers），使用逗号分隔的字符串：

```bash
REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_METHODS="HEAD,GET,OPTIONS,DELETE"
```

### 布尔值

支持以下布尔值表示：
- `true`, `yes`, `1`, `on` → `true`
- `false`, `no`, `0`, `off` → `false`

### 数字值

自动识别整数和浮点数：
- `8` → 整数 8
- `1728000` → 整数 1728000
- `3.14` → 浮点数 3.14

## 配置生成

### 自动生成

默认情况下，如果配置文件不存在，容器启动时会自动从环境变量生成配置文件。

### 强制重新生成

设置环境变量 `REGISTRY_GENERATE_CONFIG=true` 可以强制重新生成配置文件：

```bash
docker run -e REGISTRY_GENERATE_CONFIG=true ...
```

### 自定义配置文件路径

使用环境变量 `REGISTRY_CONFIG_PATH` 指定配置文件路径：

```bash
docker run -e REGISTRY_CONFIG_PATH=/custom/path/config.yml ...
```

## 示例配置

### 完整示例

```bash
# 版本
export REGISTRY_VERSION=0.1

# 日志配置
export REGISTRY_LOG_ACCESSLOG_DISABLED=true
export REGISTRY_LOG_LEVEL=info
export REGISTRY_LOG_FORMATTER=text
export REGISTRY_LOG_FIELDS_SERVICE=registry
export REGISTRY_LOG_FIELDS_ENVIRONMENT=staging

# 存储配置
export REGISTRY_STORAGE_CACHE_BLOBDESCRIPTOR=inmemory
export REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/var/lib/registry
export REGISTRY_STORAGE_MAINTENANCE_UPLOADPURGING_ENABLED=false
export REGISTRY_STORAGE_TAG_CONCURRENCYLIMIT=8
export REGISTRY_STORAGE_DELETE_ENABLED=true

# HTTP 配置
export REGISTRY_HTTP_ADDR=:5000
export REGISTRY_HTTP_HEADERS_X_CONTENT_TYPE_OPTIONS=nosniff
export REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_ORIGIN=*
export REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_METHODS=HEAD,GET,OPTIONS,DELETE
export REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_HEADERS=Authorization,Accept,Cache-Control
export REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_MAX_AGE=1728000
export REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_ALLOW_CREDENTIALS=true
export REGISTRY_HTTP_HEADERS_ACCESS_CONTROL_EXPOSE_HEADERS=Docker-Content-Digest

# 健康检查配置
export REGISTRY_HEALTH_STORAGEDRIVER_ENABLED=true
export REGISTRY_HEALTH_STORAGEDRIVER_INTERVAL=10s
export REGISTRY_HEALTH_STORAGEDRIVER_THRESHOLD=3

# 代理配置
export REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io
export REGISTRY_PROXY_USERNAME=
export REGISTRY_PROXY_PASSWORD=
export REGISTRY_PROXY_TTL=168h
```

## 注意事项

1. **环境变量优先级**：环境变量会覆盖默认配置
2. **配置文件路径**：默认配置文件路径为 `/etc/docker/registry/config.yml`
3. **Python 依赖**：需要 Python3 和 PyYAML 库
4. **大小写敏感**：环境变量名称不区分大小写，但建议使用大写
5. **空值处理**：空字符串会被转换为 `null`

## 故障排查

### 检查生成的配置文件

```bash
docker exec <container_id> cat /etc/docker/registry/config.yml
```

### 查看日志

```bash
docker logs <container_id>
```

### 手动运行配置生成脚本

```bash
docker exec <container_id> python3 /usr/local/bin/generate-config.py
```
