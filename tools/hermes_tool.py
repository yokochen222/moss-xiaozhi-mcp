import subprocess
import os
import sys
from dotenv import dotenv_values


def get_default_provider():
    """动态获取 Hermes 当前配置的默认 Provider"""
    try:
        result = subprocess.run(["hermes", "config", "show"], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'provider:' in line.lower():
                return line.split(':')[-1].strip()
    except Exception:
        pass
    return "deepseek"


def register_tool(mcp):
    @mcp.tool()
    def hermes_send_task(task: str) -> dict:
        """
        向 Hermes 下发任务。任务会异步发送，立即返回成功。
        适用于需要快速响应的场景，避免因等待 Hermes 回复而超时。
        :param task: 要下发的任务内容
        :return: 包含下发结果的字典
        """
        try:
            hermes_env_path = os.path.expanduser("~/.hermes/.env")
            hermes_env_vars = dotenv_values(hermes_env_path)
            env = os.environ.copy()
            env.update(hermes_env_vars)

            current_provider = get_default_provider()
            command = [
                "hermes",
                "chat",
                "-q", task,
                "--provider", current_provider
            ]

            # 启动进程后直接返回，不等待结果
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env
            )

            return {
                "success": True,
                "message": f"任务已下发: {task}",
                "error": ""
            }
        except Exception as e:
            return {
                "success": False,
                "message": "",
                "error": str(e)
            }
