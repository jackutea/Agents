# 吸血鬼爬行者（Vampire Crawler）- 设计说明

## 概念概述
- 名称（临时）：吸血鬼爬行者（Vampire Crawler）
- 类型：单人、类爬行地牢（roguelike/roguelite）+ 动作即时战斗（ARPG-lite）
- 目标平台：PC（首要）/ 手柄（次要）/ 从长远考虑移动端适配
- 核心卖点：快速、紧张的近战与技能连携；“吸血”资源作为战斗与成长纽带；每次爬行都有可感知的进步（短中长期成长闭环）。

## 核心体验目标（Design Goals）
- 立刻可上手、难于精通：玩家能在数分钟内理解基础操作，随着解锁技能与装备逐步深挖组合深度。
- 高信息密度战斗：每次交锋都有清晰的攻击预兆、回避节奏与硬币式风险回报（吸血换取短时强化/回血）。
- 节奏分明的爬行循环：短时运行（10–30 分钟一轮）+ 可选的元进度（永久解锁与变式）以提升重复游玩动机。
- 美术氛围：哥特暗黑、血红和冷灰主色调；强调光照与体积感。VFX 为生命吸取、时停、冲刺做突出表现。

## 核心循环（Core Loop）
1. 进入关卡/层（Room/Map）
2. 探索、发现敌人和拾取（物品/血液/单次增益）
3. 击败敌人、触发掉落与吸血机制（即时回血或充能）
4. 消耗血液在房间间或安全点处换取临时/永久强化
5. 达到区段Boss或传送点，决定继续爬行或回撤（若有元进度则存档增益）

## 玩家目标与成功感
- 立即目标：存活并尽可能推进层数，积累更稀有资源。
- 中期目标（会话内）：解锁/试用新的技能与装备组合完成挑战。
- 长期目标（跨会话）：通过永久升级/解锁（新技能/新职业/皮肤）拓展玩法空间，提高再游玩动力。

## 主要玩法元素（概览）
- 近战攻击：轻攻击、重攻击、下段/蹲避攻击（有连击链）。
- 闪避/冲刺：短免伤/无敌帧，消耗耐力或冷却。
- 吸血（核心资源）：击中或特定技能会回复生命并可能产生“血魂”货币。
- 技能树/天赋：分支式解锁，支持自由组合与互斥选项。
- 掉落与装备：武器、饰品、消耗品与稀有掉落，影响战斗节奏与战术选择。

## 控制与输入建议
- PC（键鼠）：移动 W/A/S/D；轻击 LMB；重击 RMB；闪避 Space；技能 Q/E/R；物品 1/2/3；交互 F。
- 手柄：左摇杆移动；RT/按键轻/重击；B/背键闪避；面键技能分配；方向键/摇杆切换物品。
- 响应性：最低输入延迟 100ms 目标，理想 <50ms（高帧率优先）。

## 设计约束与技术假设
- 引擎：以 Unity 为首选（现有团队熟悉度高），实现可在 60fps 下稳定运行。
- 运行设备范围：中端 PC 为基准测试机（独立开发时可在更弱设备上降质）。
- 单机优先：无需初期网络同步。但设计时为将来联机留接口（事件总线、序列化点）。

## 成功度量（KPI / Metrics）
- 首周留存、次日留存（目标：D1 >= 35% 为良好起点）
- 平均会话时长（目标：每轮 10–30 分钟）
- 平均爬行深度（平均玩家到达的最大层数）
- 玩家死亡分布（用于调节难度曲线）

## 初始交付物（给程序 / 美术 / 策划的最小可交付件）
- 程序：玩家控制与基础战斗原型（移动/轻重击/闪避/吸血逻辑）；房间生成器占位器。
- 美术：概念图（角色/敌人/房间主题）、玩家占位精灵（idle/walk/attack/hurt/death，4–8 帧），一套房间地板/墙面贴图占位。
- 内容策划：首套敌人列表（3 种普通 + 1 小 Boss）、随机房间模板（10 个），初版掉落表。

