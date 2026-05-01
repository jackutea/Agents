# Agents Workspace

## 简介

这是一个以 VS Code Agent 工作流为核心的配置型仓库。

仓库主要包含两类内容：

- `agents/`：可直接作为人机交互入口或执行面的 agent 定义
- `skills/`：按主题组织的 skill 文档，用于约束不同领域任务的处理方式

当前设计中，用户有两个主要入口：

- `main.agent`：用于复杂、多阶段、需要编排的任务
- `indie.agent`：用于迷你型、可单 agent 独立闭环的任务

## 目录概览

- `agents/`：agent 定义文件
- `skills/`：按架构、Unity、网络、Linux 等领域拆分的 skill
- `gists/`：模板型配置片段，例如 `project.config.json` 和 `.editorconfig` 模板
- `tool/`：辅助脚本

## 依赖环境

使用本仓库时，建议具备以下环境：

- Windows 开发环境
- VS Code
- Git
- GitHub Copilot / Agent 模式
- PowerShell 与 `cmd`

若任务涉及特定技术栈，还需要对应运行环境，例如：

- Unity
- .NET / C#
- Linux 远程环境
- MySQL / Redis / Nginx

## How to Use

### 1. 选择入口

- 将本工程整个克隆到本地, 并放到目标工程的.github目录下
- 复杂任务、多阶段任务、需要路由多个 agent 的任务：使用 `main.agent`
- 迷你型、局部、希望单 agent 直接完成的任务：使用 `indie.agent`

### 2. 创建项目配置

- 项目级配置统一以 `gists/project.config.json.gist.md` 为模板来源
- 实际项目配置文件为项目根目录下的 `project.config.json`
- 创建或维护该文件时，需要逐项向用户核对配置值
- 后续凡是涉及项目配置的任务，都应优先读取生成后的 `project.config.json`