import cv2
from onvif import ONVIFCamera
from scapy.all import ARP, Ether, srp
import os
import uuid
import requests
from datetime import datetime


# 检查是否为 ONVIF 设备并获取 RTSP 地址
def get_onvif_rtsp_url(ip, port=80, user='admin', password='123456'):
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
        # print(f"{ip} 不是 ONVIF 设备或连接失败: {e}")
        return None


# 使用 OpenCV 显示视频流
def display_video(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print(f"当前分辨率: {width}x{height}")

    if not cap.isOpened():
        print("无法打开视频流")
        return

    print("正在播放视频流... 按下 q 键退出")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法读取帧，可能视频流已断开")
            break

        cv2.imshow('ONVIF Camera Stream - Press Q to Exit', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 获取视频帧并编码为字节流
def capture_frame_bytes(rtsp_url, target_size_kb=1024, output_dir="captures"):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        raise Exception("无法打开视频流")

    # 读取几帧以获取稳定画面
    for _ in range(5):
        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise Exception("无法读取视频帧")

    cap.release()

    # 创建截图目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 生成唯一文件名
    now = datetime.now()
    # 格式化输出：年-月-日 时:分:秒
    formatted_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    filename = f"{formatted_time}.jpg"
    file_path = os.path.join(output_dir, filename)

    # 初始质量设置
    quality = 95
    buffer_bytes = b''

    # 尝试降低质量直到满足大小要求
    while True:
        success, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        if not success:
            raise Exception("图像编码失败")
        buffer_bytes = buffer.tobytes()

        current_size_kb = len(buffer_bytes) / 1024
        print(f"当前图像大小: {current_size_kb:.2f} KB, 使用质量等级: {quality}")

        if current_size_kb <= target_size_kb or quality <= 10:
            break  # 达到目标或质量不能再降

        quality -= 5  # 继续降低质量

    # 保存压缩后的图像用于调试
    with open(file_path, 'wb') as f:
        f.write(buffer_bytes)
    print(f"已保存压缩后的图像至: {file_path}")

    return buffer_bytes  # 返回字节流用于上传或其他用途

rtsp_url = ''
def capture(question: str):
    global rtsp_url
    if rtsp_url == '':
        rtsp_url = get_onvif_rtsp_url('192.168.10.110', 8000, 'admin', 'a632662161')

    img = capture_frame_bytes(rtsp_url)
    # 等待用户按键按下（0 表示无限期等待）
    files = {
        'file': ('camera.jpg', img, 'image/jpeg'),
    }
    data = {
        'question': question,
    }
    headers = {
        "Authorization": "Bearer test-token",
        "Device-Id": "5c:aa:f4:cc:b8:dd",
        "Client-Id": "5c:aa:f4:cc:b8:dd",
    }
    try:
        response = requests.post('https://api.xiaozhi.me/vision/explain', headers=headers, files=files,data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {"success": False, "result": "请求失败"}

# 4. 主程序逻辑
if __name__ == '__main__':
    img = capture('你在看什么？')
    print(img)