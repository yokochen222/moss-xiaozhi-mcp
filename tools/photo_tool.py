from core import camera

def register_tool(mcp):
    @mcp.tool()
    def takePhoto(question: str) -> dict:
        """ 
            此工具用于MOSS的视觉识别功能，是MOSS的眼睛，用于获取用户的照片信息。
            可以实现拍照并分析照片内容。在用户要求您查看某些内容后使用此工具。
            参数：`question`: 你想问的关于照片的问题。
            返回参数：提供照片信息的JSON对象。
        """
        try:
            result = camera.capture(question)
            print("视觉识别结果:", result)
            return result
        except Exception as e:
            print(f"Error in takePhoto: {e}")
            return {"success": False, "result": str(e)}

    @mcp.tool()
    def controlCameraPTZ(direction: str, speed: float) -> dict:
        """
            此工具用于控制MOSS上下左右移动。
            如果是多方位方向移动自动拆分成两次执行。

            参数：
              - direction: 移动方向，可选值为 'up'（上）、'down'（下）、'left'（左）、'right'（右）、
                'top-left'（左上）、'top-right'（右上）、'bottom-left'（左下）、'bottom-right'（右下）
              - speed: 移动速度，范围在0.1到1.0之间，其中 **360度对应的速度映射值为1**，
                       表示最大速度，与全向旋转角度线性对应。

            返回参数：操作结果的JSON对象
        """
        try:
            result = camera.control_ptz(direction, speed)
            print("云台控制结果:", result)
            return result
        except Exception as e:
            print(f"Error in controlCameraPTZ: {e}")
            return {"success": False, "result": str(e)}