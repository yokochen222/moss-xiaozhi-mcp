from core.camera import Camera
from dotenv import load_dotenv
import os

load_dotenv()

ENABLED_IP_CAMERA = os.getenv('ENABLED_IP_CAMERA')


if ENABLED_IP_CAMERA == 'true':
    global camera
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
    if os.getenv('ONVIF_CAMERA_PTZ_ENABLED') == 'true':
        @mcp.tool()
        def adjust_the_camera_view_tool(direction: str, angle: float) -> dict:
            """
                MOSS视角角度调整工具，最大值 -360度到360度，当用户需要调整角度时使用此工具
                参数如下
                :param direction: 方向 ('up', 'down', 'left', 'right')
                :param angle: 角度现在最大值 -360度到360度
                :return: 操作结果
            """
            try:
                result = camera.control_ptz(direction, angle)
                print("云台控制结果:", result)
                return result
            except Exception as e:
                print(f"Error in controlCameraPTZ: {e}")
                return {"success": False, "result": str(e)}