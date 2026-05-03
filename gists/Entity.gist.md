# Entity.gist

用途：Entity 运行期对象 + SO 配置资源的双层建模模板。

参考来源：
- MoodPuzzle/Assets/Src_Runtime/HotReload/Entities/Good/GoodEntity.cs
- MoodPuzzle/Assets/Src_Runtime/HotReload/Entities/Good/TM/GoodSO.cs

```csharp
using System;
using UnityEngine;

namespace NJM {

    // Runtime Entity: 场景对象 + 行为入口
    public class GoodEntity : MonoBehaviour {

        public UniqueID uniqueID;
        public TypeID typeID;
        public GoodType type;

        [SerializeField] public GoodMod mod;

        public void Ctor() {
            mod.Ctor();
            Release();
        }

        public void Init() {
            StopAllCoroutines();
            transform.localScale = Vector3.one;
            transform.rotation = Quaternion.identity;
            mod.transform.localScale = Vector3.one;
            mod.sr.transform.localScale = Vector3.one;
        }

        public void Reuse() {
            gameObject.SetActive(true);
        }

        public void Release() {
            StopAllCoroutines();
            gameObject.SetActive(false);
        }

        public void Spr_Set(Sprite spr) {
            mod.SR_Sprite_Set(spr);
        }
    }
}
```

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
