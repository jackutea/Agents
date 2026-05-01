---
name: unity-animation
description: "用于 Unity 动画剪辑与动画资源创建，适用于设计关键帧、配置循环与事件、生成 Animation Clip 资源及命名路径。"
---

# Unity Animation Skill

此 skill 提取 Unity 动画剪辑与动画资源创建的实现规范，适用于角色动画、UI 动画、过渡效果等场景。

## 接收的 Input

- 动画用途、目标对象和使用场景
- 关键帧需求、属性变化、时长、循环规则和事件需求
- 动画资源输出路径、命名规则和项目目录约束
- 是否需要在 Animator Controller 中被复用的额外要求

若未提供动画用途、关键帧需求或输出路径，则不能可靠生成动画方案。

## 处理的事项

1. 分析动画用途和目标对象。
2. 设计关键帧、曲线、循环与事件配置。
3. 确定 Animation Clip 的资源路径和命名。
4. 校验动画资源是否符合项目路径约束和复用需求。
5. 输出 Animation Clip 的创建结果与关键帧说明。

## 输出的 Output

unity-animation.skill 的 Output 应包含：

- Animation Clip 的用途与关键帧设计
- 循环、速度和事件配置结果
- 动画资源路径与命名结果
- 若存在阻塞，明确指出缺失项

## 任务编排

unity-animation.skill 的任务编排是先确认动画用途，再设计关键帧与配置，最后输出 Animation Clip 结果。

伪代码如下：

```text
unityAnimation(input) {
	if (isMissingAnimationSpec(input)) {
		return buildBlockedResult(input)
	}

	var animationPlan = analyzeAnimationPurpose(input)
	designKeyframes(animationPlan)
	configureLoopAndEvents(animationPlan)
	assignAnimationPath(animationPlan)

	return summarizeAnimationResult(animationPlan)
}
```

约束说明：

- 动画资源命名和路径必须符合项目约定。
- 事件配置只用于简单通知，不承载复杂业务逻辑。
- 输出必须覆盖关键帧设计与资源路径两个层面。

## 核心职责
- 设计 Animation Clip 结构和关键帧
- 配置动画循环、速度和事件
- 管理动画资源文件和命名规则
- 输出可直接在 Animator Controller 中使用的剪辑

## 实现流程
1. 确认动画用途：UI 过渡、角色动作、特效等
2. 设计关键帧节点与属性变化曲线
3. 创建 Animation Clip 资源，设置 `Loop Time`、`Loop Pose`、`Wrap Mode`
4. 如果需要，添加 Animation Event 或自定义事件回调
5. 生成动画资源路径与命名规则，例如 `Assets/Res_Runtime/Animation/{Name}.anim`

## 约束
- 所有文件编码：UTF-8 无 BOM
- 使用中文输出
- 动画资源文件名和路径需符合项目约定
- 避免在动画中硬编码业务逻辑，事件回调仅触发简单通知

## 输出说明
- 返回创建的 Animation Clip 路径与关键帧说明。