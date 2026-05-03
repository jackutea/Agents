# Pool.gist

用途：最小可复用对象池模板（栈式回收，创建函数注入）。

```csharp
using System;
using System.Collections.Generic;

namespace NJM {

    public class GoodPool {

        List<GoodEntity> pool;

        public GoodPool() {
            pool = new List<GoodEntity>(512);
        }

        public GoodEntity Get(Func<GoodEntity> createFunc) {
            if (pool.Count > 0) {
                int lastIndex = pool.Count - 1;
                GoodEntity goodEntity = pool[lastIndex];
                pool.RemoveAt(lastIndex);
                return goodEntity;
            }
            return createFunc();
        }

        public void Return(GoodEntity goodEntity) {
            pool.Add(goodEntity);
        }
    }
}
```
