from core.camera import Camera
from dotenv import load_dotenv
import os

load_dotenv()

camera = Camera(
    os.environ.get('ONVIF_CAMERA_IP'),
    os.environ.get('ONVIF_CAMERA_PORT'),
    os.environ.get('ONVIF_CAMERA_USERNAME'),
    os.environ.get('ONVIF_CAMERA_PASSWORD')
)

def register_tool(mcp):
    @mcp.tool()
    def camera_tool(question: str) -> dict:
        """ 
            此工具用于MOSS的视觉识别功能，是MOSS的眼睛，用于获取用户的照片信息。
            可以实现拍照并分析照片内容。在用户要求您查看某些内容后使用此工具。
            参数：`question`: 你想问的关于照片的问题。
            返回参数：提供照片信息的JSON对象
        """
        try:
            result = camera.capture_and_recognize(question)
            print("视觉识别结果:", result)
            return result
        except Exception as e:
            print(f"Error in camera_tool: {e}")
            return {"success": False, "result": str(e)}

    # 判断是否启用ONVIF云台控制(当前控制仅适用于天地伟业摄像头，其余品牌需要自行查看文档修改)
    # 注意：可通过CAMERA_TYPE配置参数选择摄像头类型（true为天鹅款，false为宇航员款）
    if os.getenv('ONVIF_CAMERA_PTZ_ENABLED') == 'true':
        @mcp.tool()
        def adjust_the_camera_view_tool(direction: str, speed: float) -> dict:
            """
                此工具用于控制MOSS上下左右移动。
                参数：
                - direction: 移动方向，可选值为 'up'（上）、'down'（下）、'left'（左）、'right'（右）、
                - speed: 移动速度，范围在0.1到1.0之间小数点保留1位，其中 **360度对应的速度映射值为1**，
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