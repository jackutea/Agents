# Linux Nginx Skill

此 skill 提取了 Linux Nginx 代理的实现流程、配置约束和非交互式参考。

## 核心职责

- 识别 Linux 发行版（Ubuntu/Debian、CentOS/RHEL）
- 安装并启动 Nginx
- 配置 HTTP/HTTPS 站点
- 配置 TCP 转发（stream）
- 验证 Nginx 服务可用性

## 实现流程

1. **连接确认**：执行前先确认是否需要通过远程 SSH 连接到目标服务器，并获取连接信息。
2. **环境侦测**：使用 `cat /etc/os-release` 等命令确定发行版。
3. **强制询问站点参数**：使用 `ask-questions` 工具获取站点域名、端口映射规则、证书路径、是否启用 HTTP 至 HTTPS 跳转，及 TCP 转发需求。
4. **执行安装**：根据包管理器选择 apt / yum / dnf，使用非交互参数安装 Nginx 并设置开机自启。
5. **初始化与配置**：生成站点配置或 stream 配置文件，确保 `nginx -t` 校验通过后重载服务。
6. **验证结果**：使用 `systemctl status nginx` 和 `curl` / `nc` 等命令验证 HTTP、HTTPS 与 TCP 转发。

## 约束

- 在未获取完整域名、端口映射规则及证书参数前，禁止写入站点配置。
- 使用非交互方式安装与配置，避免命令阻塞输入。
- 禁止使用伪 HTTPS；证书路径必须存在且可访问。
- 禁止重复映射同一监听端口至多个上游。
- 使用中文交流。

## Gist：Linux Nginx 非交互式配置参考（HTTP/HTTPS/TCP）

### Ubuntu/Debian (APT)

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

sudo tee /etc/nginx/sites-available/{Domain}.conf >/dev/null <<'EOF'
server {
    listen 80;
    server_name {Domain};

    location / {
        proxy_pass http://{UpstreamHost}:{UpstreamPort};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/{Domain}.conf /etc/nginx/sites-enabled/{Domain}.conf
sudo nginx -t
sudo systemctl reload nginx

sudo mkdir -p /etc/nginx/stream.d
sudo grep -Fq "include /etc/nginx/stream.d/*.conf;" /etc/nginx/nginx.conf || \
    sudo sed -i '/http\s*{/i stream {\n    include /etc/nginx/stream.d/*.conf;\n}\n' /etc/nginx/nginx.conf

sudo tee /etc/nginx/stream.d/tcp-{TcpListenPort}.conf >/dev/null <<'EOF'
server {
    listen {TcpListenPort};
    proxy_pass {TcpTargetHost}:{TcpTargetPort};
}
EOF

sudo nginx -t
sudo systemctl reload nginx
```

### CentOS/RHEL (YUM/DNF)

```bash
sudo dnf install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

sudo tee /etc/nginx/conf.d/{Domain}.conf >/dev/null <<'EOF'
server {
    listen 80;
    server_name {Domain};
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name {Domain};

    ssl_certificate {CertFile};
    ssl_certificate_key {KeyFile};

    location / {
        proxy_pass http://{UpstreamHost}:{UpstreamPort};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

sudo nginx -t
sudo systemctl reload nginx

sudo mkdir -p /etc/nginx/stream.d
sudo grep -Fq "include /etc/nginx/stream.d/*.conf;" /etc/nginx/nginx.conf || \
  sudo sed -i '/http\s*{/i stream {\n    include /etc/nginx/stream.d/*.conf;\n}\n' /etc/nginx/nginx.conf

sudo tee /etc/nginx/stream.d/tcp-{TcpListenPort}.conf >/dev/null <<'EOF'
server {
    listen {TcpListenPort};
    proxy_pass {TcpTargetHost}:{TcpTargetPort};
}
EOF

sudo nginx -t
sudo systemctl reload nginx
```