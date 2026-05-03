---
name: bootstrap-skill
description: "用于创建 skill、修改 skill、补全 skill 说明与工作流的技能。适用于新建 skill 文件、重构现有 skill、调整 skill 的职责边界、触发条件、输入输出与任务编排描述。"
---

# Bootstrap Skill

## 职责

bootstrap-skill.skill 只负责 skill 文件本身的创建、修改、补全与收束，不负责普通业务代码文件。

它的职责收束为以下几类：

- 判断当前任务属于新建 skill、修改已有 skill，还是收敛已有 skill 的职责边界。
- 接收当前轮人机交互中整理出的 skill 可改进项，并仅在用户已确认处理范围后进入正式编辑。
- 收集并整理目标 skill 的核心结构，至少包括职责、Input、Output、任务编排、强制约束、质量标准。
- 约束由本 skill 创建或修改的目标 skill 采用与本 skill 相同的六块结构，不额外保留其他并列章节。
- 确保目标 skill 保留 header，并且正文不出现“由谁调用该 skill”的描述。
- 对未被本次处理的 skill 改进项做保留说明，供上层继续问询或下轮处理。
- 在信息充分后，产出结构清晰、规则可执行、可直接使用的 skill 文件。
- 仅适用于 skill 文件本身的创建、修改、重写、收束与说明补全；不处理普通业务代码，也不替代运行时代码修复。

## Input

- 用户关于 skill 创建或维护的目标。
- 目标 skill 的用途、触发条件、边界与禁区。
- 目标 skill 需要处理的输入、任务编排、输出要求。
- 目标 skill 是否已存在，以及本次是新增还是修改。
- 当前轮人机交互中整理出的 skill 可改进项，以及用户已确认的处理范围。

## Output

- 本次是新建还是修改 skill。
- 创建或修改的目标 skill 文件。
- 本次补齐或修正了哪些关键部分。
- 当前轮已处理了哪些 skill 改进项，哪些仍未处理。
- 若清理了调用者描述，应明确说明已移除该类表述。
- 若仍有阻塞，明确指出缺失信息和下一步建议。

## 任务编排

伪代码如下：

```text
bootstrapSkill(input) {
  // Input 是用户提供的 skill 目标、触发条件、边界、任务编排要求、输出要求、当前是新建还是修改，
  // 以及当前轮人机交互中已经整理出的 skill 可改进项与用户已确认的处理范围。
  // 只处理 skill 文件本身；若任务实际是普通代码修改、纯概念解释或运行时代码修复，应直接返回改派建议。
  var taskType = decideCreateOrUpdate(input)
  var skillSpec = collectSkillSpec(input)
  var selectedImprovements = collectSelectedSkillImprovements(input)

  if (isMissingImprovementSelectionForSkillWork(selectedImprovements, taskType)) {
    // Output: 待确认态，返回 skill 可改进项与下一步需要用户确认的处理范围。
    return askUserToConfirmSkillImprovements(skillSpec, selectedImprovements)
  }

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

  // 在正式生成前，必须保证目标 skill 的正文能收束为固定六块，且不残留“由谁调用该 skill”的描述。
  // Output: 返回目标 skill 的新增或修改结果、已处理改进项、未处理改进项，以及清理调用者描述后的最终草案。
  return finalizeSkillDraft(draft, selectedImprovements)
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
- 涉及 skill 正式改动时，若还没有当前轮已确认的 skill 改进项范围，不得直接进入编辑。
- 本次已处理与未处理的 skill 改进项都必须在输出中显式说明，不能隐去。
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
- 能接收并落实用户已确认的 skill 改进项。
- 能在输出中显式区分已处理与未处理的 skill 改进项。
- 能输出结构清晰、可执行的 skill 文件。