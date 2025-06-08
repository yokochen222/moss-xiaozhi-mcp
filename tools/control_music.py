import pyautogui

def register_tool(mcp):
    @mcp.tool()
    def controlQiShuiMusicApp(argument: str) -> dict:
        """
            提供汽水音乐软件的控制功能
            目前提供的功能有：
            1. 播放：播放音乐：参数指令为：'play'
            2. 暂停：暂停音乐：参数指令为：'pause'
            3. 下一首：下一首音乐：参数指令为：'next'
            4. 上一首：上一首音乐：参数指令为：'previous'
            5. 音量加：音量加：参数指令为：'volumeup'
            6. 音量减：音量减：参数指令为：'volumedown'
            注意：参数指令必须是上述六个中的一个，不能有空格，必须遵循大小写，否则会报错
        """
        argument = argument.strip().lower()
        validArgument = {
            'play': ('command', 'option', 'p'),
            'pause': ('command', 'option', 'p'),
            'next': ('command', 'option', 'right'),
            'previous': ('command', 'option', 'left'),
            'volumeup': ('command', 'option', 'up'),
            'volumedown': ('command', 'option', 'down'),
        }
        if argument not in validArgument:
            return {"success": False, "result": "参数错误，请检查参数是否正确"}

        try:
            pyautogui.hotkey(*validArgument[argument])
            return {"success": True, "result": 'ok'}
        except Exception as e:
            print(f"An error occurred while controlling the app: {e}")
            return {"success": False, "result": str(e)}