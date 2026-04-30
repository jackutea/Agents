# Unity Animator Skill

此 skill 专注于 Unity Animator Controller 和状态机设计，适用于角色、UI 或系统页面的动画状态转换。

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