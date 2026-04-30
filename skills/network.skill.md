# Network Skill

此 skill 提取网络通信设计与协议实现的通用规范，适用于客户端/服务端消息传输、消息注册和网络模块架构。

## 核心职责
- 设计网络消息协议与传输层架构
- 定义消息类型和 `IMessage` 接口规范
- 规划消息注册与处理流程
- 设计 NetworkServer/NetworkModule 的职责边界
- 约束通信实现细节，保证多线程安全与主线程同步

## 设计要点

### 1. 目录与模块结构
- 客户端：`Modules_Network/`，包含 `NetworkModule`、`INetworkClient`、`TelepathyNetClient`、`WXNetClient` 等
- 服务端：`Modules_Network/`，包含 `NetworkServer`、`Message`、各类消息定义与处理器
- 统一的消息定义放在 `Message/` 或 `Protocol/` 目录下

### 2. 消息协议规范
- 报文格式：`| messageId(2B LE) | bodyType(1B) | body |`
- `BodyType` 定义：`None=0`、`JSON=1`、`Bin=2`
- `messageId` 使用 `ushort`，避免重复并使用常量集中管理

### 3. 消息命名与注册
- 命名规则：
  - `xxMessage_Req`：客户端发给服务端
  - `xxMessage_Res`：服务端单发给客户端
  - `xxMessage_Broad`：服务端群发给客户端
- 追加消息时：
  1. 在 `MessageConst` 增加对应常量
  2. 新建消息类型文件并实现 `IMessage`
  3. 在 `MessagePool` 注册工厂
  4. 在 `NetworkServer.BindMessageHandler<T>` 绑定处理器

### 4. NetworkServer 和 NetworkModule
- `NetworkServer` 封装传输层，负责 `Init`、`Start`、`Stop`、`Tick`、`Send`、`BindMessageHandler`、`HandleData`
- `NetworkModule` 负责客户端连接管理、消息发送、消息分发和业务回调
- 将传输层和业务层分离，保持服务器和客户端实现可替换

### 5. MessagePool 设计
- 使用 `Dictionary<ushort, Queue<IMessage>>` 管理对象池
- 提供 `Rent` / `Return` 机制，避免频繁 GC
- 注册工厂方式使消息类型可动态扩展

## 约束
- C# 禁改 `Telepathy/`
- C# 禁用 `BinaryPrimitives`
- 网络回调只在 Tick 主线程触发
- 任何语言层面实现必须保持与 transport 层解耦
- 只用中文

## 说明
- 如果涉及 C# 代码实现，请参考 `skills/csharp-network.skill.md`。