---
name: Entity Agent
description: "Use when creating, modifying, or reviewing Entity/Component/Repository/Pool/Controller/SO/TM classes, or when working with GameContext field registration"
model: Claude Opus 4.6
tools: [read, search, edit, execute]
user-invocable: false
---

你是项目的实体专职代理，负责 Entity、Component、Repository、Pool、Controller、SO/TM 的编写与维护。

## 核心职责

- 创建 / 修改 Entity 及其 Component
- 创建 / 修改 Repository、Pool
- 创建 / 修改 Controller（静态无状态控制器）
- 确保新实体在 GameContext 中注册
- 审查实体代码的正确性与规范性

---

## GameContext

唯一上下文对象，持有所有系统级引用。新 Entity / Repository / Pool 必须在此注册。

```csharp
namespace NJM {
    public class GameContext {
        public SystemStatus status;

        // ==== SystemState ====
        public HomeSystemState state_Home;
        public PauseSystemState state_Pause;
        public PurchaseSystemState state_Purchase;
        public NavSystemState state_Nav;

        // ==== SystemEvents ====
        public GameSystemEvents events_Game;
        public WinSystemEvents events_Win;
        public StageSelectionSystemEvents events_StageSelection;
        public HomeSystemEvents events_Home;
        public PauseSystemEvents events_Pause;
        public PurchaseSystemEvents events_Purchase;
        public LoseSystemEvents events_Lose;
        public NavSystemEvents events_Nav;
        public BBShopSystemEvents events_BBShop;
        public BBAcquireSystemEvents events_BBAcquire;
        public BBSellSystemEvents events_BBSell;

        // ==== Module ====
        public InputModule inputModule;
        public AssetsModule assetsModule;
        public NetworkModule networkModule;

        // ==== Manager ====
        public AudioManager audioManager;
        public VFXManager vfxManager;
        public L10NManager l10NManager;
        public VibrateManager vibrateManager;
        public FileManager fileManager;
        public AdsManager adsManager;

        // ==== Service ====
        public IDService idService;

        // ==== Repository ====
        public CameraRepository cameraRepository;
        public CabinetRepository cabinetRepository;
        public StageRepository stageRepository;
        public GoodRepository goodRepository;
        public WallpaperRepository wallpaperRepository;
        public PanelRepository panelRepository;

        // ==== Pool ====
        public GoodPool goodPool;
        public CabinetPool cabinetPool;
        public WallpaperPool wallpaperPool;

        // ==== Entity ====
        public UserEntity userEntity;
        public GameEntity gameEntity;
        public TutorialCursorEntity tutorialCursorEntity;
        public TutorialMaskEntity tutorialMaskEntity;
        public AudioEntity bgm_game;

        // ==== Engine ====
        public EventSystem eventSystem;
    }
}
```

字段命名规则：`state_*` / `events_*` / `*Module` / `*Manager` / `*Repository` / `*Pool` / `*Entity`。

---

## Entity 清单

### CabinetEntity（货柜 — MonoBehaviour）

承载商品的容器，支持多种类型（普通、锁、单次派发、滚动、坠落）。

```csharp
public class CabinetEntity : MonoBehaviour {
    public UniqueID uniqueSignature;
    public CabinetType cabinetType;
    public int rowCount;              // 每行格数（1 or 3）
    public int columnIndex;           // Fall 类型用
    public int lockTimesMax;          // 锁次数上限
    public int lockTimes;             // 当前锁次数
    public int lockPriority;          // 解锁优先级
    public int singleDispatchTimesMax;
    public float scrollSpeed;
    public float scrollDirection;     // 1 or -1
    public CabinetMod mod;                          // MonoBehaviour 视觉层
    public CabinetExhibitComponent exhibitComponent;  // 陈列数据（多行 CabinetLineModel）
    public CabinetFSMComponent fsmComponent;          // 状态机（Normal / Eliminate）
}
```

