import cv2
from onvif import ONVIFCamera
from scapy.all import ARP, Ether, srp
import os
import uuid
import requests
from datetime import datetime
from dotenv import load_dotenv  # 新增
import time

# 加载 .env 文件
load_dotenv()

# 从环境变量中读取摄像头配置
CAMERA_USERNAME = os.getenv("CAMERA_USERNAME", "admin")
CAMERA_PWD = os.getenv("CAMERA_PWD", "Cc5201314")
CAMERA_URL = os.getenv("CAMERA_URL", "192.168.10.104")
CAMERA_PORT = int(os.getenv("CAMERA_PORT", "8000"))
CAMERA_MAC = os.getenv("CAMERA_MAC", "98:a3:16:e7:c4:68")

# 检查是否为 ONVIF 设备并获取 RTSP 地址
def get_onvif_rtsp_url(ip=CAMERA_URL, port=CAMERA_PORT, user=CAMERA_USERNAME, password=CAMERA_PWD):
    try:
        cam = ONVIFCamera(ip, port, user, password)
        media_service = cam.create_media_service()
        profiles = media_service.GetProfiles()
        if not profiles:
            return None

        token = profiles[0].token

        stream = media_service.GetStreamUri({
            'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': 'RTSP'},
            'ProfileToken': token
        })
        stream_uri = stream.Uri

        rtsp_url = stream_uri.replace('rtsp://', f'rtsp://{user}:{password}@')
        print(f"设备 {ip} 支持 ONVIF，RTSP 地址：{rtsp_url}")

        return rtsp_url

    except Exception as e:
        print(f"🔴 获取 RTSP 地址失败: {str(e)}")
        return None


# 启动 RTSP 视频流
def start_rtsp():
    rtsp_url = get_onvif_rtsp_url(CAMERA_URL, CAMERA_PORT, CAMERA_USERNAME, CAMERA_PWD)
    if not rtsp_url:
        raise Exception("⚠️ 无法获取 RTSP 地址，请检查：\n"
                        "1. 摄像头是否支持 ONVIF\n"
                        "2. IP、端口是否正确\n"
                        "3. 账号密码是否正确\n"
                        "4. 网络是否通畅")

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        raise Exception(f"❌ 无法打开视频流：{rtsp_url}")

    print("🟢 RTSP 视频流已成功打开")
    return cap


# 关闭 RTSP 视频流
def release_rtsp(cap):
    if cap and cap.isOpened():
        cap.release()
        print("🛑 RTSP 视频流已关闭")


# 获取视频帧并编码为字节流（修改为接受 cap 参数）
def capture_frame_bytes(cap, target_size_kb=1024, output_dir="captures"):
    for _ in range(5):  # 稳定画面
        ret, frame = cap.read()
        if not ret:
            raise Exception("❌ 无法读取视频帧")

    os.makedirs(output_dir, exist_ok=True)
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"{formatted_time}.jpg"
    file_path = os.path.join(output_dir, filename)

    quality = 95
    buffer_bytes = b''
    while True:
        success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        if not success:
            raise Exception("❌ 图像编码失败")
        buffer_bytes = buffer.tobytes()
        current_size_kb = len(buffer_bytes) / 1024
        print(f"当前图像大小: {current_size_kb:.2f} KB, 使用质量等级: {quality}")
        if current_size_kb <= target_size_kb or quality <= 10:
            break
        quality -= 5

    with open(file_path, 'wb') as f:
        f.write(buffer_bytes)
    print(f"✅ 已保存压缩后的图像至: {file_path}")

    return buffer_bytes




def control_ptz(direction: str, speed: float, ip=CAMERA_URL, port=CAMERA_PORT, user=CAMERA_USERNAME, password=CAMERA_PWD):
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
        cam = ONVIFCamera(ip, port, user, password)
        ptz = cam.create_ptz_service()
        media = cam.create_media_service()

        # 获取配置文件
        profile = media.GetProfiles()[0]

        # 创建移动请求
        request = ptz.create_type('ContinuousMove')
        request.ProfileToken = profile.token

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
        ptz.Stop({'ProfileToken': profile.token})

        return {"success": True, "message": f"云台已向{direction}方向移动"}

    except Exception as e:
        print(f"🔴 云台控制失败: {str(e)}")
        return {"success": False, "error": str(e)}

# 全局变量用于缓存视频流对象
rtsp_cap = None


# 主函数：拍照 + 上传
def capture(question: str):
    global rtsp_cap
    if rtsp_cap is None or not rtsp_cap.isOpened():
        rtsp_cap = start_rtsp()

    img = capture_frame_bytes(rtsp_cap)
    files = {
        'file': ('camera.jpg', img, 'image/jpeg'),
    }
    data = {
        'question': question,
    }
    headers = {
        "Authorization": "Bearer test-token",
        "Device-Id": CAMERA_MAC,
        "Client-Id": CAMERA_MAC,
    }

    try:
        response = requests.post('https://api.xiaozhi.me/mcp/vision/explain', headers=headers, files=files, data=data)
        response.raise_for_status()

        # 成功后关闭视频流
        release_rtsp(rtsp_cap)
        rtsp_cap = None

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {"success": False, "result": "请求失败"}


# 主程序逻辑
if __name__ == '__main__':
    result = capture('你在看什么？')
    print(result)