---

_接下来我会写 `# 关键系统` 部分并提交该文件。_

# 关键系统
本节面向程序与系统设计，列出每个需要实现或数据化的子系统、负责人产出、关键接口与验收准则。

### 1) 玩家控制（PlayerController）
- 目标：高响应、可组合的输入体系，支持轻/重攻击、闪避、技能与交互。
- 主要数据：
	- moveSpeed(float)、acceleration(float)、stamina(float)、maxHealth(int)
	- currentState(enum: Idle/Moving/Attacking/Dashing/UsingSkill/Hurt/Dead)
- 关键接口：
	- Move(Vector2 dir)
	- TryAttack(AttackType type)
	- Dash(Vector2 dir)
	- UseSkill(string skillId)
	- ApplyDamage(int amount, DamageContext ctx)
- 验收：玩家输入延迟 <100ms；闪避后短帧无敌窗（config 可调整）；连击与硬直按参数可复现。

### 2) 战斗系统（Combat System）
- 职责：管理伤害计算、命中判定、硬直与击退、暴击、伤害类型、护甲/抗性。
- 伤害流程（建议事件序列）：
	1. 发起攻击 -> 生成 HitBox（基于动画帧）
	2. HitBox 命中目标 -> 触发 OnHit
	3. CombatSystem 计算最终伤害（基础伤害 * (1 - 防御修正) + 额外效果）
	4. 调用 ApplyDamage，触发受击反馈（击退、击退动画、吸血产生）
- 重要参数：hitlag、invulnFrames、staggerThreshold、knockbackForce

### 3) 吸血与资源系统（Health/Blood System）
- 两条核心数值：HP（生命）与 Blood（战斗资源/货币）。
- 吸血规则示例：
	- 普攻命中恢复 HP = floor(damage * 0.15)
	- 特殊技能或暴击触发“血魂”掉落（可作为货币）
- Blood 用途：一次性回血、房间间增益兑换、解锁永久/临时能力（需策划定义）。

### 4) 技能与CD 系统（Skill System）
- 技能数据结构（建议以 ScriptableObject / JSON 存储）：
	- id, name, description, cooldown, cost(blood/stamina), castTime, range, prefab/vfx, tags
- 支持技能组合（被动+主动）与条件触发（onKill, onHurt, onDodge）

### 5) 敌人 AI 与状态机（Enemy AI）
- 常见状态：Idle -> Patrol -> Alert -> Chase -> Attack -> Flee -> Dead
- AI 参数化：detectionRadius, chaseSpeed, attackRange, attackCooldown, aggression
- 行为树/状态机：建议使用状态机 + 可插拔行为（PatrolBehavior、ChaseBehavior、MeleeAttackBehavior）
- 路径：A*（NavMesh/简单网格）或导航点。对小单机项目可用简化寻路/朝向逻辑。

### 6) 遭遇管理（Spawner / Encounter System）
- 每个房间挂一份 Encounter 配置：spawnPoints[], waveTemplates[], trigger（enter/clear/time）
- 支持动态难度调整（根据玩家深度/已击杀数动态提高权重）。

### 7) 随机掉落与道具表（Loot / Item System）
- Rarity tiers: Common, Uncommon, Rare, Epic, Legendary
- 每个敌人/宝箱绑定 DropTable（条目包含 itemId + weight + min/maxCount）。
- 掉落规则需支持“保底”和“碎片/分解合成”机制。

### 8) 房间与关卡生成（Level Generator）
- Room types: Combat, Treasure, Shop/Rest, Trap, MiniBoss, Boss
- 生成算法建议：
	- 概念 1（快速可实现）：预制房间池 + 权重随机布局 + 连通性修正（随机连通）
	- 概念 2（可扩展）：BSP 或 graph-based 区域图 + 程序填充
