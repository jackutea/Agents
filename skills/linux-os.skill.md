# Linux OS Skill

此 skill 提供 Linux 操作系统层面的通用适配与执行规范，作为 Linux 服务执行的底层支持。

## 默认 OS

- 默认认为目标 Linux 操作系统为 **Ubuntu**。
- 如果用户明确指出不是 Ubuntu，则按实际发行版执行 OS 检测与适配。

## 核心职责

- 检测 Linux 发行版：优先判断 Ubuntu，其次支持 Debian、CentOS/RHEL、Rocky/AlmaLinux、Fedora、SUSE 等。
- 抽象包管理器：`apt` / `yum` / `dnf` / `zypper` / `pacman`。
- 提供非交互式执行准则：`DEBIAN_FRONTEND=noninteractive`、`-y` / `--assume-yes`、避免交互式提示。
- 处理远程 SSH 执行与环境确认。
- 管理服务启动与验证：`systemctl` / `service` / `ss` / `journalctl` 等。
- 提供系统权限与环境检查：是否具备 sudo 权限、是否运行在容器中、是否允许写配置文件。

## 约束

- 默认情况下，优先使用 Ubuntu 相关命令和路径。
- 若用户未说明 OS，默认假设 Ubuntu 并直接执行 Ubuntu 方案。
- 若检测到其它发行版，立即调整为对应包管理器与配置路径。
- 在任何情况下，避免执行可能破坏系统的命令，先询问再执行。
- 使用中文交流。

## OS 检测流程

1. 读取 `/etc/os-release`。
2. 识别 `ID`、`VERSION_ID`、`ID_LIKE`。
3. 若 `ID` 或 `ID_LIKE` 包含 `ubuntu`，则按 Ubuntu 处理。
4. 否则按实际发行版选择适配命令。

## 常见命令模板

### Ubuntu/Debian

```bash
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install -y <package>
```

### CentOS/RHEL

```bash
sudo yum install -y <package>
```

### Rocky/AlmaLinux

```bash
sudo dnf install -y <package>
```

### SUSE

```bash
sudo zypper install -y <package>
```

## 服务管理

- 启动服务：`sudo systemctl start <service>`
- 启用开机：`sudo systemctl enable <service>`
- 检查状态：`sudo systemctl status <service>`

## 连接与执行安全

- 如果需要远程执行，先确认 SSH 连接信息与凭证。
- 使用 `ssh -o BatchMode=yes` 防止密码交互提示。
- 若需要复制文件，使用 `scp` 或 `rsync`。
- 发生错误时，立即停止并记录失败原因。