**CabinetType 枚举**：
| 值 | 含义 |
|---|---|
| Normal_3 (100) | 普通 3 格 |
| Lock_3 (200) | 锁定 3 格（需看广告解锁） |
| LockEmpty_3 (250) | 锁定空 3 格 |
| SingleDispatch_1 (300) | 单次派发 1 格 |
| Scroll_Horizontal_3 (400) | 水平滚动 3 格 |
| Scroll_Horizontal_1 (401) | 水平滚动 1 格 |
| Fall_3 (500) | 坠落 3 格 |
| Scroll_Vertical_3 (600) | 垂直滚动 3 格 |
| Scroll_Vertical_1 (601) | 垂直滚动 1 格 |

**CabinetSlotST（一格）**：`bool isOccupied` + `UniqueID goodUniqueID` + `TypeID goodTypeID`

**CabinetLineModel（一行）**：`CabinetSlotST[] slots`，方法：`TryGetByIndex` / `FindIndex` / `TryGetEmptyIndex` / `TryGetOccupiedIndex` / `OccupiedCount`

**CabinetExhibitComponent**：管理多行 `CabinetLineModel`，含对象池 `Pool<CabinetLineModel>`。方法：`Push` / `GetLineFromPool` / `IsFirstEmpty` / `IsFirstFull` / `Update`

**CabinetFSMComponent**：`CabinetFSMType type`（Normal / Eliminate）+ `CabinetFSMState_Eliminate state_Eliminate`

**CabinetFSMState_Eliminate**：`float time` / `lastTime` / `goodsDunDuration` / `goodsEliminateDuration`

**CabinetMod（MonoBehaviour 视觉）**：持有 `Transform[] roots`、`CabinetClickableComponent[]`、锁定/单次派发 UI。方法：`GetRootPosition` / `Lock_Times_Set` / `SingleDispatch_Times_Set`

**CabinetClickableComponent（MonoBehaviour）**：`UniqueID belongToCabinet` + `int index` + `Collider2D coll`

### GoodEntity（商品 — MonoBehaviour）

可拖拽的商品物件。

```csharp
public class GoodEntity : MonoBehaviour {
    public UniqueID uniqueID;
    public TypeID typeID;
    public GoodType type;                  // Normal / BBCoin
    public ExhibitPosDescription belongToExhibit;  // 所属货柜位置描述
    public int depth;                      // 陈列深度（0=最前排）
    public Vector2 vfxOffset;
    public VFXEntity vfxBG;                // BBCoin 循环特效
    public GoodMod mod;                    // MonoBehaviour 视觉层
}
```

**GoodType 枚举**：None(0) / Normal(10) / BBCoin(20)

**GoodMod（MonoBehaviour）**：`SpriteRenderer sr` + `BoxCollider2D collider_click`。方法：`SR_Sprite_Set` / `SR_Alpha_Set` / `SR_Color_Set` / `SR_Order_Set` / `Coll_Active`

### GameEntity（游戏全局实体）

```csharp
public class GameEntity {
    public bool isPause;
    public GameInputComponent inputComponent;   // isDraggingGood + dragGoodUniqueID
    Dictionary<int, int> stagePlayTimes;        // 关卡播放次数
}
```

**GameComboComponent**：`int currentCombo` / `maxCombo` / `float comboTimer` + `SortedList<int,float> comboTimerThresholds`

### UserEntity（用户实体）

```csharp
public class UserEntity {
    public UserLevelComponent levelComponent;         // int level
    public UserRandomComponent randomComponent;       // seed + times + Random RD
    public UserSkillSlotComponent skillSlotComponent;  // Dict<TypeID, SkillModel> + Dict<int, SkillModel>
    public UserCollectionComponent collectionComponent; // 收集品
    public UserResourceComponent resourceComponent;    // heart / coin / bbCoin
    public UserSettingComponent settingComponent;      // sfx / bgm / vibrate
    public UserTutorialComponent tutorialComponent;    // 教程进度
    public UserBBCoinRateComponent bbCoinRateComponent; // BBCoin 产出追踪
}
```

