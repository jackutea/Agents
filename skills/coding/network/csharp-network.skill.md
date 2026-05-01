---
name: csharp-network
description: "用于 C# 网络实现细节，适用于设计 IMessage、消息类、对象池、NetworkServer/NetworkModule 封装，以及 Telepathy 兼容的主线程消息处理。"
---

# CSharp Network Skill

此 skill 提取 C# 网络实现的语言级细节与实现模板，专注于 `IMessage` 设计、消息类、NetworkServer、NetworkModule 和 Telepathy 兼容。

## 代码责任边界
- 仅处理 C# 网络实现细节
- 包括 `IMessage` 接口、消息类、消息池、传输层封装和主线程调度
- 不涉及高层业务流程设计或协议定义

## 核心模板

### 1. `IMessage` 接口
```csharp
public interface IMessage {
    ushort MessageId { get; }
    byte BodyType { get; }
    void WriteTo(IBinaryWriter writer);
    void ReadFrom(IBinaryReader reader);
    void Reset();
}
```

### 2. 消息类模板
```csharp
public class PingMessage_Req : IMessage {
    public ushort MessageId => MessageConst.PingMessageReq;
    public byte BodyType => BodyType.None;

    public void WriteTo(IBinaryWriter writer) {
        // 无需写 body
    }

    public void ReadFrom(IBinaryReader reader) {
        // 无需读 body
    }

    public void Reset() {
        // 清理临时字段
    }
}
```

### 3. MessagePool 模板
```csharp
public class MessagePool {
    private readonly Dictionary<ushort, Queue<IMessage>> _pools = new();
    private readonly Dictionary<ushort, Func<IMessage>> _factories = new();

    public void Register<T>(ushort messageId, Func<IMessage> factory) where T : IMessage {
        _factories[messageId] = factory;
        _pools[messageId] = new Queue<IMessage>();
    }

    public IMessage Rent(ushort messageId) {
        if (_pools.TryGetValue(messageId, out var queue) && queue.Count > 0) {
            return queue.Dequeue();
        }
        return _factories[messageId]();
    }

    public void Return(IMessage message) {
        message.Reset();
        _pools[message.MessageId].Enqueue(message);
    }
}
```

### 4. NetworkServer / Telepathy 封装
```csharp
public class NetworkServer {
    private readonly Telepathy.Server _server;

    public NetworkServer(int port) {
        _server = new Telepathy.Server();
        // 初始化配置
    }

    public void Init() {
        // 绑定事件和回调
    }

    public void Start() {
        _server.Start(port);
    }

    public void Stop() {
        _server.Stop();
    }

    public void Tick() {
        while (_server.GetNextMessage(out var msg)) {
            HandleData(msg);
        }
    }
}
```

### 5. Tick 主线程回调
- 所有业务处理回调必须由 `Tick` 在主线程触发
- 传输层负责收集原始数据并交给主线程处理
- 不要在网络回调中直接执行游戏逻辑

## 约束
- 禁改 `Telepathy/`
- 禁用 `BinaryPrimitives`
- JSON 统一使用 Newtonsoft.Json 库
- C# 网络代码必须兼容 `netstandard2.1`
- 使用 `IBinaryWriter` / `IBinaryReader` 或等价接口，避免直接依赖平台特殊类型
- 只用中文

## 说明
- 本 skill 针对 C# 网络实现细节。通用协议和消息流程请参考 `skills/coding/network/network.skill.md`。