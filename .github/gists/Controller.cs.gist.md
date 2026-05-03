# Controller.gist

用途：Controller 控制器模板（完全参考 Wu2 项目工程架构）。
在 Wu2 架构中，Controller 负责封装业务实体的生命周期（Spawn / Unspawn）、状态机的更新流转（FSM FixTick / Enter / Execute），以及各类核心业务逻辑（如技能释放、输入处理、碰撞判定）。

## 核心规范
1. **命名空间**：直接归属于对应的系统级命名空间（例如 `NJM.Systems_Game`），不再强制划分到独立的 `.Controllers` 下。
2. **纯静态类**：所有方法为 `static`，且首个参数永远是系统上下文环境（例如 `GameSystemContext`），其次才是要操作的具体实体或参数。
3. **闭环生命周期**：由 Controller 的 `Spawn` 负责向 Factory 申请创建、从 SO 捞取配置、填充组件、添入 Repository 并触发 FSM 的 Enter。由 `Unspawn` 负责从 Repository 移除并调用实体的 `TearDown` 析构。
4. **FSM 编排收口**：状态机的逐帧派发流转（如 `FSM_FixTick` 对应各个状态的 _Execute）由 Controller 本身来编排调度。
5. **代码分块**：广泛使用 `#region` 划分生命周期、FSM 各状态及附属计算。

```csharp
using System;
using UnityEngine;

namespace NJM.Systems_Game {

    public static class ExampleController {

        #region Spawn & Unspawn
        /// <summary>
        /// 生成实体的主入口
        /// </summary>
        public static ExampleEntity Spawn(GameSystemContext ctx, UniqueID uniqueID, TypeID typeID) {
            // 1. 获取配置数据
            bool has = ctx.assetModule.ExampleSO_TryGet(typeID, out var so);
            if (!has) {
                Debug.LogError($"ExampleController: ExampleSO not found for typeID {typeID}");
                return null;
            }

            // 2. 将创建委托给 Factory
            var entity = EntityFactory.Example_Create(ctx.assetModule, typeID);

            // 3. 基础设置与组件填充
            entity.Setup(uniqueID, typeID);
            var tm = so.tm;
            entity.attributeComponent.FromTM_Float(tm.floatAttributes);

            // 4. 触发初始状态
            FSM_Normal_Enter(ctx, entity);

            // 5. 注册到系统级 Repository
            ctx.exampleRepository.Add(entity);

            return entity;
        }

        /// <summary>
        /// 销毁实体
        /// </summary>
        public static void Unspawn(GameSystemContext ctx, ExampleEntity entity) {
            ctx.exampleRepository.Remove(entity);
            entity.TearDown();
        }
        #endregion

        #region FSM: Tick Routes
        public static void FSM_FixTick(GameSystemContext ctx, ExampleEntity entity, float fixdt) {
            var status = entity.stateComponent.status;
            if (status == ExampleStatus.Normal) {
                FSM_Normal_Execute(ctx, entity, fixdt);
            } else if (status == ExampleStatus.Casting) {
                FSM_Casting_Execute(ctx, entity, fixdt);
            }

            // 无视状态的通用逻辑更新（如：CD、Buff跳字倒计时等）
            FSM_Any_Execute(ctx, entity, fixdt);
        }
        #endregion

        #region FSM: Any
        static void FSM_Any_Execute(GameSystemContext ctx, ExampleEntity entity, float fixdt) {
            // 技能等定时器的刷新
            // 碰撞体退出事件的结算等
        }
        #endregion

        #region FSM: Normal
        public static void FSM_Normal_Enter(GameSystemContext ctx, ExampleEntity entity) {
            entity.stateComponent.Normal_Enter();
            entity.Anim_PlayIdle();
        }

        static void FSM_Normal_Execute(GameSystemContext ctx, ExampleEntity entity, float fixdt) {
            // 在 Normal 状态下，尝试响应业务动作（如移动/跳跃/开火等）
            Move_TryMoveByInput(ctx, entity, fixdt);
            Action_TryCastByInput(ctx, entity, fixdt);
        }
        #endregion

        #region FSM: Casting
        public static void FSM_Casting_Enter(GameSystemContext ctx, ExampleEntity entity /*, 相关参数 */ ) {
            entity.stateComponent.Casting_Enter();
        }

        static void FSM_Casting_Execute(GameSystemContext ctx, ExampleEntity entity, float fixdt) {
            // 处理施法前摇、后摇或打断等判定
        }
        #endregion

        #region Common Behaviours
        static void Move_TryMoveByInput(GameSystemContext ctx, ExampleEntity entity, float fixdt) {
            // 获取按键，设置位移
        }

        static void Action_TryCastByInput(GameSystemContext ctx, ExampleEntity entity, float fixdt) {
            // 尝试触发释放行为
        }
        #endregion
    }
}
```