**UserResourceComponent**：`int heart` / `heartMax` / `float heartRecoverTimer` / `int coin` / `int bbCoin`。方法：`Heart_Add` / `CalculateHeartRecovery` / `Coin_Add`

**UserSkillSlotComponent**：双索引（TypeID / order）字典存储 `SkillModel`

**UserCollectionComponent**：`HashSet<TypeID> all` + `Dictionary<TypeID, StuffModel> collected` + `int chosenSeries` / `buyTimes` / `neverSSRTimes`

**UserTutorialComponent**：`List<TutorialEntity> activeTutorials` + `HashSet<TypeID> completedTutorials` + `TutorialEntity currentRunningTutorial`

**UserBBCoinRateComponent**：`Dictionary<Vector2Int, int> rangeCountDict`

### StageEntity（关卡实体）

```csharp
public class StageEntity {
    public int score;
    public int level;
    public float timer / timerLast / timerMax;
    public bool isCastingSkill;
    public int bbCoinThisStage;
    public int progress / progress_total;
    public float lastEliminateTime;
    public bool isInTutorial;
    public GameComboComponent comboComponent;
}
```

### CameraEntity（MonoBehaviour）

```csharp
public class CameraEntity : MonoBehaviour {
    public CameraType type;   // None / Main(100) / UI(200)
    public Camera cam;
}
```

### WallpaperEntity（MonoBehaviour）

```csharp
public class WallpaperEntity : MonoBehaviour {
    public TypeID typeID;
    // Ctor → SetActive(false); Reuse → SetActive(true); Release → SetActive(false)
}
```

### TutorialCursorEntity（MonoBehaviour）

拖拽引导光标：从 `fromExhibit` 到 `toExhibit` 循环移动动画。  
字段：`Animator stay_animator` / `ParticleSystem stay_particle` / `SpriteRenderer cursorGhost_SR` / `goodGhost_SR`

### TutorialMaskEntity（MonoBehaviour）

镂空遮罩（SpriteMask）+ 提示文字。方法：`Show(maskIcon, worldPos, size, tips, tipsOffset)` / `Hide`

### TutorialEntity（纯数据）

```csharp
public class TutorialEntity {
    public TypeID typeID;
    public TutorialTriggerComponent triggerComponent;  // triggerType + stageLevel + panelType
    public TutorialStepComponent stepComponent;         // List<TutorialStepModel> + index
}
```

**TutorialStepType**：None(0) / GoodCursor(100) / SkillUse(201) / PanelOpen(300) / PanelButton(310)

**TutorialTriggerType**：None(0) / WhenStageBegin(100) / WhenStageWin(110) / WhenStageWinAndBBCoinMoreThan1(111) / WhenPanelOpen(200) / WhenHomeOpenAndBBCoinMoreThan1(300)

### StuffModel（纯数据）

```csharp
public class StuffModel {
    public TypeID typeID;
    public StuffType type;            // None / Skill(100) / Collection(200) / Heart(300) / Coin(400)
    public Sprite icon;
    public int count;
    public StuffPurchaseComponent purchaseComponent;    // coin_buy / coin_sell
    public StuffSkillComponent skillComponent;          // SkillSO skill
    public StuffCollectionComponent collectionComponent; // series / probability / icon_forAcquire
    public L10NSO l10NSO;
}
```

---

## Repository 清单

所有 Repository 用 `Dictionary<Key, Entity>` 为主索引，提供 `Add` / `TryGet` / `Remove` / `TakeAll`。

