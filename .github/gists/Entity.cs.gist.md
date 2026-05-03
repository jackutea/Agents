# Entity.gist

用途：Entity 相关设计（包括运行期实体、纯数据实体 Component 分组、以及基于 SO 的配置数据）的建模模板。

## 1. 纯数据实体与 Component 分层建模 (Pure C# Data Entity)

当业务实体拥有极多状态维度时（例如 `UserEntity`、`GameEntity`），**按业务领域切分成多个 Component 非常重要**。Component 用于封装领域数据与内聚的操作逻辑，避免主实体类过度臃肿。实体则作为高内聚容器，仅负责组装各个 Component。

```csharp
using System;

namespace NJM {

    // Runtime Entity: 纯数据对象，作为 Component 容器
    public class UserEntity {

        public ulong generation;

        // 实体按领域拆分出多个 Component
        public UserResourceComponent resourceComponent;

        public UserEntity() {
            generation = 0;
            // 构造时完成组件初始化
            resourceComponent = new UserResourceComponent();
        }
    }
}
```

```csharp
using System;

namespace NJM {

    // Component: 高内聚维护实体某一领域的数据和逻辑操作，保证局部的一致性
    public class UserResourceComponent {

        public int coin { get; private set; }

        public UserResourceComponent() {
            coin = 0;
        }

        public void Coin_Add(int amount) {
            coin += amount;
        }

        public void Coin_Reduce(int amount) {
            coin -= amount;
            coin = Math.Max(0, coin); // 在组件内保证数值不为负等合法性边界
        }
    }
}
```

## 2. MonoBehaviour 实体对象 (Scene Entity) - 结合 Wu2 架构

在 Wu2 等动作/高自由度中，作为入口实体的 `MonoBehaviour` 往往需要聚合非常多的组件。实体需要持有一系列按职责切分的纯 C# 组件（Component）、状态机 / 视觉层引用（SM），并在内部维护明确的生命周期方法 (`Ctor`, `Setup`, `TearDown`) 和表现层接口 (`TF`、`Move` 等封装)。

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

namespace NJM {

    // Runtime Entity: 场景对象 + 行为入口（参考 Wu2 中的 RoleEntity 架构）
    public class RoleEntity : MonoBehaviour {

        EntityType EntityType => EntityType.Role;
        public UniqueID uniqueID;
        public TypeID typeID;
        public AllyStatus allyStatus;

        // Scene Graph & View / Physics
        [SerializeField] public Transform root;
        [SerializeField] public Rigidbody2D rb;
        [SerializeField] public RoleSM sm; // SM 通常挂载在子物体处理纯视觉与动画表现
        public HashSet<Collider2D> enterColliders;
        public HashSet<Collider2D> exitColliders;

        // Pure C# Components (按领域切分，避免主实体类过大)
        public RoleInputComponent inputComponent;
        public AttributeComponent attributeComponent;
        public RoleSkillComponent skillComponent;
        public RoleStateComponent stateComponent;
        public RoleBuffComponent buffComponent;

        #region Lifecycle
        public void Ctor() {
            // 实例化所有纯数据 C# 组件
            inputComponent = new RoleInputComponent();
            attributeComponent = new AttributeComponent();
            skillComponent = new RoleSkillComponent();
            stateComponent = new RoleStateComponent();
            buffComponent = new RoleBuffComponent();

            enterColliders = new HashSet<Collider2D>();
            exitColliders = new HashSet<Collider2D>();

            // 路由其子 View/SM 的初始化
            sm.Ctor();
        }

        public void Setup(UniqueID uniqueID, TypeID typeID, AllyStatus allyStatus) {
            // 运行期赋予上下文与唯一身份
            this.uniqueID = uniqueID;
            this.typeID = typeID;
            this.allyStatus = allyStatus;
        }

        public void TearDown() {
            // 对象销毁回收
            GameObject.Destroy(gameObject);
        }
        #endregion

        #region TF (Transform Wrappers)
        public void TF_Pos_Set(Vector2 pos) {
            transform.position = pos;
        }

        public Vector2 TF_Pos_Get() {
            return transform.position;
        }
        #endregion

        #region Move / Actions
        public void Move_SetVelocityX(float x) {
            Vector2 oldVelocity = rb.velocity;
            oldVelocity.x = x;
            rb.velocity = oldVelocity;

            // 根据移动方向更新朝向与缩放
            if (x != 0) {
                transform.localScale = new Vector3(Mathf.Sign(x), 1, 1);
            }
        }
        #endregion
    }
}
```

## 3. SO 配置数据 (ScriptableObject)

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

namespace NJM {

    // SO: 配置数据 + 编辑器 Bake 入口
    [CreateAssetMenu(fileName = "So_Good_", menuName = "NJM/GoodSO", order = 1)]
    public class GoodSO : ScriptableObject, IEquatable<GoodSO> {

        public TypeID typeID;
        public GoodType goodType;
        public int specialValue;
        public List<Vector2Int> levelRanges;
        public Sprite spr;
        public bool isUnused;

        public bool IsInRange(int level) {
            foreach (var range in levelRanges) {
                if (level >= range.x && level <= range.y) {
                    return true;
                }
            }
            return false;
        }

        bool IEquatable<GoodSO>.Equals(GoodSO other) {
            if (other == null) return false;
            return typeID == other.typeID;
        }
    }
}
```