- 数据：RoomTemplate（size, doorPositions, allowedEncounterTypes, lightProfile）

### 9) UI 管理（UIManager / HUD）
- 事件驱动 UI（通过 EventBus 更新血量/技能冷却/道具栏/提示）。
- 支持可配置、解耦的 UI Component（StatBar, CooldownRing, InventorySlot, Tooltip）。

### 10) 数据驱动与内容表（Data-Driven Design）
- 强制使用数据表（ScriptableObject / JSON / CSV）存储：武器、敌人、房间模板、掉落表、技能表。
- 所有数值应支持热更或 CSV 导入以便策划调平。

### 11) 系统级需求（Pooling, Save, EventBus）
- 对象池：projectiles、VFX、blood-orbs、常驻敌人使用池化，避免频繁 new/destroy。
- 存档：区分 RunState（会话内）与 MetaState（跨会话永久进度），存储格式 JSON，支持快速序列化/反序列化。
- 事件总线：OnEnemyKilled, OnRoomCleared, OnPlayerDamaged, OnItemPicked, OnSkillUsed。

### 12) 性能与限制（Performance Budget）
- 同屏最大活跃敌人目标：12–18（根据机能可调）
- 每帧预算：逻辑 2ms，渲染 8–12ms；目标 60fps（16.7ms/frame）下留裕量。

### 13) 验收标准（Acceptance Criteria）
- 程序：实现 PlayerController + Combat + 基本 AI（至少 3 种敌人）并能跑通一条小关卡。
- 团队：所有数值与表格由策划提交初版，艺术提交占位图集与动画，确认交互与动画帧对齐。

_下一步：写 `# UI 页面清单`，并在写完后提交。_

# UI 页面清单及详情
本节为 UI 设计规范，逐项列出页面/组件、数据接口、交互流程、验收标准及美术产出要求（便于程序/美术/策划直接对接）。

## 全局规范
- 设计语言：暗色系 + 强血红点缀，强调对比与战斗信息可读性。
- 字体：主标题采用衬线或风格化字体（美术提供）；界面正文与数值采用易读无衬线（示例：Noto Sans SC）。
- 参考分辨率：1920x1080。UI 使用 1920 基准，支持 16:9/16:10/4:3 等自适应布局。
- 安全区：边界 32px 内为重要信息禁区。
- 图集与切图：所有图标 PNG/PSD（可导出 2x/1x），UI 元素应支持九宫格缩放（scale9）。

## 页面与组件清单（优先级/详情/数据接口）

- **主菜单（Main Menu）** — 优先级：P0
	- 内容：开始新游戏、继续（若有）、设置、退出、版本号、艺术背景（动态）
	- 数据接口：PlayerProfile.HasSave -> 控制“继续”可见性
	- 验收：点击新游戏进入角色选择或直接开始；UI 动画流畅无遮挡

- **暂停菜单（Pause）** — 优先级：P0
	- 内容：Resume、Settings、Exit to Menu、当前进度快照（层数/击杀数/血量）
	- 交互：按 Esc 或手柄 Start 打开，Resume 恢复时间轴

- **HUD（游戏内）** — 优先级：P0
	- 组件：
		* 血量条（HP）：左上，数值+条形，闪烁警戒色
		* Blood 资源（货币）：HP 旁或下方，以图标+值显示；短时增益提示（浮动数字）
		* 技能栏（Skill Slots）：底部居中，图标 + 冷却环 + 按键提示（键盘/手柄）
		* 消耗品栏：技能栏旁，显示数量和冷却
		* 状态图标（Buff/Debuff）：上方或右侧，以堆叠图标呈现，鼠标悬停显示 tooltip
		* 小地图/房间指示器（可选）：右上，显示已探索房间与传送点
	- 数据接口示例：UIManager.UpdateHP(current, max)、UIManager.UpdateCooldown(skillId, remaining)
	- 验收：所有信息在 1 秒内响应事件；冷却环动画与技能状态保持一致

