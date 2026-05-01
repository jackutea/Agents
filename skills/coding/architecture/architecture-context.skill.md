---
name: architecture-context
description: "用于架构上下文与 GameContext 注册规范，适用于定义状态、事件、模块、管理器、仓储、对象池和全局实体的注册边界与命名规则。"
---

# Architecture Context Skill

此 skill 定义了 GameContext 与架构上下文注册规范，用于保证架构层的对象注册、依赖方向和命名一致性。

## GameContext 规范

唯一上下文对象，持有系统级引用。

```csharp
public class GameContext {
    public SystemStatus status;

    // ==== SystemState（每个 System 各一份）====
    public {F}SystemState state_{F};
    public {G}SystemState state_{G};

    // ==== SystemEvents（每个 System 各一份）====
    public {F}SystemEvents events_{F};
    public {G}SystemEvents events_{G};

    // ==== Module（低层基础设施）====
    public InputModule inputModule;
    public AssetsModule assetsModule;

    // ==== Manager（高层业务服务）====
    public AudioManager audioManager;
    public VFXManager vfxManager;

    // ==== Service ====
    public IDService idService;

    // ==== Repository ====
    public {Entity}Repository {entity}Repository;
    public PanelRepository panelRepository;

    // ==== Pool ====
    public {Entity}Pool {entity}Pool;

    // ==== Entity（全局唯一实体）====
    public UserEntity userEntity;
    public GameEntity gameEntity;

    // ==== Engine ====
    public EventSystem eventSystem;
}
```

## 注册与命名规则

- 所有 `Repository` / `Pool` / `Entity` 实例或集合必须在 `GameContext` 中注册。
- `GameContext` 字段命名规则：`state_*` / `events_*` / `*Module` / `*Manager` / `*Repository` / `*Pool` / `*Entity`。
- `GameContext` 仅用于上层编排侧，禁止继续下传给 `Entity` / `Component` / `SO` / `Repository` 等低层。

## 上下文边界

- `GameContext` 只属于编排层入口。可传入 `System` / `Controller` / `Manager`，但不得传入纯数据层对象。
- 跨系统通信优先使用显式声明的 `SystemEvents`，避免使用通用消息总线。
- `Entity`、`Component`、`SO`、`Repository` 等低层对象不得依赖或感知 `GameContext`。

## 使用场景

- 设计新的 `Entity` / `Repository` / `Pool` 时，先检查是否需要在 `GameContext` 添加字段。
- 注册全局唯一实体时，使用明确命名字段，并保持可读性。
- 架构调整时，不要在低层类型中注入 `GameContext`。
