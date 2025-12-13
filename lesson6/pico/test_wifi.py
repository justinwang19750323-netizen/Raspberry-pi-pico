# test_wifi.py - 測試 WiFi 連線的範例程式
# 這個檔案示範如何正確使用 wifi_connect 模組

import wifi_connect as wifi

# 嘗試連線 WiFi
wifi.connect()

# 顯示 IP
print("IP:", wifi.get_ip())

# 建立 MQTT 連線
if wifi.test_internet():
    print("已連接到網際網路")
else:
    print("無法連接到網際網路")