- **物品/装备页面（Inventory / Equipment）** — 优先级：P1
	- 布局：左右分栏，左侧背包格子（支持拖拽），右侧装备槽（武器/饰品/被动槽）
	- 操作：拖拽、右键使用、售卖/分解、装备比较窗口
	- 数据模型：Item{id, name, type, stats[], rarity, icon, description}
	- 验收：物品悬停显示完整 tooltip，装备切换立即生效（数值刷新）

- **技能树/升级窗口（Skill Tree / Progress）** — 优先级：P1
	- 内容：树状或网格形态的技能节点，节点展示：图标、名称、消耗（血/点数）
	- 交互：解锁/预览/重置（若支持）
	- 数据接口：SkillTable、PlayerSkillPoints

- **商店/祭坛（Shop / Shrine）** — 优先级：P1
	- 内容：物品列、交换/购买按钮、货币显示、随机刷新机制
	- 交互：购买确认、价格显示、稀有度高亮

- **关卡完成/死亡屏（Run Summary / Game Over）** — 优先级：P0
	- 内容：本轮统计（层数、击杀、获得血/货币、掉落重要物品）、回到主菜单、再来一局选项、分享/保存临时成绩

- **提示/浮层组件（Tooltips / Notifications）** — 优先级：P0
	- Tooltip：标题（加粗）、短描述、数值表（属性 + 加成）、来源标注
	- Notification：短时浮动消息（成功拾取/技能触发等），最多同时显示 3 条

## 美术与实现规格（UI）
- 图标规格：64x64 PNG 基准，提供 128x128 备用（用于高 DPI）；图标背景透明。
- HUD 元素：建议导出为 9-slice 可拉伸的 PNG；按钮常规大小 160x48（文本可自适应）。
- 字体大小建议：主标题 28–36px；正文 14–18px；提示 12–14px。

## 交付清单（逐项给程序/美术/策划）
- 程序：提供 UIManager 与基本 HUD 绑定事件（接口见上），并实现悬停/点击事件回调。
- 美术：提供主菜单背景 1920x1080（静态或 30s 循环）、所有 UI 图标（见图标规格表）、按钮/框架样式 PSD。
- 策划：提供初版 SkillTree 布局（节点关系图）、物品描述与翻译文案表（CSV）。

---

_完成 UI 页面清单后将提交，并继续撰写“# 关卡与世界设计”。_

# 关卡与世界设计
本节为关卡设计与生成规范，提供房间模板、遭遇节奏、难度曲线与美术/程序需要的交付格式。

## 设计目标
- 每次爬行都有既定的节奏（探索 - 战斗 - 奖励）
- 房间设计要保证“信息清晰、风险可评估、可读性强”
- 难度随爬行深度渐进，并提供“短期风险/长期收益”的抉择

## 房间类型（Room Types）
- Combat：常规战斗房间（普通小怪，多波/密度可配置）
- Elite：精英怪房间（1–2 个强敌，或带特殊机制）
- MiniBoss：小 Boss 房间（阶段性战斗）
- Boss：区段终结 Boss 房间
- Treasure：高质量掉落（常伴陷阱或谜题以平衡）
- Shop/Rest：提供购买/交易或短暂回复
- Trap：主要为环境伤害/机制作挑战玩家移动与视野

## 房间模板与数据格式（输出给程序/策划）
- 房间模板（示例 JSON）：
```
{
	"id": "combat_small_01",
	"size": [12,8],
	"doors": [{"pos":[0,4],"dir":"left"}],
	"spawnPoints": [{"pos":[6,4],"type":"grunt","count":3}],
	"lightProfile": "dark_candle",
	"treasureSpawns": [{"pos":[10,2],"weight":0.1}]
}
```
- 策划交付：每个模板需包含注释字段（玩法意图、建议敌人等级、期望通关时间）。

