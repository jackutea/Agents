# System.gist

用途：System 主流程 + State + Events 的三件套模板。

参考来源：
- MoodPuzzle/Assets/Src_Runtime/HotReload/Systems_Home/HomeSystem.cs
- MoodPuzzle/Assets/Src_Runtime/HotReload/Systems_Home/HomeSystemState.cs
- MoodPuzzle/Assets/Src_Runtime/HotReload/Systems_Home/HomeSystemEvents.cs

```csharp
using System;
using System.Collections;

namespace NJM.Systems_Home {

    // System: 负责流程编排，不直接持有大状态
    public static class HomeSystem {

        public static void Open(GameContext ctx, Action onOpenDone = null) {
            CoroutineHelper.StartCoroutine(PanelController_Home.OpenIE(ctx, () => {
                onOpenDone?.Invoke();
            }));
            CoroutineHelper.StartCoroutine(PanelController_TopResourceInfo.OpenIE(ctx));
            CoroutineHelper.StartCoroutine(WaitPartCDone(ctx));
            EngineController.FPS_AutoFit(ctx);
        }

        static IEnumerator WaitPartCDone(GameContext ctx) {
            yield return ctx.assetsModule.Wait_PartC_IE();
            var state = ctx.state_Home;
            if (state.bgm == null) {
                state.bgm = ctx.audioManager.Play(ctx.assetsModule.GameConfigSO_Get().bgm_home, 1f);
            } else {
                state.bgm.FadeIn(1f);
            }
        }

        public static void Close(GameContext ctx) {
            PanelController_Home.Close(ctx);
            PanelController_TopResourceInfo.Close(ctx);
        }
    }
}
```

```csharp
namespace NJM {

    // State: 仅保存该系统的跨帧状态
    public class HomeSystemState {
        public AudioEntity bgm;
        public HomeSystemState() { }
    }
}
```

```csharp
using System;

namespace NJM {

    // Events: 统一定义 Handle + Invoke
    public class HomeSystemEvents {

        public Action<bool> OnHeartAddHandle;
        public void OnHeartAddInvoke(bool isAutoStartStage) => OnHeartAddHandle.Invoke(isAutoStartStage);

        public Action OnCoinAddHandle;
        public void OnCoinAddInvoke() => OnCoinAddHandle.Invoke();

        public Action OnStartGameHandle;
        public void OnStartGameInvoke() => OnStartGameHandle.Invoke();

        public HomeSystemEvents() { }
    }
}
```