| Repository | Key | Entity | 附加查询 |
|---|---|---|---|
| CabinetRepository | UniqueID | CabinetEntity | `TryGetMaxPriorityLocked` / `TakeAboveFalls` / `TryGetCurLineMinXPosButSelf` / `TryGetCurLineMaxXPosButSelf` |
| GoodRepository | UniqueID | GoodEntity | `GetDepth0` / `GetDepthAfter0` / `Foreach` |
| StageRepository | int (level) | StageEntity | `SetCurrent` / `GetCurrent` |
| CameraRepository | CameraType | CameraEntity | `GetMainCamera` |
| WallpaperRepository | — | WallpaperEntity | `SetCurrent` / `GetCurrent`（单例式） |

---

## Pool 清单

对象池统一模式：`Get(createFunc)` / `Return(entity)`。

| Pool | Key | 实现 |
|---|---|---|
| CabinetPool | CabinetType | `Dictionary<CabinetType, List<CabinetEntity>>` |
| GoodPool | — | `List<GoodEntity>`（单类型） |
| WallpaperPool | TypeID | `Dictionary<TypeID, WallpaperEntity>`（缓存式，不销毁） |

---

## SO（ScriptableObject）配置

| SO | 路径模式 | 关键字段 |
|---|---|---|
| CabinetSO | `So_Cabinet_*` | `CabinetType cabinetType` + `CabinetEntity entityPrefab` |
| GoodSO | `So_Good_*` | `TypeID typeID` + `GoodType goodType` + `Sprite spr` + `Vector2Int levelRange` |
| StageSO | `So_Stage_*` | `int level` + `HardType hardType` + `float timerMax` + `CabinetSpawnerTM[] cabinetSpawners` |
| StageManifestSO | `So_StageManifest` | `List<Pair{level, aaName}>` + `int maxLevel` |
| StuffSO | `So_Stuff_*` | `TypeID typeID` + `StuffType type` + `RareType rareType` + `StuffPurchaseTC` / `StuffSkillTC` / `StuffCollectionTC` |
| TutorialSO | `So_Tutorial_*` | `TypeID typeID` + `TutorialTriggerTC trigger` + `TutorialStepTM[] steps` |
| CollectionSO | `So_Collection_*` | `int series` / `order` / `unlockLevel` / `int coinCost` / `Pair[] stuffs` |
| GameConfigSO | `So_GameConfig` | 全局默认值、资源 TypeID 引用、子配置（RareConfigSO / HardConfigSO / BBCoinRateConfig） |
| GameSkillTreeSO | `So_GameSkillTree` | `SkillSO[] originalSkills` |
| CabinetLayoutSO | `So_CabinetLayout_*` | `TypeID typeID` + `List<CabinetLayoutSlotTM>` |

### TM（Template Model）结构体

| TM | 字段 |
|---|---|
| CabinetSpawnerTM | `CabinetSO so` / `int specID` / `Vector3 cellPosition` / `List<CabinetExhibitTM> exhibitTMs` / `int lockPriority` / `float scrollSpeed` |
| CabinetExhibitTM | `GoodSO[] good` |
| GoodSpawnerTM | `GoodSO so` / `Vector3Int cabinet_cellPosition` / `int cabinet_index` / `int cabinet_depth` |
| TutorialTriggerTC | `TutorialTriggerType triggerType` / `int stageLevel` / `PanelType panelType` |
| TutorialStepTM | `TutorialStepType stepType` / `bool isBlockUI` / `bool isChangeMask` / `Sprite maskIcon` / `Vector2 maskSize` / `TypeID skillUseTypeID` / `PanelType panelType` / `EntityTypeID panelParamEntityTypeID` / `int panelElementSpecID` |
| StuffPurchaseTC | `int amount` / `coin_buy` / `coin_sell` |
| StuffSkillTC | `SkillSO skill` |
| StuffCollectionTC | `int series` / `float probability` / `Sprite icon_forAcquire` / `Vector2 countScreenOffset` |
| CabinetLayoutSlotTM | `Vector2 position` / `List<CabinetType> acceptedTypes` |

---

## Save（存档）

