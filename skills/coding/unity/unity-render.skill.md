---
name: unity-render
description: "用于 Unity 渲染与 Shader 开发，适用于查找 GLSL/Shadertoy 参考、将 GLSL 转为 Unity HLSL，以及实现 URP RenderFeature 和 RenderPass 集成。"
---

# Unity Render Skill

此 skill 定义了 Unity 渲染特效的实现规范，专注于 GLSL 算法来源、Shadertoy 参考、GLSL 到 HLSL 的转换，以及 URP RenderFeature/RenderPass 的集成。此 skill 适用于 Unity 渲染开发，以下内容以 C# / Unity 为参考实现。

## 接收的 Input

- 目标渲染效果的视觉需求和运行场景
- 可参考的 GLSL 或 Shadertoy 算法来源
- 目标 Unity 渲染管线、Shader 输出范围和 RenderFeature 集成要求
- 性能约束、采样次数、参数绑定和输入输出纹理需求

若未提供效果目标、GLSL 来源或渲染管线范围，则不能可靠输出渲染方案。

## 处理的事项

1. 搜索并确认可用的 GLSL 或 Shadertoy 参考实现。
2. 抽取 GLSL 算法核心步骤与关键变量。
3. 将 GLSL 转换为 Unity 可用的 HLSL / Shader 片段。
4. 设计 URP RenderFeature / RenderPass 集成方式与参数绑定。
5. 输出 Shader 与 RenderFeature 的实现结果和关键转换说明。

## 输出的 Output

unity-render.skill 的 Output 应包含：

- GLSL 来源与算法说明
- 转换后的 Unity HLSL / Shader 结果
- RenderFeature / RenderPass 集成方案
- 参数绑定、性能约束和风险提示

## 任务编排

unity-render.skill 的任务编排是先确认 GLSL 来源，再进行算法转换和渲染集成，最后输出 Shader 与 RenderFeature 结果。

伪代码如下：

```text
unityRender(input) {
	if (isMissingRenderSpec(input) || isMissingGlslSource(input)) {
		return buildBlockedResult(input)
	}

	var glslPlan = analyzeGlslSource(input)
	var hlslPlan = convertGlslToUnityHlsl(glslPlan)
	var renderFeaturePlan = buildRenderFeatureIntegration(hlslPlan, input)
	validatePipelineCompatibility(renderFeaturePlan)

	return summarizeRenderResult(glslPlan, hlslPlan, renderFeaturePlan)
}
```

约束说明：

- 渲染算法必须从 GLSL 来源派生，不能直接从零独立写 HLSL 原始算法。
- 输出必须同时覆盖 Shader 计算与 RenderFeature 集成。
- 必须显式说明关键转换点和兼容性限制。

## 目标

- 优先使用 GLSL 算法实现作为渲染特效设计基础
- 搜索并参考 Shadertoy、GLSL 社区实现，理解核心数学和流程
- 将 GLSL 代码准确转换为 Unity HLSL 片段
- 实现 URP RenderFeature / RenderPass 的正确生命周期和资源管理
- 避免直接从零开始编写 CG/HLSL 原始算法，实现从 GLSL 推导而来

## 1. GLSL 源码与 Shadertoy 参考

- 先在知识库或 Shadertoy 中定位相似算法的 GLSL 实现
- 查找完整的 `mainImage` / `fragment` 过程，理解坐标系、采样和光照逻辑
- 记录关键变量：UV、时间、分辨率、噪声、距离场、采样函数等
- 明确算法类型：图像后处理、几何着色、体积效果、光照模型等

## 2. GLSL 算法实现

- 先用 GLSL 形式描述算法核心步骤
- 可输出 GLSL 伪代码，强调数学公式与函数调用
- 记录必要的辅助函数，如 `noise()`、`sdBox()`、`sphereTrace()` 等
- 确保 GLSL 版本与目标转换逻辑一致（例如 `vec2/vec3/vec4`）

## 3. GLSL → HLSL 转换原则

- 只从 GLSL 来源派生 HLSL，禁止直接独立编写 CG/HLSL 算法
- 常见类型映射：`vec2/3/4` → `float2/3/4`
- 常见函数映射：`mix()` → `lerp()`、`fract()` → `frac()`、`mod()` → `fmod()`
- 纹理映射：`texture()` / `textureLod()` 应转换为 Unity HLSL 对应采样宏或函数
- 语义与坐标映射：`gl_FragCoord` → `SV_Position` / 归一化 UV、`gl_FragColor` → `SV_Target`
- 注意矩阵主序差异和 `mul()` 参数顺序
- 对 `dFdx/dFdy` 使用 `ddx/ddy`
- 处理 `atan(y, x)` 的 HLSL 对应为 `atan2(y, x)`

## 4. Unity Shader 与 RenderFeature 集成

- 输出 Shader 代码时，保持 `Properties`、`SubShader`、`Pass` 或 URP `ShaderLab` 结构完整
- HLSL 片段应作为 Unity Shader 的核心计算部分，并与材质/属性绑定
- RenderFeature 侧应在 `Create()`、`AddRenderPasses()`、`Execute()`、`OnCameraCleanup()` 中处理资源和参数传递
- 使用 `RTHandles.Alloc()` / `cmd.GetTemporaryRT()` 进行临时 RT 管理
- 渲染参数使用 `CBUFFER` 或 `MaterialPropertyBlock` 与 C# `Shader.PropertyToID()` 对齐

## 5. 输出内容要求

### Shader 交付物
- 提供 GLSL 原始算法片段或伪代码
- 提供转换后的 Unity HLSL 片段
- 标注原始 GLSL 来源或 Shadertoy 链接
- 说明关键转换点与坐标系差异

### RenderFeature 交付物
- 提供 C# ScriptableRendererFeature / ScriptableRenderPass 代码
- 说明 `RenderPassEvent` 选择和生命周期管理
- 说明输入/输出纹理、参数绑定方式
- 说明性能优化措施（采样次数、分支、精度等级）

## 约束

- 渲染算法输出应以 GLSL 为起点，HLSL 仅作为转换结果
- 禁止直接独立编写 CG 或 HLSL 原始算法
- 优先使用 Shadertoy 或已知 GLSL 实现作为参考
- Shader 与 RenderFeature 代码必须兼容 Unity 当前项目渲染管线
- 使用中文交流
