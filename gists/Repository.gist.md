# Repository.gist

用途：按 UniqueID 管理运行期实体，提供主仓 + 子索引（如 BBCoin）的仓储结构。

参考来源：
- MoodPuzzle/Assets/Src_Runtime/HotReload/Entities/Good/GoodRepository.cs

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

namespace NJM {

    public class GoodRepository {

        Dictionary<UniqueID, GoodEntity> all;
        Dictionary<UniqueID, GoodEntity> bbcoins;
        GoodEntity[] tempArray;

        public GoodRepository() {
            all = new Dictionary<UniqueID, GoodEntity>();
            bbcoins = new Dictionary<UniqueID, GoodEntity>();
            tempArray = new GoodEntity[100];
        }

        public void Add(GoodEntity goodEntity) {
            bool succ = all.TryAdd(goodEntity.uniqueID, goodEntity);
            if (!succ) {
                Debug.LogError($"GoodEntity {goodEntity.uniqueID.GetString()} already exists.");
                return;
            }
            if (goodEntity.type == GoodType.BBCoin) {
                bbcoins.TryAdd(goodEntity.uniqueID, goodEntity);
            }
        }

        public bool TryGet(UniqueID uniqueID, out GoodEntity goodEntity) {
            return all.TryGetValue(uniqueID, out goodEntity);
        }

        public void Remove(UniqueID uniqueID) {
            all.Remove(uniqueID);
            bbcoins.Remove(uniqueID);
        }

        public int TakeAll(out GoodEntity[] goodEntities) {
            int count = all.Count;
            if (count > tempArray.Length) {
                tempArray = new GoodEntity[count];
            }
            all.Values.CopyTo(tempArray, 0);
            goodEntities = tempArray;
            return count;
        }

        public void ForeachBBCoin(Action<GoodEntity> action) {
            foreach (var good in bbcoins.Values) {
                action(good);
            }
        }
    }
}
```
