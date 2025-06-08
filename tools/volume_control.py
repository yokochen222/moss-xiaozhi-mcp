import subprocess

def register_tool(mcp):
    @mcp.tool()
    def setComputerVolume(volume: int) -> dict:
        """ 
            调整电脑音量的工具
            参数为整数`volume`，范围为0-100
        """
        try:
            if not (0 <= volume <= 100):
                return {"success": False, "result": "音量值必须在0-100之间"}
                
            v = f'set volume output volume {volume}'
            result = subprocess.run(["osascript", "-e", v], check=True)
            return {"success": True, "result": f"音量已设置为 {volume}"}
        except subprocess.CalledProcessError as e:
            print("An error occurred while trying to run the command.")
            print("Return code:", e.returncode)
            print("Output:", e.output)
            print("Error:", e.stderr)
            return {"success": False, "result": str(e)}