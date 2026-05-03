# Controller.gist

用途：Controller 协调模板（调用 Domain / Repository / Manager，封装流程型业务动作）。

参考来源：
- MoodPuzzle/Assets/Src_Runtime/HotReload/Controllers/GoodController.cs

```csharp
using System;
using System.Collections;
using UnityEngine;
using NJM.Domains;

namespace NJM.Controllers {

    public static class GoodController {

        public static void LateTick(GameContext ctx, GoodEntity good) {
            if (good.vfxBG == null) {
                return;
            }

            bool shouldShow = good.depth <= 0;
            if (good.vfxBG.gameObject.activeSelf != shouldShow) {
                good.vfxBG.gameObject.SetActive(shouldShow);
            }
            good.vfxBG.transform.position = good.transform.position + (Vector3)good.vfxOffset;
        }

        public static void BeKill(GameContext ctx, CabinetEntity cab, GoodEntity good) {
            var config = ctx.assetsModule.GameConfigSO_Get();
            ctx.vfxManager.Play(config.vfx_match3_eliminate, good.transform.position);
            cab.Good_Eliminate(good.belongToExhibit.depth, good.belongToExhibit.slotIndex);
            GoodDomain.Unspawn(ctx.vfxManager, ctx.goodRepository, ctx.goodPool, good);
        }

        public static void BeKillByHammer(GameContext ctx, CabinetEntity cab, GoodEntity good, Action callback) {
            var config = ctx.assetsModule.GameConfigSO_Get();
            ctx.vfxManager.Play(config.vfx_skill_hammer_kill, good.transform.position);
            CoroutineHelper.StartCoroutine(KillByHammerIE(ctx, cab, good, callback));
        }

        static IEnumerator KillByHammerIE(GameContext ctx, CabinetEntity cab, GoodEntity good, Action callback) {
            yield return new WaitForSeconds(1f);
            BeKill(ctx, cab, good);
            callback?.Invoke();
        }
    }
}
```
