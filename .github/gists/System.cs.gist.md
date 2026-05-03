# System.gist

用途：System 主流程编排 + Events 的结构模板。主要用于定义生命周期（Tick / FixTick / LateTick）或操作链路的顶层入口，负责分发状态流转，不直接持有大范围状态。
注意：本层通常通过调用各个 `Controller` 完成具体逻辑，主要侧重输入分发及不同更新时机的路由。

```csharp
using System;

namespace NJM {

    // System: 核心周期编排、大流程控制、输入前处理与事件分发路由
    public static class GameSystem {

        public static void Tick(GameContext ctx, float dt) {
            // 保护机制，如果系统没在运行等特定状态则跳过
            if (ctx.status != SystemStatus.Running) {
                return;
            }

            ProcessInput(ctx, dt);
            PreTick(ctx, dt);
        }

        public static void FixTick(GameContext ctx, float fixdt) {
            StageController.TimerTick(ctx, fixdt);
            
            // 分发下游 Controller 处理对应实体的独立生命周期
            var cabinets = ctx.cabinetRepository.GetList();
            for (int i = cabinets.Count - 1; i >= 0; i--) {
                var cabinet = cabinets[i];
                CabinetController_FSM.Tick(ctx, cabinet, fixdt);
            }
        }

        static void ProcessInput(GameContext ctx, float dt) {
            InputController.Process(ctx, dt);
        }

        static void PreTick(GameContext ctx, float dt) {
            var inputModule = ctx.inputModule;
            // 对于输入的细化处理和状态流转，在主 Controller 中聚合
            if (inputModule.MouseStatus == InputMouseStatus.DownFirst) {
                InputController.MouseDown(ctx, dt);
            } else if (inputModule.IsDragging) {
                InputController.MouseDrag(ctx, dt);
            } else if (inputModule.MouseStatus == InputMouseStatus.Up) {
                InputController.MouseUp(ctx, dt);
            }
        }

        public static void LateTick(GameContext ctx, float dt) {
            // 所有更新完毕后，更新状态展示、UI 和视角跟进等
            PanelController_StageInfo.Update(ctx);
        }

        #region 大流程控制 (Stage流转等)
        public static void NewStageCo(GameContext ctx, int level, Action callback) {
            CoroutineHelper.StartCoroutine(StageController.NewStageIE(ctx, level, callback));
        }

        public static void ExitStage(GameContext ctx) {
            ctx.status = SystemStatus.Stopped;
            StageController.ExitGame(ctx);
        }
        #endregion
    }
}
```

```csharp
using System;

namespace NJM {

    // Events: 统一定义该系统广播给其他系统或顶层调用的事件流（系统间解耦交互）
    public class GameSystemEvents {

        public Action<StageEntity> OnWinHandle;
        public void Win(StageEntity stage) => OnWinHandle?.Invoke(stage);

        public Action<int> OnLoseHandle;
        public void Lose(int reasonType) => OnLoseHandle?.Invoke(reasonType);

        public Action OnPauseHandle;
        public void Pause() => OnPauseHandle?.Invoke();

        public GameSystemEvents() { }
    }
}
```