## 地图生成算法（建议）
- 阶段 1（布局）：使用预制房间池随机拼接（带权重）；确保连通性并放置 Boss 房间在末端。
- 阶段 2（填充）：根据房间类型填充遭遇（Encounter templates）、掉落与光照。
- 阶段 3（装饰）：放置装饰物、隐藏道具与环境互动点。

## 节奏与遭遇设计（Pacing）
- 一条“区段”包含 6–10 个房间（含 1 个 Boss），平均 10–20 分钟完成。
- 节奏建议：Combat - Combat - Treasure/Shop - Combat - Elite - Boss

## 难度曲线与缩放（Scaling）
- 深度 D 决定基础怪物生命/伤害的增幅：HP = baseHP * (1 + 0.08 * D)
- 难度权重：随着深度增加，增加 Elite 出现概率与群体尺寸。

## 地图与光照需求（美术）
- 每个房间需标注光源位置、遮挡物与层级（foreground/midground/background）。
- 动态灯光建议：重点光源分辨率 1024；影子用于重要区域提示。

## 策划产出清单（每个区段）
- 房间模板（至少 12 个，可复用）
- 遭遇模板（10–20 个，含不同难度/变体）
- 掉落表（分层，含稀有度权重）

## 验收标准
- 能生成一条包含 8 房间 + 1 Boss 的可通关路线，且每种房间类型能正确加载对应遭遇与掉落。

---

_完成“关卡与世界设计”后提交，并继续“# 敌人/单位设计”。_

# 敌人 / 单位设计
本节为内容策划与程序实现提供可直接落地的敌人模板、行为定义与生成规则。

## 敌人设计字段（每个敌人模板必须包含）
- id: string
- name: 展示名
- archetype: grunt / elite / miniBoss / boss / special
- baseHP: int
- moveSpeed: float
- damage: int
- attackRange: float
- attackCooldown: float
- detectionRadius: float
- behavior: (详见行为库)
- lootTable: id
- animations: {idle, walk, attack, hurt, death}

## 敌人原型示例

- **Grunt - 血徒 (blood_grunt)**
	- 描述：近战普通小怪，群体出现，用于填充战斗房间
	- baseHP: 30; moveSpeed: 3.2; damage: 6; attackCooldown: 1.0; detectionRadius: 6
	- 行为：Patrol -> Detect -> Chase -> MeleeAttack
	- 掉落：低概率掉落消耗品，常规金钱

- **Bat Swarm - 蝙蝠群 (bat_swarm)**
	- 描述：空中单位，群体飞行，瞬时高移动
	- baseHP: 10; moveSpeed: 5.0; damage: 4; attackCooldown: 0.8; detectionRadius: 5
	- 行为：群体AI（简单偏移群体行为），对近战玩家具有高威胁

- **Vampire Knight - 吸血骑士 (vamp_knight)**
	- 描述：精英，拥有冲锋与破防技
	- baseHP: 120; moveSpeed: 2.6; damage: 18; attackCooldown: 1.6; detectionRadius: 7
	- 行为：Patrol -> Aggro -> TelegraphedCharge -> StaggerOnHit
	- 特殊：被击中时有 20% 吸血转化为自身短时护盾

- **Blood Wraith - 血影（miniBoss）**
	- 描述：小 Boss，有两阶段战斗（近战与召唤）
	- phase1HP: 200 -> phase2HP: 250
	- 技能：瞬移、召唤小怪、吸血领域（持续伤害 + 吸血）

- **区段 Boss（示例）**
	- 设计：三阶段战斗；每阶段切换攻击模式与场地障碍交互
	- 输出：完整战斗脚本需含阶段阈值、技能循环、躲避窗口、易伤时刻

## AI 状态机示例（伪码）
```
state = Idle
on Update:
	if state == Idle and detectPlayer(): state = Alert
	if state == Alert and canReachPlayer(): state = Chase
	if state == Chase and withinAttackRange(): state = Attack
	if state == Attack and attackCooldownReady(): performAttack()
	on Hurt: maybe Stagger
	on Death: state = Dead; spawnLoot()
```

