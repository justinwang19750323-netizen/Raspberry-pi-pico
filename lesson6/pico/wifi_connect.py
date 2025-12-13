# wifi_connect.py - 作為 wifi.py 的別名模組
# 重新導出 wifi 模組的所有功能

from wifi import (
    connect,
    disconnect,
    is_connected,
    get_ip,
    test_internet,
    WIFI_SSID,
    WIFI_PASSWORD
)

