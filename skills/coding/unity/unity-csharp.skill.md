---
name: unity-csharp
description: "用于 Unity C# 代码编写，适用于创建或修改 MonoBehaviour、ScriptableObject 配套脚本、运行期脚本、编辑器脚本，以及遵循 Unity 项目结构与代码风格约束输出 .cs 文件。"
---

# Unity CSharp Skill

此 skill 专注于 Unity C# 代码编写，适用于运行期脚本、编辑器脚本、组件脚本、配置脚本及其他 Unity 相关 `.cs` 文件的创建与修改。

## 接收的 Input

- 用户或调用方提出的 Unity C# 代码编写或修改需求
- 目标脚本路径、类名、命名空间、用途、依赖组件、运行期或编辑器期类型
- 若涉及架构层设计，还包括上下文注册、实体设计、目录结构、依赖方向、代码风格等架构信息

若信息不足以可靠生成 `.cs` 文件结构，应先指出缺失项。

## 核心职责
- 创建或修改 Unity C# 脚本文件
- 明确脚本属于运行期、编辑器期、工具类或配置类
- 保持脚本路径、类名、命名空间与项目结构一致
- 输出可直接继续实现或接入 Unity 工程的 `.cs` 文件内容
- 当任务涉及架构约束时，在内部继续调用相关 architecture skills

## 任务编排

unity-csharp.skill 的任务编排是先确定 C# 脚本用途，再在需要时把架构层规则下沉到 architecture skills，最后统一生成 `.cs` 结果。

伪代码如下：

```text
unityCSharp(input) {
	var scriptSpec = analyzeScriptSpec(input)
	if (isMissingCriticalInfo(scriptSpec)) {
		return buildBlockedResult(scriptSpec)
	}

	var architectureNotes = []
	if (includesArchitectureConstraint(scriptSpec)) {
		architectureNotes.push(architecture-design.skill(scriptSpec))
        architectureNotes.push(architecture-main.skill(scriptSpec))
		architectureNotes.push(architecture-context.skill(scriptSpec))
		architectureNotes.push(architecture-entity.skill(scriptSpec))
	}

	var codeResult = buildUnityCSharp(scriptSpec, architectureNotes)
	return summarizeCSharpResult(codeResult, architectureNotes)
}
```

约束说明：

- `unity-csharp.skill` 是 Unity 架构规则进入 architecture skills 的唯一内部入口。
- 若任务涉及架构设计或风格审查，必须把相关 architecture skills 全部纳入内部编排。
- `unity.agent` 不直接调用 architecture skills，而是通过 `unity-csharp.skill` 间接处理。

## 实现流程
1. 确认脚本用途，例如 MonoBehaviour、普通运行期类、Editor 脚本、ScriptableObject 配套脚本、工具类
2. 确认目标路径、类名、命名空间、依赖组件、生命周期方法和输出要求
3. 若涉及架构约束，在内部调用`architecture-design.skill.md`、`architecture-main.skill.md`、`architecture-context.skill.md`、`architecture-entity.skill.md`
4. 根据脚本用途判断应放入 `Src_Runtime`、`Src_Editor` 或其他约定目录
5. 按 Unity 和项目约定编写 `.cs` 文件内容
6. 输出创建或修改结果，并指出仍需补充的信息

## 约束
- 所有文件编码：UTF-8 无 BOM
- 使用中文输出
- 路径、类名、命名空间必须与项目结构和用途一致
- 若任务涉及架构层设计，应在内部调用所有相关 architecture skills，并保持输出与架构约束一致
- 若信息不足以可靠生成代码结构，应先指出缺失项，不凭空补全关键依赖

## 输出说明
- 输出处理时接入了哪些 architecture skills（如有）
- 输出创建或修改的 `.cs` 文件列表
- 说明脚本用途、目标路径和关键类结构
- 若存在阻塞，明确指出缺失信息与下一步建议