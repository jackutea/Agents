---
name: bootstrap-skill
description: "用于创建 skill、修改 skill、补全 skill 说明与工作流的技能。适用于新建 skill 文件、重构现有 skill、调整 skill 的职责边界、触发条件、输入输出与任务编排描述。"
---

# Bootstrap Skill

## 目的

该 skill 用于两类任务：

1. 创建新的 skill。
2. 修改已有 skill。

目标是产出结构清晰、规则可执行的 skill 文件。

## 适用场景

在以下情况使用本 skill：

- 用户要求创建一个新的 skill。
- 用户要求修改、重写、收敛或扩展一个已有 skill。
- 用户要求完善 skill 的说明、输入、输出、任务编排或约束。
- 用户要求梳理多个 skill 的边界，避免职责重叠。

在以下情况不要使用本 skill：

- 只是修改普通代码文件，而不是 skill 文件。
- 只是解释 skill 概念，没有要求落地到文件。
- 只是修复运行时代码错误，且问题不在 skill 定义本身。

## 接收的 Input

bootstrap-skill.skill 接收以下 Input：

- 用户关于 skill 创建或维护的目标。
- 目标 skill 的用途、触发条件、边界与禁区。
- 目标 skill 需要处理的输入、任务编排、输出要求。
- 目标 skill 是否已存在，以及本次是新增还是修改。

若信息不足以可靠写出 skill 文件，必须先向用户提问补齐。

## 处理的事项

bootstrap-skill.skill 负责以下事项：

1. 判断当前任务是新建 skill，还是修改 skill。
2. 明确目标 skill 的用途、边界和触发条件。
3. 确保 skill 文件必须包含 header。
4. 确保 skill 文件必须包含 `Input`、任务编排、`Output` 三块核心内容。
5. 确保任务编排部分必须包含伪代码，而不是只写原则描述。
6. 若目标 skill 缺少上述任意部分，先补齐，再处理其他扩展内容。
7. 禁止在 skill 正文中描述由谁调用该 skill，或把特定 agent / 调用者写成 skill 自身定义的一部分。
8. 若用户要求同时改 agent 和 skill，优先明确两者边界，避免互相覆盖职责。

## 输出的 Output

bootstrap-skill.skill 的 Output 至少应包含：

- 本次是新建还是修改 skill
- 创建或修改的目标 skill 文件
- 本次补齐或修正了哪些关键部分
- 若清理了调用者描述，应明确说明已移除该类表述
- 若仍有阻塞，明确指出缺失信息和下一步建议

## 任务编排

bootstrap-skill.skill 的任务编排是围绕单个目标 skill 进行结构补全与规则修正。

伪代码如下：

```text
bootstrapSkill(input) {
  var taskType = decideCreateOrUpdate(input)
  var skillSpec = collectSkillSpec(input)

  if (isMissingCriticalInfo(skillSpec)) {
    return askUserForMissingInfo(skillSpec)
  }

  var draft = buildOrUpdateSkill(taskType, skillSpec)

  ensureHeader(draft)
  ensureInputSection(draft)
  ensureTaskOrchestrationSection(draft)
  ensureTaskOrchestrationPseudoCode(draft)
  ensureOutputSection(draft)
  removeSkillCallerDescription(draft)

  return finalizeSkillDraft(draft)
}
```

约束说明：

- 任务编排必须写成可执行流程，而不是空泛描述。
- 伪代码必须体现 skill 如何消费输入、如何组织步骤、如何返回输出。
- skill 正文不得描述由谁调用自己，也不得把特定 agent / 调用者写入自身职责定义。
- 不得省略 header、`Input`、任务编排、`Output` 中任一部分。

## 执行流程

### 第一步：确认 skill 任务类型

先判断当前任务属于：

- 新建 skill
- 修改 skill 正文
- 同时补全结构与正文

### 第二步：整理最少必要信息

至少确认：

- skill 的用途
- 它接收什么 Input
- 它如何进行任务编排
- 它输出什么 Output

### 第三步：构建或修正 skill 结构

确保目标 skill 至少包含：

- header
- `Input`
- 任务编排
- 任务编排伪代码
- `Output`

### 第四步：补充细节与约束

在基础结构完整后，再补充：

- 适用场景
- 不适用场景
- 强制约束
- 成功标准

### 第五步：返回结果

返回 skill 草案、改动说明和剩余阻塞项。

## 强制约束

- 每个 skill 必须有 header。
- 每个 skill 必须明确包含 `Input`、任务编排、`Output` 三块核心内容。
- 任务编排必须包含伪代码。
- skill 中禁止出现由谁调用自己的描述。
- 若信息不足，先提问，不自行脑补关键规则。
- 参考项目时，禁止出现参考项目名。
- 使用中文交流。

## 成功标准

- 能创建新的 skill
- 能修改已有的 skill
- 能保证目标 skill 具备 header、`Input`、任务编排、`Output`
- 能保证任务编排部分带有伪代码
- 能移除或避免写入 skill 调用者描述
- 能输出结构清晰、可执行的 skill 文件