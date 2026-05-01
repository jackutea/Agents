---
name: unity-create-project
description: "用于 Unity 项目创建与初始化，适用于创建目录结构、按 Unity 版本生成 .gitignore、根据 gist 创建 .editorconfig、配置 Package 与项目设置。"
---

# Unity Create Project Skill

此 skill 专注于 Unity 项目创建和初始化流程，涵盖项目目录、Package 管理、Settings 配置以及基础工程约定。

## 核心职责
- 创建并初始化 Unity 项目目录结构
- 根据 Unity 版本创建项目所需 `.gitignore`
- 根据 `/gists/.editorconfig.gist.md` 创建 `.editorconfig`
- 配置常用 Package 与项目设置
- 规范 `Assets`、`Packages`、`ProjectSettings` 目录
- 生成基础脚本和资源占位文件

## 实现流程
1. 确认目标 Unity 版本和平台
2. 若任务包含 `.gitignore`，必须先向用户确认 Unity 版本；未确认前不得创建 `.gitignore`
3. 创建项目根目录与基础目录：`Assets/`、`Packages/`、`ProjectSettings/`、`Assets/Src_Runtime/`、`Assets/Src_Editor/`、`Assets/Src_Tests/`、`Assets/Res_Editor/`、`Assets/Res_Runtime/`
4. 根据已确认的 Unity 版本生成项目所需 `.gitignore`
5. 根据 `/gists/.editorconfig.gist.md` 创建 `.editorconfig`
6. 配置 `ProjectSettings/ProjectSettings.asset`、`EditorBuildSettings.asset`、`GraphicsSettings.asset` 等必要设置
7. 安装/配置必要 Package，如 `com.unity.textmeshpro`、`com.unity.addressables`、`com.unity.collections`、`com.unity.inputsystem` 等
8. 生成基础脚本占位文件，例如 `Assets/Src_Runtime/Main.cs`

## 约束
- 所有文件编码：UTF-8 无 BOM
- 使用中文输出
- 遵循现有项目命名与目录约定
- 创建 `.gitignore` 前必须先确认 Unity 版本
- 创建 `.editorconfig` 时必须以 `/gists/.editorconfig.gist.md` 为模板来源

## 输出说明
- 若需要，输出应包含已创建项目文件列表、`.gitignore` / `.editorconfig` 结果与关键配置项说明。