## 碰撞、判定与动画对齐（美术与程序注意点）
- 所有攻击需有对应 HitBox 帧（动画帧索引）映射表，策划需在 Figma/CSV 中给出帧数。
- Hurtbox 与碰撞层定义：Player Hurtbox，Enemy Hurtbox，Enemy Hitbox，Projectile Hitbox。

## 遭遇构成规则（Room Composition）
- 普通房间：3–6 个 grunt 或 1 精英 + 2 grunt
- 精英房间：1 elite + 2 swarm / 3 grunt（根据深度权重浮动）
- MiniBoss 房间：1 miniBoss + 辅助杂兵

## 掉落与奖励策略
- 每种敌人绑定 DropTable（权重/稀有度）。精英掉落概率更高且有底池保底机制。

## 验收标准
- 每个敌人模板可通过 JSON/ScriptableObject 实例化并在预制房间中正常刷出与战斗。
- 行为可在单关卡环境中复现，伤害/HP 与预期数据一致。

---

_写完“敌人/单位设计”后提交，并继续“# 进度与成长”。_

# 进度与成长（Progression & Growth）
本节定义玩家成长的短期（会话内）与长期（跨会话）系统、货币与升级路线，确保策划/程序/美术可以并行实现。

## 核心概念
- Run Progress（会话内）：玩家在一轮爬行中获得的临时升级（技能、消耗品、临时属性）。
- Meta Progress（跨会话）：永久解锁（新职业、永久被动、皮肤、商店折扣等）。

## 货币体系
- Blood（战斗资源）：会话内主要资源，用于现场治疗/兑换临时强化。
- Blood Shards（碎片/元货币）：稀有，跨会话累积用于永久解锁。
- Gold / Echoes（可选）：用于商店常规购买。

## 经验与等级（若采用）
- 会话内经验用于短期升级（每升一级获得点数用于解锁技能或提升基础属性）。
- 经验公式示例：ExpToLevel(n) = floor(50 * 1.12^(n-1))

## 技能树与天赋（Design）
- 结构：分支式树（主动/被动/战术），节点需标注消耗与互斥关系。
- 解锁方式：技能点 / 消耗 Blood Shards（取决于长期/短期）

## 装备与强化
- 装备分类：武器、护甲、饰品（每类影响不同战斗维度）。
- 强化系统：消耗相同装备或特殊材料提升等级（可选）。

## 平衡与公式（示例）
- 敌人伤害随深度线性增长：Damage = baseDamage * (1 + 0.06 * Depth)
- 掉落稀有度随深度提升：RareChance = base + 0.01 * Depth

## 升级/重置策略
- 元进度保底：在一定次数失败后给出保底碎片，避免长期流失感。

## 策划交付（产物）
- 技能点曲线表（CSV）
- 货币产量与消费表（每层平均产出、重要支出点）
- 初版平衡数值（等级/伤害/血量/掉落概率）

## 验收条件
- 程序可加载并保存 MetaState，且 MetaState 的解锁在游戏主界面可见。
- 会话内等级/技能解锁顺畅、数值变化即时反映在 UI 上。

---

_完成“进度与成长”后提交，下一步写 “# 技术细节”。_

# 技术需求与关键系统详细设计
本节为程序员提供可直接落地的技术规格、类/模块清单与数据结构样例，便于实现与代码评审。

## 项目结构建议（Unity）
- Assets/
	- Scripts/
		- Core/ (EventBus, Save, Pooling)
		- Player/ (PlayerController, PlayerCombat)
		- Enemy/ (AI, EnemyController)
		- Level/ (RoomTemplate, LevelGenerator)
		- UI/ (UIManager, HUD)
		- Data/ (ScriptableObjects, JSON loaders)
	- Art/
	- Prefabs/

