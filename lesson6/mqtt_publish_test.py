#!/usr/bin/env python3
"""
簡單的 MQTT Publish 測試程式
用於快速測試 MQTT 訊息發布功能
"""

import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime

# ========== 設定區域 ==========
BROKER = "localhost"      # MQTT Broker 位址
PORT = 1883               # MQTT 埠號
TOPIC = "test/topic"      # 發布的主題
QOS = 1                   # 訊息品質等級 (0, 1, 2)
# ==============================

def on_connect(client, userdata, flags, reason_code, properties):
    """連線成功時的回調函數"""
    if reason_code.is_failure:
        print(f"❌ 連線失敗，錯誤代碼: {reason_code}")
    else:
        print(f"✅ 成功連接到 MQTT Broker: {BROKER}:{PORT}")

def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """訊息發布成功時的回調函數"""
    print(f"✅ 訊息已成功發布 (Message ID: {mid})")

def publish_simple_message(client):
    """發布簡單文字訊息"""
    print("\n--- 測試 1: 發布簡單文字訊息 ---")
    message = f"Hello MQTT! 時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    result = client.publish(TOPIC, message, qos=QOS)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"✅ 訊息已發布到主題: {TOPIC}")
        print(f"   內容: {message}")
    else:
        print(f"❌ 發布失敗，錯誤代碼: {result.rc}")
    
    time.sleep(0.5)

def publish_json_message(client):
    """發布 JSON 格式訊息"""
    print("\n--- 測試 2: 發布 JSON 格式訊息 ---")
    data = {
        "device": "Raspberry Pi",
        "temperature": 25.5,
        "humidity": 60,
        "status": "正常",
        "timestamp": datetime.now().isoformat()
    }
    
    json_message = json.dumps(data, ensure_ascii=False)
    result = client.publish(TOPIC, json_message, qos=QOS)
    
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"✅ JSON 訊息已發布到主題: {TOPIC}")
        print(f"   內容: {json_message}")
    else:
        print(f"❌ 發布失敗，錯誤代碼: {result.rc}")
    
    time.sleep(0.5)

def publish_multiple_messages(client, count=5):
    """連續發布多筆訊息"""
    print(f"\n--- 測試 3: 連續發布 {count} 筆訊息 ---")
    for i in range(count):
        message = f"測試訊息 #{i+1} - {datetime.now().strftime('%H:%M:%S')}"
        result = client.publish(TOPIC, message, qos=QOS)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"✅ [{i+1}/{count}] {message}")
        else:
            print(f"❌ [{i+1}/{count}] 發布失敗")
        
        time.sleep(1)  # 每秒發布一筆
    
    print(f"\n✅ 已發布所有 {count} 筆訊息")

def main():
    """主程式"""
    print("=" * 60)
    print(" MQTT Publish 測試程式")
    print("=" * 60)
    print(f"\n設定:")
    print(f"  Broker: {BROKER}:{PORT}")
    print(f"  主題: {TOPIC}")
    print(f"  QoS: {QOS}")
    print("\n請確保 MQTT Broker 正在運行...\n")
    
    try:
        # 建立 MQTT 客戶端
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect
        client.on_publish = on_publish
        
        # 連接到 Broker
        print(f"正在連接到 {BROKER}...")
        client.connect(BROKER, PORT, 60)
        client.loop_start()  # 開始背景執行緒
        
        # 等待連線建立
        time.sleep(1)
        
        # 執行測試
        publish_simple_message(client)
        publish_json_message(client)
        publish_multiple_messages(client, count=5)
        
        # 等待所有訊息發布完成
        time.sleep(1)
        
        # 關閉連線
        client.loop_stop()
        client.disconnect()
        print("\n✅ MQTT 連線已關閉")
        print("\n測試完成！")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  使用者中斷程式")
        if 'client' in locals():
            client.loop_stop()
            client.disconnect()
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        if 'client' in locals():
            client.loop_stop()
            client.disconnect()

if __name__ == "__main__":
    main()

