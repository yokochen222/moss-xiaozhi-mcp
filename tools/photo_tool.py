from core import camera

def register_tool(mcp):
    @mcp.tool()
    def tekePhoto(question: str) -> dict:
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
            print(f"Error in tekePhoto: {e}")
            return {"success": False, "result": str(e)}