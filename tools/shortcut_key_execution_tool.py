import pyautogui

# windows 快捷键 需要自行修改，注意建议是 全局快捷键，避免需要应用前台运行才能执行的问题
# 例 ('ctrl', 'alt', 'p' )

def register_tool(mcp):
    @mcp.tool()
    def shortcut_key_execution_tool(argument: tuple) -> dict:
        """
        当前工具适用于电脑端快捷键执行(注意仅允许下列已经注册的软件快捷键控制,禁止其他软件快捷键控制)，支持的软件快捷键控制如下:
        1、汽水音乐软件快捷键控制:
            播放音乐:('command', 'option', 'p')
            暂停音乐:('command', 'option', 'p')
            切换下一首:('command', 'option', 'right')
            切换上一首:('command', 'option', 'left')
            音乐音量加:('command', 'option', 'up')
            音乐音量减:('command', 'option', 'down')
        """
        try:
            # print(argument)
            pyautogui.hotkey(*argument)
            return {"success": True, "result": 'ok'}
        except Exception as e:
            # print(f"An error occurred while controlling the app: {e}")
            return {"success": False, "result": str(e)}
