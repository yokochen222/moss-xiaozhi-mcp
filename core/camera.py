
import cv2
import requests
import time

from onvif import ONVIFCamera
from getmac import get_mac_address

class Camera:
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
        # 初始化视频流
        self.videoCapture = cv2.VideoCapture(self.rtsp_url)
        if not self.videoCapture.isOpened():
            raise Exception(f"无法打开视频流：{self.rtsp_url}")

    # 关闭视频流
    def stop_video_stream(self):
        if self.videoCapture and self.videoCapture.isOpened():
            self.videoCapture.release()
            self.videoCapture = None

    # 读取视频流
    def get_video_stream(self, target_size_kb=50):
        # 判断视频流是否已启动
        if not self.videoCapture or not self.videoCapture.isOpened():
            # 未启动则自动启动
            self.start_video_stream()
            initIsOpened = False
        
        for _ in range(5):  # 稳定画面
            ret, frame = self.videoCapture.read()
            if not ret:
                raise Exception("无法读取视频帧")

        quality = 95
        bufferBytes = b''
        while True:
            success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            if not success:
                raise Exception("图像编码失败")
            bufferBytes = buffer.tobytes()
            current_size_kb = len(bufferBytes) / 1024
            if current_size_kb <= target_size_kb or quality <= 10:
                break
            quality -= 5
        return bufferBytes

    #画面截取并识别
    def capture_and_recognize(self, question: str) -> dict:
        try:
            img = self.get_video_stream()
        except Exception as e:
            return {"success": False, "error": f"视频流获取失败: {str(e)}"}
        files = { 'file': ('camera.jpg', img, 'image/jpeg') }
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
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"success": False, "result": str(e)}


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

