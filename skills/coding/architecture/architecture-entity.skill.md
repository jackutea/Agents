---
name: architecture-entity
description: "用于架构层的 Entity/Component/Repository/Pool/Controller/SO/TM 设计与实现，适用于输出详细模板、命名规则与生命周期约束。"
---

# Architecture Entity Skill

此 skill 提取了 Architecture 领域内 Entity/Component/Repository/Pool/Controller/SO/TM 的详细实现规范与模板。

## Entity + Component

### 模板

- **场景实体**（MonoBehaviour）：挂在 GameObject 上，有视觉表现
- **纯数据实体**（class）：无 MonoBehaviour，纯内存对象

```csharp
public class {Entity}Entity : MonoBehaviour {
    public UniqueID uniqueID;
    public TypeID typeID;
    public {Entity}Mod mod;
    public {Entity}{Aspect}Component {aspect}Component;

    public void Ctor() { /* 构造 Component */ }
    public void Init(int entityID) { /* 分配 UniqueID，从 SO 赋值 */ }
    public void Reuse() { gameObject.SetActive(true); }
    public void Release() { gameObject.SetActive(false); }
}

public class {Entity}Entity {
    public UniqueID uniqueID;
    public TypeID typeID;
    public {Entity}{Aspect}Component {aspect}Component;

    public {Entity}Entity() { /* 构造 Component */ }
}
```

### Component 规范

- 纯 class 或 struct，只存数据
- 允许查询辅助方法，不含业务逻辑
- 命名：`{Entity}{Aspect}Component`

### Mod 规范（视觉层）

- MonoBehaviour，持有 SpriteRenderer/Collider/UI 等引用
- 只做视觉操作
- 命名：`{Entity}Mod`

## Repository

主索引 `Dictionary<UniqueID, {Entity}Entity>`，提供 `Add` / `TryGet` / `Remove` / `TakeAll`。
可按查询需求添加附加索引（如 `byTypeID`、`byCategory`）。

```csharp
public class {Entity}Repository {
    Dictionary<UniqueID, {Entity}Entity> all;
    {Entity}Entity[] tempArray;

    public void Add({Entity}Entity entity) { ... }
    public bool TryGet(UniqueID id, out {Entity}Entity entity) { ... }
    public void Remove(UniqueID id) { ... }
    public int TakeAll(out {Entity}Entity[] entities) { ... }
}
```

单例式 Repository（全局唯一实体）可使用 `SetCurrent` / `GetCurrent` 模式。

## Pool

对象池统一模式：`Get(createFunc)` / `Return(entity)`。

```csharp
public class {Entity}Pool {
    List<{Entity}Entity> pool;
    public {Entity}Entity Get(Func<{Entity}Entity> createFunc) { ... }
    public void Return({Entity}Entity entity) { ... }
}

public class {Entity}Pool {
    Dictionary<{Type}, List<{Entity}Entity>> poolDict;
    public {Entity}Entity Get({Type} type, Func<{Entity}Entity> createFunc) { ... }
    public void Return({Entity}Entity entity) { ... }
}
```

## SO（ScriptableObject）配置

Entity 的不可变配置模板，存放于 `TM/` 子目录。

```csharp
[CreateAssetMenu(fileName = "So_{Entity}_", menuName = "NJM/{Entity}SO")]
public class {Entity}SO : ScriptableObject {
    public TypeID typeID;
    public {Entity}Entity entityPrefab;
    // ... 配置字段
}
```

命名规则：`So_{Entity}_{Name}.asset`

### TM / TC（Template Model / Template Component）

SO 内嵌的配置片段，用 `[Serializable] struct`。

```csharp
[Serializable]
public struct {Feature}TM {
    public {Entity}SO so;
    // ... 配置字段
}

[Serializable]
public struct {Feature}TC {
    // ... 组件级配置字段
}
```

## Controller

静态无状态控制器，第一参数始终是 `GameContext ctx`。

```csharp
namespace NJM.Controllers {
    public static class {Entity}Controller {
        public static void Tick(GameContext ctx, {Entity}Entity entity, float dt) { ... }
    }
}
```

### Controller 典型方法

- `Tick(ctx, entity, dt)`
- `Spawn(ctx, so)`
- `Unspawn(ctx, entity)`

### FSM Controller

```csharp
public static class {Entity}Controller_FSM {
    public static void Tick(GameContext ctx, {Entity}Entity entity, float dt) {
        switch (entity.fsmComponent.type) {
            case {FSM}Type.StateA: StateA_Execute(ctx, entity, dt); break;
            case {FSM}Type.StateB: StateB_Execute(ctx, entity, dt); break;
        }
    }
}
```

### PanelController

通用模式：`Open/OpenIE(ctx, ...)` → 从 PanelRepository 获取或实例化预制体 → `Show()`；`Close(ctx)` → `Hide()`。

```csharp
public static class PanelController_{Panel} {
    public static void Open(GameContext ctx) {
        ctx.panelRepository.TryGet<Panel_{Panel}>(PanelType.{Panel}, out var panel);
        if (panel == null) {
            // 加载预制体 → Instantiate → Ctor → 注册回调 → Set to Repository
        }
        panel.Show();
    }
    public static void Close(GameContext ctx) {
        if (ctx.panelRepository.TryGet<Panel_{Panel}>(PanelType.{Panel}, out var panel)) {
            panel.Hide();
        }
    }
}
```

### SaveController

- `TryLoad(ctx)`
- `SaveAll(ctx)`

```csharp
[Serializable]
public struct ValidValue<T> {
    [JsonProperty("v")] public T value;
    [JsonProperty("i")] public bool isValid;
    public void SetValue(T newValue) { value = newValue; isValid = true; }
    public T GetValue(T fallback) { return isValid ? value : fallback; }
}
```

## 编写规范

1. Entity：MonoBehaviour 类或纯数据类，必有 `UniqueID` + `TypeID`
2. Component：纯 class/struct，只存数据，无行为
3. Repository：主索引 `Dictionary<K, Entity>`；对外暴露 `Add` / `TryGet` / `Remove` / `TakeAll`
4. Pool：`Get(createFunc)` / `Return(entity)`
5. Controller：`static class`，第一参数 `GameContext ctx`，无内部状态
6. SO：不可变配置，文件命名 `So_{Entity}_{Name}.asset`
7. TM/TC：`[Serializable] struct`
8. SaveModel：用 `ValidValue<T>` 包装可选值
9. Namespace：Entity/Component/SO/TM 用 `NJM`；Controller 用 `NJM.Controllers`
10. 生命周期：`Ctor()` → `Init()` → `Reuse()` / `Release()`
