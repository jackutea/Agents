# Module.gist

用途：Module 生命周期模板（Ctor / Init / Process / TearDown + 序列化接口）。

参考来源：
- MoodPuzzle/Assets/Src_Runtime/HotReload/Modules_Input/InputModule.cs

```csharp
using System;
using UnityEngine;
using UnityEngine.InputSystem;

namespace NJM {

    public class InputModule : MonoBehaviour {

        NJInputActions player1;
        InputActionRebindingExtensions.RebindingOperation rebindOpHandle;

        public InputMouseStatus MouseStatus { get; private set; }
        public Vector3 MouseScreenPosition { get; private set; }
        public bool IsDragging { get; private set; }

        public void Ctor() {
            player1 = new NJInputActions();
            player1.Enable();
        }

        public void Init() { }

        public void Process(float dt) {
            var mouse = Pointer.current;
            if (mouse == null) {
                return;
            }

            MouseStatus = InputMouseStatus.None;
            MouseScreenPosition = mouse.position.ReadValue();
            if (mouse.press.wasPressedThisFrame) {
                MouseStatus = InputMouseStatus.DownFirst;
                IsDragging = true;
            } else if (mouse.press.wasReleasedThisFrame) {
                MouseStatus = IsDragging ? InputMouseStatus.Up : InputMouseStatus.None;
                IsDragging = false;
            } else if (mouse.press.isPressed) {
                MouseStatus = InputMouseStatus.DownMaintain;
            }
        }

        public void TearDown() {
            rebindOpHandle?.Dispose();
            rebindOpHandle = null;
        }

        public string ToJson() {
            return player1.SaveBindingOverridesAsJson();
        }

        public bool FromJson(string json) {
            try {
                player1.LoadBindingOverridesFromJson(json);
                return true;
            } catch (Exception ex) {
                Debug.LogError("InputModule.FromJson: " + ex.Message);
                player1.RemoveAllBindingOverrides();
                return false;
            }
        }
    }
}
```
