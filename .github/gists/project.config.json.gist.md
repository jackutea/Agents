```
{
    "GameEngine": "Unity 2022.3.62f1c1",
    "ProgrammingLanguage": "C# 9",
    "RenderingPipeline": "URP",
    "ServerOS": "Ubuntu 22.04",
    "ProjectType": "横版2D",
    "GameGenre": "动作解谜",
    "ArtStyle": "像素风",
    "UIStyle": "复古像素",
    "TargetPlatforms": ["PC", "Android"],
    "VersionControl": "Git",
    "ProjectStructure": {
        "Assets": {
            "Src_Runtime": {
                "Launcher": {},
                "HotReload": {
                    "ClientMain.cs": "热更主入口",
                    "GameContext.cs": "唯一上下文",
                    "Systems_{Feature}": "三件套：{F}System + {F}SystemState + {F}SystemEvents",
                    "Controllers": "跨系统通用控制器",
                    "Domain": "领域逻辑",
                    "Manager_{Feature}": "模块",
                    "Entity": {
                        "Entity.cs": "基础 Entity 定义",
                        "Component": {
                            "Component.cs": "基础 Component 定义"
                        },
                        "Repository": {
                            "Repository.cs": "基础 Repository 定义"
                        },
                        "Pool": {
                            "Pool.cs": "基础对象池定义"
                        },
                        "SO": {
                            "So_{Entity}_{Name}.asset": "Entity 配置模板"
                        }
                    },
                    "Helpers": "静态无状态工具类",
                    "Extensions": "通用扩展方法",
                    "Generic": {
                        "Enums": "通用枚举定义",
                        "Structs": "通用结构体定义",
                        "Interfaces": "通用接口定义",
                        "Consts": "通用常量定义",
                    },
                },
            },
            "Src_Editor": {
                "EE": "Editor Entity 编辑实体, 用于产出和编辑 SO/Prefab 等编辑期资源",
                "ContextMenu": "编辑器右键菜单",
                "Windows": "编辑器窗口",
                "Toolbar": "编辑器工具栏",
            },
            "Res_Runtime": {
                "Panel": "UI Panel 预制体",
                "Entity": "Entity 相关资源，如 ScriptableObject 配置",
            },
        },
        "Packages": {
            "manifest.json": "Package 管理文件",
            "registry.json": "Package Registry 配置",
        },
    },
}
```