import subprocess
import platform
import shlex

def register_tool(mcp):
    @mcp.tool()
    def command_execution_tool(command: str) -> dict:
        """
        执行终端命令的工具
        :param command: 要执行的命令字符串
        :return: 包含执行结果的字典
        """
        argument = command.strip()
        try:
            # 根据不同平台设置shell
            if platform.system() == "Windows":
                # Windows使用cmd.exe
                result = subprocess.run(
                    argument,
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                # macOS/Linux使用bash解析命令
                args = shlex.split(argument)
                result = subprocess.run(
                    args,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            return {
                "success": True,
                "result": result.stdout,
                "error": ""
            }
        except subprocess.CalledProcessError as e:
            return {
                "success": False,
                "result": e.stdout,
                "error": e.stderr,
                "returncode": e.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "result": "",
                "error": str(e)
            }

