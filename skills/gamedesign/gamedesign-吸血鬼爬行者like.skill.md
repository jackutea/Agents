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

