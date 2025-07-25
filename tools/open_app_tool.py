import subprocess
import platform

system = platform.system()

# *** 注意：windows 平台下 应用安装路径需要自行修改绝对路径例：'C:\\Program Files (x86)\\Tencent\\WeChat\\WeChat.exe'

def register_tool(mcp):
    @mcp.tool()
    def open_app_tool(argument: str, payload='') -> dict:
        """
        提供打开电脑应用的功能
        目前提供的应用有：
            1. 终端：打开终端：启动参数指令为：'Terminal'
            2. 汽水音乐：打开汽水音乐：参数指令为：'/Applications/汽水音乐.app'
            3. 微信：打开微信：参数指令为：'/Applications/WeChat.app'
            4. 企业微信：打开企业微信：参数指令为：'/Applications/企业微信.app'
            5. 浏览器：打开浏览器：参数指令为：'/Applications/Google Chrome.app'；默认打开的页面为浏览器默认主页，如果需要打开特定网站需要提供第二个参数 payload，payload 为网站的 URL，
            如果需要打开哔哩哔哩搜索特定内容网址为：https://search.bilibili.com/all?keyword=这里填写需要搜索的内容名称
            如果需要打开淘宝搜索特定商品网址为：https://s.taobao.com/search?q=这里填写需要搜索的商品名称
            如果需要打开腾讯视频搜索特定电视剧或者电影名称网址为：https://v.qq.com/x/search/?q=这里填写电视或者电影的名称
            如果需要搜索某个问题可以调用bing搜索工具，网址为：https://cn.bing.com/search?q=这里填写要搜索的问题
            注意：参数指令不能有空格，必须遵循大小写，否则会报错。如果要打开的不是声明中的应用，则尝试使用浏览器搜索打开，此时需要提供第二个参数 payload，payload 为网站的 URL
        """
        argument = argument.strip()
        try:
            if system == 'Darwin':
                if payload != '':
                    result = subprocess.run(["open", "-a", argument, payload], check=True)
                    return {"success": True, "result": result}
                result = subprocess.run(["open", "-a", argument], check=True)
                return {"success": True, "result": result}
            elif system == 'Windows':
                if payload != '':
                    result = subprocess.run([argument, payload], check=True)
                    return {"success": True, "result": result}
                else:
                    result = subprocess.run([argument], check=True)
                    return {"success": True, "result": result}
            
            return {"success": False, "result": "当前系统不支持该功能"}
        except subprocess.CalledProcessError as e:
            return {"success": False, "result": str(e)}
