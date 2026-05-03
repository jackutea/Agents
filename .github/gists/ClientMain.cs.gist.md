# ClientMain.gist

用途：客户端主入口初始化模板（Ctor -> 注入 Context -> 绑定事件 -> 启动流程）。

```csharp
using UnityEngine;
using UnityEngine.EventSystems;
using System;
using System.Collections;

namespace TemplateNamespace {

    public class ClientMain : MonoBehaviour {

        GameContext ctx;

        // Module
        static InputModule inputModule;
        static AssetsModule assetsModule;
        static NetworkModule networkModule;

        // Repository
        static GameRepository gameRepository;

        // Pool
        static GamePool gamePool;

        // UI
        [SerializeField] Canvas canvas_World;

        // Lifecycle State
        bool isInit = false;
        bool isTearDown = false;

        #region Start & Bootstrap
        void Start() {
            // 1) Ctor
            ctx = new GameContext();
            inputModule = GetComponentInChildren<InputModule>();
            inputModule.Ctor();
            assetsModule = new AssetsModule();
            networkModule = new NetworkModule();
            gameRepository = new GameRepository();
            gamePool = new GamePool();

            // 2) Inject
            ctx.inputModule = inputModule;
            ctx.assetsModule = assetsModule;
            ctx.networkModule = networkModule;
            ctx.gameRepository = gameRepository;
            ctx.gamePool = gamePool;
            ctx.canvas_World = canvas_World;
            ctx.eventSystem = EventSystem.current;

            // 3) Bootstrap
            BindingEvents();
            SetupNetwork();
            StartCoroutine(InitIE());
        }

        void BindingEvents() {
            // Register input, controller and network handlers here
        }

        void SetupNetwork() {
            // Network setup, message dispatch, connect
            // networkModule.OnData = (data) => { ... }
        }

        IEnumerator InitIE() {
            // ==== PreInit ====
            inputModule.Init();

            // ==== Load Assets ====
            yield return assetsModule.Load_PartA_IE();

            // ==== Login / Remote Data (With Timeout/Retry) ====
            /*
            float timeout = 2f;
            while (!ctx.userEntity.isLoginSucc && timeout > 0f) {
                timeout -= Time.deltaTime;
                yield return null;
            }
            */

            // ==== Enter Game / World ====
            
            // Set init flag
            isInit = true;

            // Trigger GC after heavy loading
            GC.Collect();
        }
        #endregion

        #region Update (Pre, Fix, Late)
        float restTickTime = 0f;
        void Update() {
            float dt = Time.deltaTime;

            // Optional: Network Tick (can tick before init)
            networkModule.Tick();

            if (!isInit) {
                return;
            }

            // 1) Pre Tick (Input, Logic that doesn't strictly need fixed step)
            // GameSystem.Tick(ctx, dt);

            // 2) Fix Tick (Core game logic, Physics)
            float fixInterval = dt; // Or a fixed time step like 0.02f
            restTickTime += dt;
            do {
                float step = Math.Min(restTickTime, fixInterval);
                restTickTime -= step;
                // GameSystem.FixTick(ctx, step);
                // Physics2D.Simulate(step);
            } while (restTickTime > fixInterval);

            // 3) Late Tick (Camera follow, Audio/VFX tick)
            // GameSystem.LateTick(ctx, dt);
        }

        void LateUpdate() {
            if (!isInit) {
                return;
            }
            // Screen coordinate conversions, UI final adjustments
        }
        #endregion

        #region Application focus, quit & teardown
        void OnApplicationFocus(bool hasFocus) {
            if (!isInit) return;

            // Optional: Manual GC triggering out of focus
            GC.Collect();

            if (!hasFocus) {
                // Focus Lost: Pause timers, Save data, AFK states
                // SaveController.SaveAll(ctx);
            } else {
                // Focus Resumed: Reconnect, resume states
                // UserController.Comeback(ctx);
            }
        }

        void OnApplicationQuit() {
            TearDown();
        }

        void OnDestroy() {
            TearDown();
        }

        void TearDown() {
            if (!isInit) {
                return;
            }
            if (isTearDown) {
                return;
            }
            isTearDown = true;

            // Save data automatically before exit
            // SaveController.SaveAll(ctx);

            // Disconnect and Cleanup
            networkModule.Disconnect();
            assetsModule.UnloadAll();
        }
        #endregion
    }
}
```
