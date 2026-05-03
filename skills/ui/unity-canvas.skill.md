---
name: unity-canvas
description: "用于创建和维护 Unity Canvas 及所有 UI 组件，适用于组织 UI 节点层级、挂载 UI 组件、生成或补全 UI 相关 prefab 与 prefab.meta 结果。"
---

# Unity Canvas Skill

## 目的

该 skill 用于处理 Unity Canvas 及所有 UI 组件相关的 prefab 结构与维护工作。

目标是产出结构清晰、可直接落地的 UI prefab 与 `.prefab.meta` 结果，并明确 Canvas、节点层级、布局组件和交互组件的组织方式。

## 适用场景

在以下情况使用本 skill：

- 用户要求创建或维护 Canvas。
- 用户要求创建、补全或调整 UI prefab 节点层级。
- 用户要求挂载、整理或校验 UI 组件，例如 `RectTransform`、`CanvasRenderer`、`Image`、`TextMeshProUGUI`、`Button`、`LayoutGroup`、`ContentSizeFitter`、`ScrollRect` 等。
- 用户要求维护 UI 相关 `.prefab` 与 `.prefab.meta` 的配套结果。

在以下情况不要使用本 skill：

- 任务属于动画、Animator Controller 或渲染 Shader。
- 任务属于非 UI prefab。
- 任务属于 ScriptableObject 资源文件。
- 任务属于 Unity C# 代码编写。

## 接收的 Input

- 目标 UI prefab 路径、名称和目录约束。
- Canvas 类型、渲染模式、分辨率适配、相机或 Sorting 要求。
- 节点层级、组件清单、布局约束、交互需求和资源引用关系。
- 真实 GUID 上下文、已有 prefab 差异目标、是否需要补全 `.prefab.meta`。

若未提供目标路径、关键节点结构、组件要求或真实 GUID 上下文，则不能可靠生成 UI prefab 结果。

## 处理的事项

1. 确认 UI prefab 的名称、路径、节点层级和命名规则。
2. 确认 Canvas 配置、适配规则、布局组件和交互组件要求。
3. 校验 GUID、资源引用和 `.prefab.meta` 上下文是否齐全。
4. 生成或补全 UI prefab 结构结果。
5. 生成或补全对应 `.prefab.meta` 结果，并保持配对一致。
6. 输出 UI 文件结果、缺失项和后续建议。

## 输出的 Output

unity-canvas.skill 的 Output 应包含：

- 创建或修改的 `.prefab` 与 `.prefab.meta` 文件
- Canvas 配置、节点层级与组件组织结果
- 使用到的真实依赖上下文说明
- 若存在阻塞，明确指出缺失信息

## 任务编排

unity-canvas.skill 的任务编排是先确认 UI 结构与 Canvas 约束，再组织节点和组件，最后返回 prefab 与 meta 结果。

伪代码如下：

```text
unityCanvas(input) {
  if (isMissingPrefabPath(input) || isMissingUiHierarchy(input) || isMissingGuidContext(input)) {
    return buildBlockedResult(input)
  }

  var uiPlan = analyzeUnityUiSpec(input)
  validateCanvasConfig(uiPlan)
  validateGuidAndMetaContext(uiPlan)
  buildPrefabHierarchy(uiPlan)
  attachUiComponents(uiPlan)
  createPrefabMeta(uiPlan)

  return summarizeUnityCanvasResult(uiPlan)
}
```

约束说明：

- `.prefab` 与 `.prefab.meta` 必须成对生成或修改。
- GUID 和资源引用必须来自真实上下文，禁止凭空捏造。
- 输出必须同时覆盖 Canvas 配置、节点层级、组件组织和阻塞信息。
- skill 正文不得描述由谁调用自己。

## 强制约束

- 每个 skill 必须有 header。
- 必须明确包含 `Input`、任务编排、`Output` 三块核心内容。
- 任务编排必须包含伪代码。
- 不得写入特定 agent 或调用者描述。
- 若信息不足，先提问，不自行脑补关键规则。

## 成功标准

- 能创建新的 UI prefab 与 `.prefab.meta` 结果
- 能组织 Canvas 与 UI 节点层级
- 能补全常见 UI 组件配置
- 能保证任务编排部分带有伪代码
- 能输出结构清晰、可执行的 skill 文件