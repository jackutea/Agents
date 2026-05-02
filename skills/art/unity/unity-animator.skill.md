---
name: unity-animator
description: "用于 Unity Animator Controller 与状态机设计，适用于创建动画状态、参数、转换条件、Blend Tree 与子状态机结构。"
---

# Unity Animator Skill

此 skill 专注于 Unity Animator Controller 和状态机设计，适用于角色、UI 或系统页面的动画状态转换。

## 接收的 Input

- 目标对象的动画状态集合和切换需求
- 需要使用的参数类型、触发器、条件和 Blend Tree 需求
- Animator Controller 的资源路径、命名规则和复用要求
- 是否需要子状态机、层级拆分或跨状态复用

若未提供状态集合、转换条件或资源范围，则不能可靠设计状态机。

## 处理的事项

1. 分析状态集、状态切换条件和触发逻辑。
2. 设计参数、状态节点、过渡条件和退出时间。
3. 设计 Blend Tree、子状态机或层级拆分方案。
4. 校验 Animator 结构是否满足可读性和可维护性要求。
5. 输出 Animator Controller 的结构说明和关键转换结果。

## 输出的 Output

unity-animator.skill 的 Output 应包含：

- 状态机结构与状态列表
- 参数、触发器和转换条件
- Blend Tree 或子状态机设计结果
- 资源路径、命名和阻塞项

## 任务编排

unity-animator.skill 的任务编排是先确定状态集合，再组织参数和转换关系，最后输出 Animator Controller 设计结果。

伪代码如下：

```text
unityAnimator(input) {
	if (isMissingAnimatorSpec(input)) {
		return buildBlockedResult(input)
	}

	var animatorPlan = analyzeAnimatorStates(input)
	defineAnimatorParameters(animatorPlan)
	buildStateMachine(animatorPlan)
	refineBlendTreeAndSubStates(animatorPlan)

	return summarizeAnimatorResult(animatorPlan)
}
```

约束说明：

- 状态与过渡关系必须保持可读，避免无必要的复杂嵌套。
- 输出必须覆盖状态、参数和过渡条件，不只列单个节点。
- 资源命名和路径必须符合项目约定。

## 核心职责
- 设计 Animator Controller 架构
- 创建动画状态机与状态转换
- 定义参数、触发器和条件
- 管理子状态机、Blend Tree 与过渡逻辑

## 实现流程
1. 确认动画状态集和切换逻辑
2. 设计参数集合：`Bool`、`Trigger`、`Float`、`Int`
3. 创建状态机节点与过渡关系
4. 绑定 Animation Clip 到状态节点
5. 设置转换条件、退出时间、过渡持续时间
6. 如果需要，设计 Blend Tree 和子状态机

## 约束
- 所有文件编码：UTF-8 无 BOM
- 使用中文输出
- Animator 资源命名与项目规范一致
- 过渡逻辑应避免复杂嵌套，保持可读性和可维护性

## 输出说明
- 返回 Animator Controller 结构说明、参数列表与关键状态转换。