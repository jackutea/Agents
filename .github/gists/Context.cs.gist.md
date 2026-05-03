# Context.gist

用途：统一依赖容器，集中托管 State / Events / Module / Manager / Repository / Pool / Entity。

```csharp
using UnityEngine;
using UnityEngine.EventSystems;

namespace NJM {

    public class GameContext {

        public SystemStatus status;

        // System State
        public HomeSystemState state_Home;
        public PauseSystemState state_Pause;

        // System Events
        public HomeSystemEvents events_Home;
        public GameSystemEvents events_Game;

        // Module
        public InputModule inputModule;
        public AssetsModule assetsModule;
        public NetworkModule networkModule;

        // Manager
        public AudioManager audioManager;
        public VFXManager vfxManager;

        // Repository
        public GoodRepository goodRepository;
        public CabinetRepository cabinetRepository;

        // Pool
        public GoodPool goodPool;
        public CabinetPool cabinetPool;

        // Entity
        public UserEntity userEntity;
        public GameEntity gameEntity;

        // Engine
        public Canvas canvas_World;
        public EventSystem eventSystem;

        public GameContext() { }
    }
}
```
