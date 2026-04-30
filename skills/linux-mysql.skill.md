# Linux MySQL Skill

此 skill 提取了 Linux MySQL 代理的实现流程、配置约束和非交互式初始化参考。

## 核心职责

- 识别 Linux 发行版（Ubuntu/Debian、CentOS/RHEL）
- 安装 MySQL Server
- 运行 MySQL 初始化与安全配置
- 启动并设置 MySQL 服务开机自启
- 验证 MySQL 服务可用性

## 实现流程

1. **连接确认**：执行前先确认是否需要通过远程 SSH 连接到 Linux 服务器，并获取连接信息。
2. **环境侦测**：使用 `cat /etc/os-release` 或类似命令确定发行版与版本。
3. **强制询问密码**：使用 `ask-questions` 工具获取 MySQL Root 密码，禁止使用默认密码或自动生成密码。
4. **执行安装**：根据系统包管理器选择 apt / yum / dnf，使用非交互参数安装 MySQL。
5. **初始化与配置**：启动 MySQL 服务并使用 `ALTER USER` 或对应命令设置 Root 密码。
6. **验证结果**：验证 MySQL 服务运行状态，并返回最终结果。

## 约束

- 在未获取 Root 密码前，禁止执行修改密码或初始化操作。
- 使用非交互方式安装与配置，避免运行时阻塞输入。
- 安装过程和密码设置必须清晰记录并反馈给用户。
- 使用中文交流。

## Gist：Linux MySQL 非交互式初始化参考

### Ubuntu/Debian (APT)

```bash
sudo apt update
sudo apt install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql

sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{RootPassword}';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### CentOS/RHEL (YUM/DNF)

```bash
sudo dnf install -y @mysql
sudo systemctl start mysqld
sudo systemctl enable mysqld

# 安装后通常会生成临时密码，需要先获取
# TEMP_PASS=$(sudo grep 'temporary password' /var/log/mysqld.log | awk '{print $NF}')
# mysql -u root -p"$TEMP_PASS" --connect-expired-password -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '{RootPassword}';"
```