## 关键类与接口（概要）
- `IEntity`：ID, Health, ApplyDamage(), OnDeath()
- `PlayerController`：Move/Attack/Dash/UseSkill
- `EnemyController`：StateMachine, PerformAttack
- `CombatSystem`：ResolveHit(hitContext)
- `LevelGenerator`：Generate(seed)
- `UIManager`：Register/Unregister events, UpdateHUD
- `SaveManager`：SaveRunState(), LoadRunState(), SaveMeta(), LoadMeta()

## 事件总线示例（Event Names）
- OnEnemySpawned(EnemyId, RoomId)
- OnEnemyKilled(EnemyId, KillerId)
- OnPlayerDamaged(amount, attackerId)
- OnItemPicked(itemId)

## 数据结构示例（JSON / ScriptableObject）
- Skill SO:
	- id, name, cooldown, cost, prefabRef, tags
- Enemy JSON:
	- id, prefabRef, baseHP, aiProfile, lootTable

## 存档格式（示例 JSON）
```
RunState: {
	player: {hp, pos, skills, inventory},
	currentFloor: 3,
	seed: 12345,
	clearedRooms: ["r001","r002"]
}
MetaState: {
	unlockedSkills: ["leech_strike"],
	shards: 12
}
```

## 池化与性能
- 建议对弹道、VFX、血魂、常驻敌人使用对象池；每类对象预分配 N 个（N 可配置）。
- 使用 Unity Profiler + 自定义 Telemetry（每帧记录活跃实体数、GC 分配、主要方法耗时）。

## 测试与调试工具
- 开发命令：spawn_enemy(id), grant_item(id), advance_floor()
- 日志：统一日志前缀（[Combat], [AI], [Level]）便于追踪

## 推荐第三方库与中间件
- Addressables（资源管理）、DOTween（动画）、Cinemachine（镜头管理，可选）

## 接口契约示例（C# 风格伪代码）
```csharp
public interface IEntity {
	string Id {get;} int HP {get;}
	void ApplyDamage(int amount, DamageContext ctx);
	event Action<IEntity> OnDeath;
}

public class CombatSystem {
	public void ResolveHit(HitContext ctx) {
		var dmg = Calculate(ctx);
		ctx.Target.ApplyDamage(dmg, ctx.damageContext);
		if(ctx.Source is Player) OnEnemyHurt?.Invoke(...);
	}
}
```

## 验收标准（技术）
- 程序实现能在开发机上稳定运行 60fps，且核心模块（Combat/Level/AI）均有单元或集成测试。

---

_完成“技术细节”后提交，下一步为“# 美术资源需求”。_

# 美术资源需求（Art & Assets）
本节为美术提供详细的交付规格表与命名规范，确保程序能直接使用贴图、动画与 VFX。

## 总体风格与色彩
- 风格：哥特暗黑 + 手绘质感（高对比，强调光影）。
- 主色板建议：
	- 主色：#5B0E0E（血红深色）
	- 辅色：#111218（近黑）
	- 高光：#EFA7A7（淡血光）
	- 次要：#6B828C（冷灰）

## 导出与技术要求
- 文件格式：
	- 精灵/贴图：PNG（支持透明），PSD 源文件归档保存
	- UI 图标：PNG 64/128/256 像素三套
	- VFX：SpriteSheet 或 Particle Texture（PNG）+ optional normal map (PNG)
	- 音频：WAV（开发）/OGG（发布）
- Unity PPU（Pixels Per Unit）：建议 100 PPU 为基础，可在团队中统一
- 命名规范：<type>_<subtype>_<action>_<frame>.<ext>
	- 例如：char_player_idle_01.png; enemy_vamp_knight_attack_03.png

## 角色与动画（最低产出）
- 玩家（Player）
	- 动作集：idle(4), walk(8), run(8), light_attack(6), heavy_attack(8), dash(6), hurt(4), death(8)
	- Sprite 帧建议：以 8 帧/动作 为起点，部分动作（连击）可用 12–16 帧
	- 绑定点：root（脚下中心）、weapon_hand（武器挂点）、vfx_attach（特效挂点）