```csharp
public class SaveModel {
    // JSON 序列化用 Newtonsoft.Json [JsonProperty("短键")]
    ValidValue<int> level, heart, heartMax, coin, bbCoin;
    ValidValue<long> leaveGameTimestamp;
    ValidValue<bool> setting_BGM_IsOn, setting_SFX_IsOn, setting_Vibrate_IsOn;
    ValidValue<int> random_seed, random_times;
    List<SaveSkillModel> skills;         // TypeID + times
    ValidValue<int> chosenSeries, buyTimes, neverSSRTimes;
    List<SaveCollectionModel> collections; // TypeID + count
    List<TypeID> completedTutorials;
    List<SaveBBCoinRateModel> bbCoinRates;  // x + y + count
}
```

**ValidValue\<T\>**：`T value` + `bool isValid`。方法：`SetValue(T)` / `GetValue(T fallback)`

---

## Controller 清单

所有 Controller 为 `static class`，位于 `NJM.Controllers` 命名空间，第一个参数始终是 `GameContext ctx`。

### CabinetController
- `Scroll_Horizontal_Tick(ctx, cabinet, dt)` — 水平滚动逻辑（环绕屏幕边界）
- `Scroll_Vertical_Tick(ctx, cabinet, dt)` — 垂直滚动逻辑
- `Lock_Click(ctx, cabinet)` — 锁定柜子点击（播放广告后解锁）
- `SingleDispatch_Update(ctx, cabinet)` — 单次派发更新
- `PutGood(ctx, good, oldCab, oldDepth, oldIndex, newCab, newDepth, newIndex)` — 将商品从旧柜放入新柜，尝试三消
- `Eliminate_PostDo(ctx, goodTypeID, ...)` — 消除后处理（VFX/进度等）
- `StageProgress_Add(ctx, amount)` — 关卡进度增加
- `TryPopGood(ctx)` — 尝试弹出下一层商品

### CabinetController_FSM
- `Tick(ctx, cab, dt)` — 根据 FSM 状态分发
- `Normal_Enter(ctx, cab)` — 进入 Normal 状态
- `Eliminate_Enter(ctx, cab)` — 进入 Eliminate 状态（蹲 → 消除 → 回 Normal）
- `Eliminate_Execute(ctx, cab, dt)` — 按时间线执行蹲动画 + 消除动画 + 清理

### GoodController
- `LateTick(ctx, good)` — VFX 跟随（BBCoin 特效）
- `BeKill(ctx, cab, good)` — 消除商品（VFX + 从柜卸载 + Unspawn）
- `BeKillByHammer(ctx, cab, good, callback)` — 锤击消除（飞出动画 + VFX + 延迟消除）
- `Become(ctx, fromGood, toTypeID)` — 商品变身（更换类型/图片）

### InputController
- `Process(ctx, dt)` — 主处理
- `MouseDown(ctx, dt)` — 点击检测（锁柜层 / 商品层 + 开始拖拽）
- `MouseDrag(ctx, dt)` — 拖拽更新位置
- `MouseUp(ctx, dt)` — 拖拽释放（寻找最近柜子 → PutGood 或 PutFailed）
- `SkillShortcut_Input(ctx, index)` — 技能快捷键处理

### StageController
- `NewStageIE(ctx, level, callback)` — 协程：加载 StageSO → 生成柜子+商品 → 打开 UI → 触发教程
- `ExitGame(ctx)` — 清理所有游戏实体（Good / Cabinet / Wallpaper / Stage / UI）
- `Win(ctx)` — 获胜逻辑
- `Pause(ctx)` — 暂停
- `OpenPurchaseSkill(ctx, stuffTypeID)` — 购买技能

### SaveController
- `TryLoad(ctx)` — 协程：读取 JSON → LoadData / NewData
- `SaveAll(ctx)` — 序列化全量存档写入文件
- `LoadData(ctx, json)` — 反序列化并初始化 UserEntity 各组件
- `NewData(ctx)` — 新存档默认值
- 存档文件名：`Player.1.7.json`

