# Module.gist

用途：各子系统模块 / Manager (基于 MoodPuzzle 工程提取) 的代码参考模板。
说明：不同领域的业务有各自定制的结构封装，请严格参考对应领域的原始设计，不要套用单一泛化模板。

```csharp
// =====================================
// 1. Input (InputModule) - MonoBehaviour
// 职责：维护多玩家输入设备的状态，并提供按键 UI 提示图的支持 (结合 Wu2 架构)。
// =====================================
using System.Collections.Generic;
using UnityEngine;

namespace NJM {
    public class InputModule : MonoBehaviour {
        // 输入键位对应的 UI 提示图配置 (如 PS/Xbox 按键图标)
        [SerializeField] InputPromptSo inputPromptSO;
        
        // 面向多玩家/控制器的输入实体映射字典
        Dictionary<GamePlayerOrder, InputEntity> inputs;
        
        public void Ctor() {
            var player1 = new InputEntity();
            inputs = new Dictionary<GamePlayerOrder, InputEntity> {
                { GamePlayerOrder.Player1, player1 }
            };
            player1.Inject(inputPromptSO);
        }
        
        public void Init() {
            // 烘焙对应的 Sprite 字典缓冲，并正式激活 InputEntity
            inputPromptSO.BakeDict();
            if (inputs.TryGetValue(GamePlayerOrder.Player1, out var p1)) {
              p1.Init();
            }
        }
        
        public void Process(GamePlayerOrder order, float dt) {
            // 分发到具体玩家的实体内，每帧轮询设备实际状态或动作重映射
            if (inputs.TryGetValue(order, out var inputEntity)) {
                inputEntity.Process(dt);
            }
        }

        public bool TryGetInput(GamePlayerOrder order, out InputEntity inputEntity) {
            return inputs.TryGetValue(order, out inputEntity);
        }

        // 供 UI 层查询某个操作键绑定的摇杆/键盘实体图标
        public bool TryGetSprite(GamePlayerOrder order, InputKey inputKey, out Sprite sprite) {
            if (inputs.TryGetValue(order, out var inputEntity)) {
                // inputEntity.TryGetFirstBindingSprite(...)
            }
            sprite = null;
            return false;
        }
        
        public void TearDown() {
            // 实体内的各自清理与释放
        }
    }
}

// =====================================
// 2. Asset (AssetsModule) - 纯 C# 类 (Manager级)
// 职责：全局资产仓库，管理 SO、Prefab，分阶段异步加载资源。
// =====================================
using System.Collections;
using System.Collections.Generic;
using UnityEngine.ResourceManagement.AsyncOperations;

namespace NJM {
    public class AssetsModule {
        Dictionary<TypeID, Panel_Base> panels;
        AsyncOperationHandle part1Op;
        
        public bool isPartBDone;
        public Queue<System.Action> part2DoneQueue;

        public AssetsModule() {
            panels = new Dictionary<TypeID, Panel_Base>(32);
            part2DoneQueue = new Queue<System.Action>();
        }

        public IEnumerator Load_PartA_IE() {
            // 使用 Addressables 异步加载，如 yield return LoadLabel("PartA", ...)
            yield return null;
        }

        public IEnumerator Load_PartB() {
            // ...
            isPartBDone = true;
            yield return null;
        }
    }
}

// =====================================
// 3. L10N (L10NManager) - 纯 C# 类
// 职责：多语言文本和标记的管理，支持运行时语言切换并处理 Fallback。
// =====================================
using UnityEngine;

namespace NJM {
    public class L10NManager {
        L10NRepository repository;
        const SystemLanguage lang_fallback = SystemLanguage.English;
        SystemLanguage lang_current;

        public L10NManager() {
            repository = new L10NRepository();
            lang_current = SystemLanguage.ChineseSimplified;
            // 配合系统 API 获取系统语言如 WX.GetSystemInfoSync().language
        }

        public void AddAll(ICollection<L10NSO> all) {
            // 从 SO 配置灌入多语言数据，填入 repository
        }

        public void Language_Set(SystemLanguage lang) {
            lang_current = lang;
        }

        public bool TryGet(EntityTypeID typeID, out L10NOneLangTC oneLangTC) {
            // 先查当前语言字典，如查询不到则降级查询 lang_fallback
            oneLangTC = default;
            return false;
        }
    }
}

// =====================================
// 4. Ads (AdsManager) - MonoBehaviour
// 职责：生命周期伴随 GameObject，管理广告实体创建析构。
// =====================================
using UnityEngine;

namespace NJM {
    public class AdsManager : MonoBehaviour {
        AdsAssets assets;
        AdsRepository repository;
        public bool isPlaying;

        public void Ctor() {
            assets = new AdsAssets();
            repository = new AdsRepository();
        }

        public void AddAll(ICollection<AdsSO> ads) { assets.LoadAll(ads); }

        public void Banner_Show(TypeID typeID, int left, int top, int width) {
            // 通过 TypeID 识别广告是否为 Banner，新建或获取 WXAdsBannerEntity 展示
        }

        public void Reward_Play(TypeID typeID, System.Action OnCompleted, System.Action<AdsFailedType> OnFailed) {
            if (isPlaying) { OnFailed?.Invoke(AdsFailedType.Failed); return; }
            isPlaying = true;
            // 获取 WXAdsRewardEntity 实例并播放回调
        }

        public void TearDown() {
            // repository 中存活广告对象统一息屏/销毁
        }
    }
}

// =====================================
// 5. VFX (VFXManager) / 6. Audio (AudioManager) - 五件套架构
// 职责：通过 Asset-Repository-Pool-Entity-Manager 五件套管理特效/音效。
// =====================================
using UnityEngine;

namespace NJM {
    public class VFXManager {
        VFXAssets assets;
        VFXRepository repository;
        VFXPool pool;
        int idCounter = 0;

        public VFXManager() {
            assets = new VFXAssets();
            repository = new VFXRepository();
            pool = new VFXPool();
        }

        public void LoadAllIE(ICollection<VFXSO> vFXSOs) { assets.LoadAll(vFXSOs); }

        public VFXEntity Play(TypeID typeID, Vector3 worldPos) {
            // 从 Assets 查询 SO，委托 Spawn 发放 Entity
            return null;
        }
        
        VFXEntity Spawn(VFXSO so) {
            var entity = pool.Get(so.typeID, () => Create(so));
            entity.Reuse();
            entity.uniqueID = idCounter++;
            repository.Add(entity);
            return entity;
        }

        public void Tick(float dt) {
            // 减去非循环实例的生命周期并调用 Release(entity)
        }
        
        public void Release(VFXEntity entity) {
            repository.Remove(entity);
            pool.Return(entity);
            entity.Release();
        }
    }
}

// =====================================
// 7. NetworkClient (NetworkModule) - 纯 C# 类
// 职责：网络收发客户端抽象。封装封包/解包/加密。
// =====================================
using System;

namespace NJM {
    public class NetworkModule {
        public readonly INetworkClient client; // 例如 TelepathyNetClient / WXNetClient
        byte[] sendBuffer;
        
        public ValidValue<ulong> salt;
        public Action OnConnected;
        public Action<ArraySegment<byte>> OnData;

        public NetworkModule() {
            // 根据平台宏定义初始化底层 Client，绑定 HandleConnected 等
            sendBuffer = new byte[MessageConst.MAX_MESSAGE_SIZE];
        }

        public void Connect(string ip, int port) { client.Connect(ip, port); }
        public void Disconnect() { TearDown(); client.Disconnect(); }

        public void Tick(int processLimit = 100) {
            client.Tick(processLimit);
            // 自动重连机制 & Heartbeat 超时判定
        }

        public bool SendMessage(IMessage message) {
            // 封装 MessageId、BodyType 与 Payload，写入 sendBuffer
            // 若 salt 有效则异或加密 payload，调用 client.Send()
            return true;
        }
        
        public void TearDown() {
            salt.isValid = false;
        }
    }
}
```
