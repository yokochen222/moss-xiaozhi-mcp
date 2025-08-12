
import cv2
import requests
import time
import os
import datetime
import threading

from onvif import ONVIFCamera
from getmac import get_mac_address

class Camera:
    captures_dir = 'captures'
    _stream_thread = None
    _stream_active = False
    _latest_frame = None
    _frame_lock = threading.Lock()
    
    def _ensure_captures_dir_exists(self):
        """确保captures目录存在"""
        if not os.path.exists(self.captures_dir):
            os.makedirs(self.captures_dir)
            return True
        return False
    
    def __init__(self, ip, port, user, password):
        self.mac_address = get_mac_address()
        self.videoCapture = None
        try:
            self.__init_camera(ip, port, user, password)
        except Exception as e:
            raise Exception(f"摄像头初始化失败: {str(e)}")

    # 初始化摄像头 并 拉取视频流
    def __init_camera(self, ip, port, user, password):
        camera = ONVIFCamera(ip, port, user, password)
        media_service = camera.create_media_service()
        profiles = media_service.GetProfiles()
        if not profiles or len(profiles) == 0:
            raise Exception(f"摄像头连接失败，请检查摄像头配置是否正确。")
        
        token = profiles[0].token

        streamUri = media_service.GetStreamUri({
            'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': 'RTSP'},
            'ProfileToken': token
        })

        self.token = token
        self.rtsp_url = streamUri.Uri.replace('rtsp://', f'rtsp://{user}:{password}@')
        self.camera = camera

    # 启动视频流
    def start_video_stream(self):
        # 初始化视频流，设置低延迟模式
        self.videoCapture = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        
        # 设置RTSP选项以减少延迟
        self.videoCapture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.videoCapture.set(cv2.CAP_PROP_FPS, 30)
        
        if not self.videoCapture.isOpened():
            # 尝试使用不同的后端
            self.videoCapture = cv2.VideoCapture(self.rtsp_url)
            if not self.videoCapture.isOpened():
                raise Exception(f"无法打开视频流：{self.rtsp_url}")

        # 读取一帧来确保流已启动
        ret, _ = self.videoCapture.read()
        if not ret:
            raise Exception("无法读取视频流的第一帧")

    # 关闭视频流
    def stop_video_stream(self):
        self._stream_active = False
        if self._stream_thread:
            self._stream_thread.join()
        if self.videoCapture and self.videoCapture.isOpened():
            self.videoCapture.release()
            self.videoCapture = None
        self._latest_frame = None

    # 后台线程持续获取视频流
    def _stream_worker(self):
        while self._stream_active:
            ret, frame = self.videoCapture.read()
            if ret:
                with self._frame_lock:
                    self._latest_frame = frame
            time.sleep(0.01)
    
    # 读取视频流
    def get_video_stream(self, target_size_kb=50):
        # 如果后台线程未运行，则启动
        if not self._stream_active:
            if not self.videoCapture or not self.videoCapture.isOpened():
                self.start_video_stream()
            self._stream_active = True
            self._stream_thread = threading.Thread(target=self._stream_worker)
            self._stream_thread.daemon = True
            self._stream_thread.start()
            
            # 等待第一帧数据
            max_wait = 5  # 最大等待秒数
            start_time = time.time()
            while time.time() - start_time < max_wait:
                with self._frame_lock:
                    if self._latest_frame is not None:
                        break
                time.sleep(0.1)
            else:
                raise Exception("视频流连接超时")
        
        # 获取最新帧
        with self._frame_lock:
            if self._latest_frame is None:
                raise Exception("无法获取视频帧")
            frame = self._latest_frame

        # 优化图像编码逻辑
        quality = 90  # 稍微降低初始质量
        max_quality_steps = 5  # 限制质量调整次数
        step_count = 0
        bufferBytes = b''

        while True:
            success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            if not success:
                raise Exception("图像编码失败")
            bufferBytes = buffer.tobytes()
            current_size_kb = len(bufferBytes) / 1024

            if current_size_kb <= target_size_kb or quality <= 10 or step_count >= max_quality_steps:
                break
            
            # 动态调整质量步长
            if current_size_kb > target_size_kb * 1.5:
                quality -= 10
            else:
                quality -= 5
            step_count += 1
        
        return bufferBytes

    #画面截取并识别
    def capture_and_recognize(self, question: str) -> dict:
        try:
            img = self.get_video_stream()
        except Exception as e:
            return {"success": False, "error": f"视频流获取失败: {str(e)}"}
        
        # 生成唯一的图片名称（使用时间戳）
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        img_name = f'capture_{timestamp}.jpg'
        
        # 确保captures目录存在
        self._ensure_captures_dir_exists()
        
        if os.environ.get('ONVIF_CAMERA_CAPTURE') == 'true':
            # 保存图片到captures目录
            img_path = os.path.join(self.captures_dir, img_name)
            with open(img_path, 'wb') as f:
                f.write(img)
        
        files = { 'file': (img_name, img, 'image/jpeg') }
        data = {
            'question': question,
        }
        headers = {
            "Authorization": "Bearer test-token",
            "Device-Id": self.mac_address,
            "Client-Id": self.mac_address,
        }

        try:
            response = requests.post('https://api.xiaozhi.me/vision/explain', headers=headers, files=files, data=data)
            response.raise_for_status()
            result = response.json()
            # 确保captures目录存在
            self._ensure_captures_dir_exists()

            if os.environ.get('ONVIF_CAMERA_LOG') == 'true':
                log_path = os.path.join(self.captures_dir, 'log.txt')
                with open(log_path, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"时间: {timestamp}\n")
                    log_file.write(f"图片名称: {img_name}\n")
                    log_file.write(f"响应结果: {result}\n")
                    log_file.write("--------------------\n")
            
            return result
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            
            # 记录错误日志到log.txt
            # 确保captures目录存在
            self._ensure_captures_dir_exists()
            
            # 日志文件路径设置为captures目录下
            log_path = os.path.join(self.captures_dir, 'log.txt')
            with open(log_path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"时间: {timestamp}\n")
                log_file.write(f"图片名称: {img_name}\n")
                log_file.write(f"错误信息: {error_msg}\n")
                log_file.write("--------------------\n")
            
            return {"success": False, "result": error_msg}


    def control_ptz(self, direction: str, speed: float):
        """
        控制摄像头云台
        :param direction: 方向 ('up', 'down', 'left', 'right',
                                'top-left', 'top-right', 'bottom-left', 'bottom-right')
        :param speed: 速度 (0.1-1.0)
        :param ip: 摄像头IP
        :param port: 摄像头端口
        :param user: 用户名
        :param password: 密码
        :return: 操作结果
        """
        try:
            # 验证速度范围
            if not 0.1 <= speed <= 1.0:
                raise ValueError("速度必须在0.1到1.0之间")

            # 连接ONVIF摄像头
            cam = self.camera
            ptz = cam.create_ptz_service()
            media = cam.create_media_service()

            # 获取配置文件
            profile = media.GetProfiles()[0]

            # 创建移动请求
            request = ptz.create_type('ContinuousMove')
            request.ProfileToken = self.token

            # 定义各方向参数
            directions = {
                'up':           {'x': 0.0,     'y': speed},
                'down':         {'x': 0.0,     'y': -speed},
                'left':         {'x': -speed,  'y': 0.0},
                'right':        {'x': speed,   'y': 0.0},
                'top-left':     {'x': -speed,  'y': speed},
                'top-right':    {'x': speed,   'y': speed},
                'bottom-left':  {'x': -speed,  'y': -speed},
                'bottom-right': {'x': speed,   'y': -speed}
            }

            if direction not in directions:
                raise ValueError(f"无效的方向: {direction}")

            request.Velocity = {'PanTilt': directions[direction], 'Zoom': {'x': 0}}

            # 执行移动
            ptz.ContinuousMove(request)
            # 移动持续时间（可根据需要调整）
            time.sleep(1)
            # 停止移动
            ptz.Stop({'ProfileToken': self.token})

            return {"success": True, "message": f"云台已向{direction}方向移动"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def show_live_feed(self, window_name='Live Camera Feed'):
        """
        显示实时摄像头画面
        :param window_name: 窗口名称
        """
        try:
            # 检查视频流是否已启动
            if not self.videoCapture or not self.videoCapture.isOpened():
                self.start_video_stream()
            
            print(f"正在显示实时画面。按 'q' 键退出...")
            
            # 创建显示窗口
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            
            while True:
                # 读取视频帧
                ret, frame = self.videoCapture.read()
                if not ret:
                    print("无法读取视频帧，退出实时画面")
                    break
                
                # 显示帧
                cv2.imshow(window_name, frame)
                
                # 按下 'q' 键退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        except Exception as e:
            print(f"实时画面显示出错: {str(e)}")
        finally:
            # 关闭窗口
            cv2.destroyWindow(window_name)