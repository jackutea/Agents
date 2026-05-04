# Blender MCP Skill

本 Skill 旨在为 Agent 提供关于通过 MCP 和 Socket 操作 Blender 执行建模、绑定、动画的基础指导。

## 核心工作流

1. **评估需求与拆解**：
   收到类似于“创建一个桌子，并绑定一根可以控制高度的骨骼”的需求时，必须拆解为：
   - A. 确认 Blender Socket 服务是否已连通 
   - B. 执行建模指令：生成各部件 Mesh（桌面、桌腿等），或者先建一个 Cube 然后利用代码 Extrude。
   - C. 执行绑定指令：创建一个 Armature，向 Edit Bones 添加骨骼，调整坐标。
   - D. 蒙皮与权重：选中子物体与 Armature，进行 Parent (`bpy.ops.object.parent_set(type='ARMATURE_AUTO')`)。

2. **API 调用原则 (bpy)**：
   由于外部 MCP 只能发送代码文本或特定指令给 Blender 端监听器执行，使用 `bpy.ops` API 时应注意上下文（Context）极易不对。
   - 优先通过低级 API 修改数据：例如直接改 `bpy.data.objects['Cube'].location`，而不是依赖操作游标和 `bpy.ops.transform.translate`。
   - 必须先获取该对象再操作：
     ```python
     import bpy
     obj = bpy.data.objects.get("Target")
     if obj:
         obj.location.x += 1.0
     ```

3. **常用操作代码片段对照**：
   - **建立猴头**: `bpy.ops.mesh.primitive_monkey_add()`
   - **添加修改器**: `mod = obj.modifiers.new(name="SubSurf", type='SUBSURF'); mod.levels = 2`
   - **创建骨骼**:
     ```python
     bpy.ops.object.armature_add()
     arm_obj = bpy.context.active_object
     bpy.ops.object.mode_set(mode='EDIT')
     # modify bones
     bpy.ops.object.mode_set(mode='OBJECT')
     ```
   - **设置关键帧**: `obj.keyframe_insert(data_path="location", frame=1)`

4. **异常处理**：
   如果 Listener 反馈 `AttributeError` 或 `ContextError`，请根据错误信息进行修改，重试前确保对象处于正确的模式（如 Object Mode vs Edit Mode）。
