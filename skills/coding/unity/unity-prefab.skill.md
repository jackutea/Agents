---
name: unity-prefab
description: "用于 Unity UI prefab 构建，适用于设计节点层级、生成 .prefab 与 .prefab.meta、挂载脚本组件，以及配置 Addressables 标记。"
---

# Unity Prefab Skill

此 skill 专注于 Unity UI prefab 的构建与绑定，尤其适用于 Panel、窗口、界面组件等 prefab 生成与脚本挂载。

## 核心职责
- 设计 UI prefab 结构与节点层级
- 生成 `.prefab` 和 `.prefab.meta` 文件
- 编写并挂载 UI 脚本组件
- 添加 Addressables 标记与分组

## 实现流程
1. 设计 prefab 根节点：`Canvas` + `CanvasScaler` + `GraphicRaycaster`
2. 生成 UI 组件树，并确保 Image/TMP 节点包含 `CanvasRenderer`
3. 生成 `Assets/Res_Runtime/Panel/Panel_{Name}.prefab` 和对应 `.prefab.meta`
4. 生成 UI 脚本 `Assets/Src_Runtime/Panel/Panel_{Name}.cs`，继承 `PanelBase`
5. 挂载脚本至 prefab，并同步更新 `m_Script` 引用与 `.cs.meta` GUID
6. 将 prefab 标记到 Addressables Group `Panel`，Label `Panel`

## 约束
- 所有文件编码：UTF-8 无 BOM
- 使用中文输出
- UI prefab 文件请保持项目现有资源目录结构
- `.prefab` 与 `.prefab.meta` 必须成对生成
- 组件 GUID 必须来源真实项目环境，禁止凭记忆填写

## 输出说明
- 输出创建/修改的 `.prefab`、`.prefab.meta`、脚本和 Addressables 标记列表。