- 敌人（按原型）
	- Grunt：idle(4), walk(6), attack(6), hurt(3), death(6)
	- Bat Swarm：flap(6)（使用 tiling + shader 组合呈现群体）
	- Vampire Knight：idle(4), walk(8), charge(10), heavy_attack(10), hurt(4), death(8)

## 场景与装饰
- 房间地板/墙面：可瓦片化 TileSet，常用瓦片尺寸 32x32 或 64x64（依据 PPU）
- 道具/遮挡：分为前景（遮挡玩家）、中景、背景三层

## VFX（特效）
- 核心特效：
	- 吸血特效（吸血光束 + 回血粒子）: Sprite Sheet 32–48帧，尺寸 256x256
	- 攻击冲击：短时泡影 8–12 帧
	- 技能投射体：带尾迹的粒子图
- 要求：提供透明 PNG 序列或合并 SpriteSheet，并注释 pivot 与播放帧率（fps）

## UI 资源
- 图标集：所有技能/物品图标 64x64 PNG，命名为 item_<id>_icon.png
- HUD 元素：分层 PSD，按钮、边框、按钮按下状态（3 状态）

## 音频（简要）
- 每个攻击/技能一个短 SFX（0.1–0.6s），每个 Boss 一个主题音乐（loop）

## 交付清单（最小）
- 玩家占位动画组（见上）
- 三种普通敌人动画组、两种精英/小 Boss 动画组
- 房间 TileSet（至少 1 套主题）
- HUD 图标与主菜单背景 PSD
- VFX 核心 3 个（吸血、冲击、冲刺）

## 验收标准
- 所有 PNG/PSD 命名符合规范、帧数与挂点说明齐全；程序可在不改动资源的情况下加载并播放动画。

---

_完成“美术资源需求”后提交，接着撰写“# 内容策划（场景/任务/叙事）”。_

# 内容策划（场景 / 任务 / 叙事）
本节为内容策划提供任务模板、叙事钩子、关卡事件与文案产出规范，确保程序与美术能直接使用文案与事件数据。

## 叙事与世界观（Pitch）
- 世界设定（简短）：一座被诅咒的城邑向下扩展成无数迷宫地下层，吸血鬼的诅咒蔓延，玩家作为被诅咒者之一，必须在吸血的同时寻找解脱之法。
- 主题要点：罪与救赎、代价与选择、月下的孤独感

## 场景钩子（示例）
- 废弃礼拜堂：光源稀少，触发“被祝福的火炬”机关可减少诅咒强度
- 血之庭院：中央喷泉为吸血池，吞噬或牺牲产生不同奖励路线

## 任务模板（Design Template，交付给程序/策划的 CSV）
- 字段：id, title_key, description_key, trigger (enter/kill/talk), target, reward, repeatable

## 关卡事件脚本（事件样例）
- 事件：房间开启后 10s 触发陷阱 -> 延迟 2s 敌人从天台掉落 -> 若玩家站在中心触发额外精英出现

## 文案与本地化规范
- 使用 Key-Value 格式：ui.menu.start = "开始游戏"，story.node1.title = "堕落之门"
- 文案长度：UI 文案 < 60 字；Tooltip < 140 字；对话无长度硬限制但需分段

## 道具/物品描述示例
- item.leech_blade.name = "汲血之刃"
- item.leech_blade.desc = "击中敌人时回复 15% 伤害为生命。"

## 剧情与任务产出清单
- 初版 6 个场景钩子（每个 1–2 段剧情）、10 个任务模板、30 条物品描述、成就/挑战清单

## 验收标准
- 策划 CSV 导入后，事件触发与奖励发放与文案展示均能在运行时被读取并正确显示。

---

_完成内容策划后提交，并开始撰写 Milestone & TODO 清单（含分工与验收）。_








