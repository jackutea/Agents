---
name: unity-scriptableobject
description: "用于创建和补全 Unity ScriptableObject 资源文件，适用于生成自定义 .asset 与 .asset.meta、校验资源路径与类型信息、返回可继续使用的资源结果。"
---

# Unity ScriptableObject Skill

此 skill 专注于 Unity ScriptableObject 资源文件的创建，尤其适用于自定义 `.asset` 与 `.asset.meta` 文件的生成与补全。

## 接收的 Input

- ScriptableObject 类型名、资源名称和目标输出路径
- 相关 `.cs.meta`、GUID、fileID 或其他真实依赖上下文
- 资源命名规则、目录约束和是否需要补全已有资源
- 调用方希望返回的资源结果和阻塞信息

若未提供类型名、目标路径或真实 GUID 上下文，则不能可靠生成资源文件。

## 处理的事项

1. 确认 ScriptableObject 的类型、名称、路径和命名规则。
2. 校验 `.cs.meta`、GUID、fileID 和依赖上下文是否齐全。
3. 生成 `.asset` 文件内容。
4. 生成对应 `.asset.meta` 文件并保持配对一致。
5. 输出资源结果、缺失项和后续建议。

## 输出的 Output

unity-scriptableobject.skill 的 Output 应包含：

- 创建或修改的 `.asset` 与 `.asset.meta` 文件
- 资源类型、路径和命名结果
- 使用到的真实依赖上下文说明
- 若存在阻塞，明确指出缺失信息

## 任务编排

unity-scriptableobject.skill 的任务编排是先确认类型与 GUID 上下文，再生成 `.asset` 与 `.asset.meta` 配对结果，最后返回资源输出。

伪代码如下：

```text
unityScriptableObject(input) {
	if (isMissingSoType(input) || isMissingSoPath(input) || isMissingGuidContext(input)) {
		return buildBlockedResult(input)
	}

	var soPlan = analyzeScriptableObjectSpec(input)
	validateGuidAndMetaContext(soPlan)
	createAssetYaml(soPlan)
	createAssetMeta(soPlan)

	return summarizeScriptableObjectResult(soPlan)
}
```

约束说明：

- `.asset` 与 `.asset.meta` 必须成对生成或修改。
- GUID、fileID 等必须来自真实上下文，禁止凭空捏造。
- 输出必须同时覆盖资源路径、类型和阻塞信息。

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