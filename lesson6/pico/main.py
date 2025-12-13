import wifi_connect as wifi
import time
from umqtt.simple import MQTTClient

# MQTT 設定
MQTT_BROKER = "172.20.10.3"  # 公開測試用 Broker
MQTT_PORT = 1883
CLIENT_ID = "pico_w_publisher"
TOPIC = "pico/test"

# 嘗試連線 WiFi
wifi.connect()

# 顯示 IP
print("IP:", wifi.get_ip())

# 建立 MQTT 連線（加入錯誤處理和重試機制）
print("正在連接 MQTT Broker...")
max_retries = 5
retry_delay = 2  # 秒

for attempt in range(max_retries):
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=60)
        client.connect()
        print(f"✅ 已連接到 {MQTT_BROKER}")
        break
    except OSError as e:
        error_code = e.args[0] if e.args else "unknown"
        print(f"❌ 連接失敗 (嘗試 {attempt + 1}/{max_retries}): 錯誤碼 {error_code}")
        
        if error_code == 103:  # ECONNABORTED
            print("   原因：連接被中止")
            print("   可能原因：")
            print("   - MQTT Broker 無法訪問或未運行")
            print("   - 網絡連接不穩定")
            print("   - 防火牆阻擋連接")
            print("   - IP 地址或端口錯誤")
        elif error_code == 113:  # EHOSTUNREACH
            print("   原因：無法到達主機")
        elif error_code == 110:  # ETIMEDOUT
            print("   原因：連接超時")
        elif error_code == 111:  # ECONNREFUSED
            print("   原因：連接被拒絕（Broker 可能未運行或端口錯誤）")
        else:
            print(f"   詳細錯誤: {e}")
        
        if attempt < max_retries - 1:
            print(f"   {retry_delay} 秒後重試...")
            time.sleep(retry_delay)
        else:
            print("❌ 連接失敗，已達最大重試次數")
            raise

# 每隔 10 秒發布一次訊息
counter = 0
while True:
    counter += 1
    message = f"Hello from Pico W! #{counter}"
    
    print("-" * 30)
    client.publish(TOPIC, message)
    print(f"已發布訊息: {message}")
    print(f"主題: {TOPIC}")
    
    print("等待 10 秒後再次發布...")
    time.sleep(10)

