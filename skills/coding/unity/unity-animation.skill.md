---
name: unity-animation
description: "用于 Unity 动画剪辑与动画资源创建，适用于设计关键帧、配置循环与事件、生成 Animation Clip 资源及命名路径。"
---

# Unity Animation Skill

此 skill 提取 Unity 动画剪辑与动画资源创建的实现规范，适用于角色动画、UI 动画、过渡效果等场景。

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