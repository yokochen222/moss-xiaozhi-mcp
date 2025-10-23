import sys
import os
from core.ha import ha_requet

def get_homeassistant_devices():
    url = '/api/states'
    response = ha_requet(url, 'GET', {})
    return response

def register_tool(mcp):
    @mcp.tool()
    def set_xiaomi_screen_light_status_tool(action: str) -> dict:
      """
        提供控制小米屏幕挂灯1s开关功能
        参数：
          action: 控制内容，值解释如下
          'open': 打开灯
          'close': 关闭灯
        返回：
          成功返回：{'success': True, 'result': '控制成功'}
          失败返回：{'success': False, 'result': '控制失败'}
      """
      action = action.strip()
      # HA 中设备实体ID
      entity_id = "light.yeelink_cn_620529130_lamp22_s_2"
      try:

        if action == 'open':
          url = '/api/services/light/turn_on'
        else:
          url = '/api/services/light/turn_off'

        # 请求参数
        payload = {"entity_id": entity_id}
        
        # 发送控制请求
        response = ha_requet(url, 'POST', payload)

        return {'success': True, 'result': response}
      except Exception as e:
        return {'success': False, 'result': str(e)}
      
    @mcp.tool()
    def get_xiaomi_screen_light_status_tool() -> dict:
      """
        提供获取小米屏幕挂灯1s开关状态功能
        参数：
          None
        返回：
          {'success': True, 'result': '灯状态'}
          {'success': False, 'result': '获取失败'}
      """
      entity_id = "light.yeelink_cn_620529130_lamp22_s_2"
      url = '/api/states/' + entity_id
      response = ha_requet(url, 'GET', {})
      return response 