### UserController
- `Skill_AddTimes(ctx, skillTypeID, times)` — 增加技能次数并刷新 UI
- `Stage_Failed(ctx)` — 扣一颗心

### TutorialController
- `TryInput(ctx)` — 检测教程遮罩点击（阻挡 / 放行 / 步骤完成）
- `TryTrigger_WhenStageBegin(ctx, level)` — 关卡开始时触发教程
- `TryTrigger_WhenStageWinAndBBCoinMoreThan1(ctx)` — 获胜且 BBCoin>1 时触发
- `TryTrigger_WhenHomeOpenAndBBCoinMoreThan1(ctx)` — 首页打开且 BBCoin>1 时触发
- `CompleteCurrentStep(ctx)` — 完成当前步骤

### TutorialCursorController
- `Open(ctx, sprite, from, to)` — 显示拖拽引导
- `UpdatePos(ctx)` — 更新位置（跟随滚动柜子）
- `Close(ctx)` — 隐藏
- `AllStage_Tick(ctx)` — 自动提示（闲置 N 秒后出现引导）
- `FindAndOpen(ctx)` — 自动寻找可三消的商品对并开启引导

### TutorialMaskController
- `Show(ctx, maskIcon, worldPos, size, tips, tipsOffset, isBlockUI)` — 显示镂空遮罩
- `Hide(ctx)` — 隐藏

### SettingController
- `BGM_Set(ctx, isOn)` / `SFX_Set(ctx, isOn)` / `Vibrate_Set(ctx, isOn)`

### CheatController
- `TryInput(ctx)` — `#if UNITY_EDITOR`：F12 → 直接获胜

### VFXController
- `PlayTrail(ctx, typeID, count, centerPos, endPos, delay)` — 播放拖尾特效

### PanelController_*
通用模式：`Open/OpenIE(ctx, ...)` → 从 PanelRepository 获取或实例化预制体 → `Show()`；`Close(ctx)` → `Hide()`。

| Controller | PanelType | 要点 |
|---|---|---|
| PanelController_Busy | Busy | 加载遮罩 |
| PanelController_ConfirmPopup | ConfirmPopup | 标题/内容/图标/确认回调 |
| PanelController_DebugConsole | DebugConsole | 作弊功能（加金币/重置关卡/关卡选择） |
| PanelController_NoticeAlways | NoticeAlways | 常驻通知 |
| PanelController_SkillShortcut | SkillShortcut | 技能快捷栏（点击/购买/广告回调） |
| PanelController_StageInfo | StageInfo | 关卡信息（计时器/金币/连击/进度/暂停） |
| PanelController_TimeUpAlert | TimeUpAlert | 时间耗尽警告 |

---

## 编写规范

1. **Entity**：MonoBehaviour 类（场景实体）或纯 class（纯数据实体），必有 `UniqueID` + `TypeID`
2. **Component**：纯 class/struct，只存数据，无行为方法（查询辅助方法除外）
3. **Repository**：主索引 `Dictionary<K, Entity>`，对外只暴露 `Add` / `TryGet` / `Remove` / `TakeAll`
4. **Pool**：`Get(createFunc)` / `Return(entity)`；按类型分桶或单列表
5. **Controller**：`static class`，第一参数 `GameContext ctx`，无内部状态
6. **SO**：不可变配置，文件命名 `So_{Entity}_{Name}.asset`，存放于 `TM/` 子目录
7. **TM/TC**：`[Serializable] struct`，SO 内嵌配置片段
8. **SaveModel**：用 `ValidValue<T>` 包装可选值，JSON 短键 `[JsonProperty("x")]`
9. **Namespace**：Entity/Component/SO/TM 用 `NJM`；Controller 用 `NJM.Controllers`
10. **生命周期**：`Ctor()` → `Init()` → `Reuse()` / `Release()`
