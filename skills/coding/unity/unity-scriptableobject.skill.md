---
name: unity-scriptableobject
description: "用于创建和补全 Unity ScriptableObject 资源文件，适用于生成自定义 .asset 与 .asset.meta、校验资源路径与类型信息、返回可继续使用的资源结果。"
---

# Unity ScriptableObject Skill

此 skill 专注于 Unity ScriptableObject 资源文件的创建，尤其适用于自定义 `.asset` 与 `.asset.meta` 文件的生成与补全。

## 核心职责
- 生成自定义 ScriptableObject 的 `.asset` 文件
- 生成与之对应的 `.asset.meta` 文件
- 校验资源路径、命名和类型信息
- 向调用方返回可继续使用的资源结果

## 实现流程
1. 确认 ScriptableObject 类型名、资源名称、输出路径和命名约定
2. 确认是否已有匹配的 `.cs.meta`、GUID 或现成资源依赖；缺失时明确提示
3. 生成目标 `.asset` 文件内容，保持 Unity 可识别的 YAML 结构
4. 生成对应 `.asset.meta` 文件，并确保其与资源路径一致
5. 输出创建结果、缺失项和后续建议

## 约束
- 所有文件编码：UTF-8 无 BOM
- 使用中文输出
- `.asset` 与 `.asset.meta` 必须成对生成
- GUID、fileID 等必须来源真实上下文；信息不足时不得凭空捏造

## 输出说明
- 输出创建或修改的 `.asset`、`.asset.meta` 文件列表
- 如有缺失信息，明确指出阻塞点与所需补充内容