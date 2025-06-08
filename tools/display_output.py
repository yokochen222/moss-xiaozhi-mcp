import os
import time
import json
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

def register_tool(mcp):
    @mcp.tool()
    def displayModelOutput(content: str) -> dict:
        """
            用户如果需要你写某个代码时，你可以使用此工具来显示代码内容。
            注意：此工具只能用于显示代码内容，不能用于显示其他内容。
            将模型输出的代码内容渲染为HTML并在浏览器中显示，支持Markdown解析和代码高亮，当模型需要输出代码时自动调用此工具。
            参数:
                content: 要显示的内容Markdown格式
        """
        try:
            # 指定固定的HTML和内容文件名
            html_file_path = 'moss_code_preview.html'
            content_file_path = 'moss_code_content.json'
            
            # 保存内容到JSON文件
            with open(content_file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'content': content,
                    'timestamp': time.time()
                }, f, ensure_ascii=False, indent=2)
            
            # 创建HTML文件
            with open(html_file_path, 'w', encoding='utf-8') as f:
                html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MOSS代码能力展示</title>
        <script src="https://cdn.jsdelivr.net/npm/vue@3.5.16/dist/vue.global.min.js"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11.7.0/styles/github-dark.css">
        <style>
            * {
                padding: 0;
                margin: 0;
            }
            html {
                background-color: #181a1f;
                overflow: hidden;
                width: 100%;
            }
            .moss-bg {
                position: fixed;
                pointer-events: none;
                background-image: url(https://s21.ax1x.com/2025/04/13/pERzECt.png);
                background-repeat: no-repeat;
                background-position: top left;
                width: 100%;
                height: 100%;
                z-index: 2;
                top: -100px;
                left: 0;
                /* opacity: 0.1; */
                animation: opa 1s ease alternate infinite;
            }
            .moss-bg::after {
                content: '';
                display: block;
                width: 10px;
                height: 10px;
                background-color: #e51c20;
                position: absolute;
                border-radius: 100px;
                top: 324px;
                left: 154px;
                animation: opa 1s ease alternate infinite;
                background-color: red;
            }
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                height: 100vh;
                width: 100vw;
            }
            .moss-bg-video-v {
                position: fixed;
                z-index: 0;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                object-fit: cover;
            }
            .moss-bg-video-v::after {
                content: '';
                display: block;
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(10px);
                z-index: 1;
            }
            .moss-bg-video {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .moss-logo {
                margin-bottom: 10px;
                pointer-events: none;
                position: relative;
                z-index: 3;
            }
            .moss-logo img {
                width: 140px;
            }
            .moss-code-section {
                font-family: 'Courier New', Courier, monospace;
                font-size: 14px;
                line-height: 1.5;
                background-color: rgba(0, 0, 0, 0.6);
                padding: 20px;
                border-radius: 5px;
                width: 768px;
                max-height: 80vh;
                white-space: pre-wrap;
                word-wrap: break-word;
                position: relative;
                color: #fff;
                border: 1px solid #555;
                overflow: hidden;
                z-index: 3;
            }
            .moss-code-box {
                max-height: 80vh;
                overflow: auto;
            }
            .copy-btn {
                background-color: #ff7b72;
                color: #fff;
                border: none;
                padding: 2px 6px;
                border-radius: 5px;
                cursor: pointer;
                margin-bottom: 10px;
                font-size: 12px;
                transition: background-color 0.3s ease;
                position: absolute;
                right: 10px;
                top: 10px;
            }
            @keyframes opa {
                from {
                    opacity: 0.3;
                }
                to {
                    opacity: 0.7;
                }
            }
        </style>
    </head>

    <body>
        <div id="app"></div>
        <script type="module">
            import { marked } from 'https://cdn.jsdelivr.net/npm/marked@4.2.12/lib/marked.esm.js'
            import highlightJs from 'https://cdn.jsdelivr.net/npm/highlight.js@11.11.1/+esm'

            // 对HTML标签进行实体编码，防止被浏览器解析
            function encodeHtmlEntities(str) {
                return str
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#39;');
            }

            marked.setOptions({
                highlight: function (code, lang) {
                    return highlightJs.highlightAuto(code, [lang]).value;
                },
            });

            const { createApp, ref, computed, onMounted } = Vue;
            const app = createApp({
                template: `
                <div class="moss-bg-video-v">
                    <video class="moss-bg-video" src="http://sxi0md7ux.hn-bkt.clouddn.com/video.mp4" autoplay loop muted></video>
                </div>
                <div class="moss-bg"></div>
                <div class="moss-logo"><img src="https://s21.ax1x.com/2025/04/13/pERzZgf.png" /></div>
                <div class="moss-code-section">
                    <button @click="copyCode" class="copy-btn">{{isCopied ? '已复制': '复制'}}</button>
                    <div ref="codeBlockRef" class="moss-code-box">
                        <div v-html="renderedMarkdown"></div>
                    </div>
                </div>`,
                setup() {
                    const markdownContent = ref('');
                    const isCopied = ref(false);
                    const renderedMarkdown = computed(() => marked.parse(markdownContent.value));
                    const codeBlockRef = ref(null);
                    
                    // 从服务器获取Markdown内容
                    const fetchMarkdown = async () => {
                        try {
                            const response = await fetch('/get-markdown');
                            if (!response.ok) {
                                throw new Error('Failed to fetch Markdown content');
                            }
                            const data = await response.json();
                            markdownContent.value = data.content;
                        } catch (err) {
                            console.error('Error fetching Markdown:', err);
                        }
                    };
                    
                    // 初始加载
                    onMounted(() => {
                        fetchMarkdown();
                        
                        // 每2秒定时请求更新
                        setInterval(fetchMarkdown, 2000);
                    });
                    
                    const copyCode = async () => {
                        try {
                            const pureCode = codeBlockRef.value.textContent;
                            await navigator.clipboard.writeText(pureCode);
                            isCopied.value = true;
                        } catch (err) {
                            isCopied.value = false;
                            console.error('复制失败:', err);
                        }
                        setTimeout(() => {
                            isCopied.value = false;
                        }, 2000);
                    };

                    return {
                        markdownContent,
                        isCopied,
                        renderedMarkdown,
                        codeBlockRef,
                        copyCode
                    };
                }
            });

            app.mount('#app');
        </script>
    </body>

    </html>
                """
                
                # 写入HTML内容
                f.write(html_content)
            
            # 启动一个简单的HTTP服务器
            class CustomHandler(SimpleHTTPRequestHandler):
                def end_headers(self):
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    super().end_headers()
                    
                def do_GET(self):
                    if self.path == '/get-markdown':
                        try:
                            # 读取JSON文件内容并返回
                            with open(content_file_path, 'r', encoding='utf-8') as f:
                                content_data = json.load(f)
                            
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            # 将字典转换为JSON字符串并编码为字节流
                            self.wfile.write(json.dumps(content_data).encode('utf-8'))
                        except Exception as e:
                            self.send_error(500, f"Error getting Markdown content: {str(e)}")
                    else:
                        return super().do_GET()
            
            # 如果服务器未启动，则在后台线程中启动
            if not hasattr(displayModelOutput, 'server_thread') or not displayModelOutput.server_thread.is_alive():
                server_address = ('localhost', 8000)
                httpd = HTTPServer(server_address, CustomHandler)
                
                displayModelOutput.server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
                displayModelOutput.server_thread.start()
                
                # 打开浏览器访问HTTP服务器而非本地文件
                webbrowser.open('http://localhost:8000/moss_code_preview.html')
            else:
                # 如果服务器已运行，只需通知用户刷新浏览器
                print("文件已更新，页面将自动更新内容")
            
            return {"success": True, "result": f"内容已在浏览器中显示: http://localhost:8000/moss_code_preview.html"}
        
        except Exception as e:
            print(f"Error in displayModelOutput: {e}")
            return {"success": False, "result": str(e)}
        return {"success": True, "result": f"内容已在浏览器中显示"}