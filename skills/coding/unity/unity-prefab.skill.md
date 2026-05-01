---
name: unity-prefab
description: "用于 Unity UI prefab 构建，适用于设计节点层级、生成 .prefab 与 .prefab.meta、挂载脚本组件，以及配置 Addressables 标记。"
---

# Unity Prefab Skill

此 skill 专注于 Unity UI prefab 的构建与绑定，尤其适用于 Panel、窗口、界面组件等 prefab 生成与脚本挂载。

## 接收的 Input

- prefab 的用途、名称、目标路径和 UI 层级需求
- 需要挂载的脚本、组件树、Addressables 分组和标签规则
- 与 `.prefab.meta`、`.cs.meta`、GUID 相关的真实上下文信息
- 现有资源结构和项目命名约束

若未提供 prefab 名称、目标路径或真实 GUID 上下文，则不能可靠生成 prefab 结果。

## 处理的事项

1. 设计 prefab 根节点和 UI 组件层级。
2. 生成 `.prefab` 与 `.prefab.meta` 配对结果。
3. 生成或绑定脚本组件，并同步脚本引用。
4. 配置 Addressables 分组与标签。
5. 校验所有 GUID、路径和资源结构是否来源真实上下文。

## 输出的 Output

unity-prefab.skill 的 Output 应包含：

- 生成或修改的 `.prefab`、`.prefab.meta` 和脚本文件
- UI 层级与挂载结果
- Addressables 标记结果
- 若存在阻塞，明确指出缺失的 GUID、路径或依赖

## 任务编排

unity-prefab.skill 的任务编排是先确定 prefab 结构，再生成资源配对和脚本绑定，最后汇总 Addressables 与输出结果。

伪代码如下：

```text
unityPrefab(input) {
	if (isMissingPrefabSpec(input) || isMissingGuidContext(input)) {
		return buildBlockedResult(input)
	}

	var prefabPlan = analyzePrefabStructure(input)
	buildPrefabHierarchy(prefabPlan)
	createPrefabAndMeta(prefabPlan)
	attachScriptsAndResolveGuid(prefabPlan)
	markAddressables(prefabPlan)

	return summarizePrefabResult(prefabPlan)
}
```

约束说明：

- `.prefab` 与 `.prefab.meta` 必须成对生成。
- 所有 GUID 必须来自真实项目上下文，禁止凭空填写。
- 输出必须覆盖 UI 层级、脚本挂载和 Addressables 三个层面。

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