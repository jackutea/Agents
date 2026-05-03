# ClientMain.gist

用途：客户端主入口初始化模板（Ctor -> 注入 Context -> 绑定事件 -> 启动流程）。

参考来源：
- MoodPuzzle/Assets/Src_Runtime/HotReload/ClientMain.cs

```csharp
using UnityEngine;
using UnityEngine.EventSystems;

namespace NJM {

    public class ClientMain : MonoBehaviour {

        GameContext ctx;

        // Module
        static InputModule inputModule;
        static AssetsModule assetsModule;
        static NetworkModule networkModule;

        // Repository
        static GoodRepository goodRepository;
        static CabinetRepository cabinetRepository;

        // Pool
        static GoodPool goodPool;
        static CabinetPool cabinetPool;

        [SerializeField] Canvas canvas_World;

        void Start() {
            // 1) Ctor
            ctx = new GameContext();
            inputModule = GetComponentInChildren<InputModule>();
            inputModule.Ctor();
            assetsModule = new AssetsModule();
            networkModule = new NetworkModule();
            goodRepository = new GoodRepository();
            cabinetRepository = new CabinetRepository();
            goodPool = new GoodPool();
            cabinetPool = new CabinetPool();

            // 2) Inject
            ctx.inputModule = inputModule;
            ctx.assetsModule = assetsModule;
            ctx.networkModule = networkModule;
            ctx.goodRepository = goodRepository;
            ctx.cabinetRepository = cabinetRepository;
            ctx.goodPool = goodPool;
            ctx.cabinetPool = cabinetPool;
            ctx.canvas_World = canvas_World;
            ctx.eventSystem = EventSystem.current;

            // 3) Bootstrap
            BindingEvents();
            SetupNetwork();
            StartCoroutine(InitIE());
        }

        void BindingEvents() {
            // register handlers
        }

        void SetupNetwork() {
            // connect and message dispatch
        }

        System.Collections.IEnumerator InitIE() {
            yield break;
        }
    }
}
```
