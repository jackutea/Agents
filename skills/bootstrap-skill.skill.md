---
name: bootstrap-skill
description: "用于创建 skill、修改 skill、补全 skill 说明与工作流的技能。适用于新建 skill 文件、重构现有 skill、调整 skill 的职责边界、触发条件、输入输出与任务编排描述。"
---

# Bootstrap Skill

## 职责

bootstrap-skill.skill 只负责 skill 文件本身的创建、修改、补全与收束，不负责普通业务代码文件。

它的职责收束为以下几类：

- 判断当前任务属于新建 skill、修改已有 skill，还是收敛已有 skill 的职责边界。
- 收集并整理目标 skill 的核心结构，至少包括职责、Input、Output、任务编排、强制约束、质量标准。
- 约束由本 skill 创建或修改的目标 skill 采用与本 skill 相同的六块结构，不额外保留其他并列章节。
- 确保目标 skill 保留 header，并且正文不出现“由谁调用该 skill”的描述。
- 在信息充分后，产出结构清晰、规则可执行、可直接使用的 skill 文件。

本 skill 适用于以下情况：

- 用户要求创建新的 skill。
- 用户要求修改、重写、收敛或扩展已有 skill。
- 用户要求完善 skill 的职责、输入、输出、任务编排或约束。

本 skill 不适用于以下情况：

- 只是修改普通代码文件，而不是 skill 文件。
- 只是解释 skill 概念，没有要求落地到文件。
- 只是修复运行时代码错误，且问题不在 skill 定义本身。

若用户提供的信息不足以可靠完成 skill 文件，必须先返回缺失项并向用户提问，而不是自行脑补。

## Input

bootstrap-skill.skill 接收以下 Input：

- 用户关于 skill 创建或维护的目标。
- 目标 skill 的用途、触发条件、边界与禁区。
- 目标 skill 需要处理的输入、任务编排、输出要求。
- 目标 skill 是否已存在，以及本次是新增还是修改。

若这些信息不足以可靠写出 skill 文件，必须先向用户提问补齐。

## Output

bootstrap-skill.skill 的 Output 至少应包含：

- 本次是新建还是修改 skill。
- 创建或修改的目标 skill 文件。
- 本次补齐或修正了哪些关键部分。
- 若清理了调用者描述，应明确说明已移除该类表述。
- 若仍有阻塞，明确指出缺失信息和下一步建议。

## 任务编排

bootstrap-skill.skill 的任务编排是围绕单个目标 skill 进行结构补全与规则修正，并确保最终结构收束为固定六块内容。

伪代码如下：

```text
bootstrapSkill(input) {
  // Input: 用户提供的 skill 目标、触发条件、边界、任务编排要求、输出要求，以及当前是新建还是修改。
  var taskType = decideCreateOrUpdate(input)
  var skillSpec = collectSkillSpec(input)

  if (isMissingCriticalInfo(skillSpec)) {
    // Output: 阻塞态，返回缺失信息和下一步需要补充的内容。
    return askUserForMissingInfo(skillSpec)
  }

  var draft = buildOrUpdateSkill(taskType, skillSpec)

  ensureHeader(draft)
  ensureResponsibilitySection(draft)
  ensureInputSection(draft)
  ensureOutputSection(draft)
  ensureTaskOrchestrationSection(draft)
  ensureTaskOrchestrationPseudoCode(draft)
  ensureConstraintsSection(draft)
  ensureQualitySection(draft)
  ensureFixedSkillSectionLayout(draft)
  removeSkillCallerDescription(draft)

  // Output: 返回目标 skill 的新增或修改结果，以及清理调用者描述后的最终草案。
  return finalizeSkillDraft(draft)
}
```

## 强制约束

- 每个 skill 必须有 header。
- 每个 skill 必须明确包含职责、Input、Output、任务编排、强制约束、质量标准六块核心结构。
- 由本 skill 创建或修改的目标 skill，应与本 skill 保持同样的正文组织方式，只保留以上六块内容；其他信息应收束进这六块中，而不是继续展开为额外的并列章节。
- 任务编排必须包含伪代码。
- 任务编排必须明确体现 Input 如何进入、如何组织步骤、以及 Output 如何返回。
- 任务编排允许使用注释加强说明，但不能只写空泛原则。
- skill 正文中禁止出现由谁调用自己的描述，也不得把特定 agent / 调用者写入自身职责定义。
- 若信息不足，先提问，不自行脑补关键规则。
- 参考项目时，禁止出现参考项目名。
- 使用中文交流。

## 质量标准

- 能创建新的 skill。
- 能修改已有的 skill。
- 能保证目标 skill 保留 header。
- 能强制目标 skill 具备职责、Input、Output、任务编排、强制约束、质量标准六块核心结构。
- 能强制由本 skill 创建或修改的目标 skill 与本 skill 自身保持相同的六块结构，不额外保留其他并列章节。
- 能保证任务编排部分带有伪代码。
- 能保证任务编排明确体现 Input 与 Output。
- 能移除或避免写入 skill 调用者描述。
- 能输出结构清晰、可执行的 skill 文件。