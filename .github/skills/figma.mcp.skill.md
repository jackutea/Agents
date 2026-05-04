# Figma UI MCP Skill

本 Skill 为 Agent 提供了在使用 Figma MCP 时“如何分层设计”和“如何稳定导出”的认知流指导。

## 核心工作流

1. **构思 DOM 树状结构**
   在动手调用创建工具之前，必须将用户的设计稿拆解成树状依赖。
   *例如：“创建一个名片框”*
   - Root: 外层背景层 Frame (`id: card_root`)
     - Child 1: 头像区 Rectangle (`parent_id: card_root`)
     - Child 2: 名字信息 Text (`parent_id: card_root`)

2. **依次建立图层并设定依赖**
   不能只使用全局坐标乱摆。通过指定 `parent_id` 确保建立真正的图层嵌套逻辑。
   - `create_frame({ name: "Card Root", width: 400, height: 200 })` -> 返回 `node_id_A`
   - `create_rectangle({ name: "Avatar", width: 50, height: 50, parent_id: "node_id_A", x: 20, y: 20 })`
   - `create_text({ characters: "John Doe", parent_id: "node_id_A", x: 90, y: 20 })`

3. **分层导出 (Exporting)*
   当用户要求“分别导出”时：
   你需要对每一个需要导出的 `node_id` 单独调用 `export_node_to_png({ node_id: "...", export_path: "d:/Agents/exports/avatar.png" })`。MCP 服务端与插件会通过 WebSocket 协同处理图像数据，最终存进您传入的绝对路径。

## 异常处理
- 如果由于连接断开导致工具返回超时或失败，提示用户确保 Figma 插件面板正处于打开并激活（运行中）状态。
- 如果请求导出的图层没有任何视觉实化（例如一个完全透明无背景的空 Frame），Figma 会输出全透明 PNG。建议对 Frame 加上 `fills` 背景（如白色或灰色）后再导出。
