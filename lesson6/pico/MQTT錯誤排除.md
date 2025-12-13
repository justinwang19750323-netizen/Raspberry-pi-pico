# MQTT 連接錯誤排除指南

## 錯誤碼 103: ECONNABORTED

### 錯誤說明
**ECONNABORTED** 表示連接被中止，通常發生在建立 TCP 連接的過程中。

### 常見原因

1. **MQTT Broker 無法訪問**
   - Broker 未運行
   - IP 地址或端口錯誤
   - 網絡路由問題

2. **網絡連接問題**
   - WiFi 連接不穩定
   - 網絡延遲過高
   - 防火牆阻擋

3. **Broker 配置問題**
   - 只允許本地連接（綁定到 127.0.0.1）
   - 未正確監聽指定端口

### 排查步驟

#### 1. 檢查 MQTT Broker 狀態（在 Raspberry Pi 上）

```bash
# 檢查 mosquitto 是否運行
sudo systemctl status mosquitto

# 如果未運行，啟動它
sudo systemctl start mosquitto

# 檢查監聽的端口
sudo netstat -tlnp | grep 1883
# 或
sudo ss -tlnp | grep 1883
```

#### 2. 檢查 Broker 配置

檢查 `/etc/mosquitto/mosquitto.conf`：

```bash
sudo nano /etc/mosquitto/mosquitto.conf
```

確保包含：
```
listener 1883
allow_anonymous true  # 或配置認證
bind_address 0.0.0.0  # 允許外部連接（如果只允許本地，用 127.0.0.1）
```

#### 3. 檢查網絡連接

從 Raspberry Pi 測試連接：

```bash
# 測試 Broker 是否可訪問
mosquitto_pub -h 172.20.10.3 -p 1883 -t "test" -m "hello"
mosquitto_sub -h 172.20.10.3 -p 1883 -t "test" -v
```

#### 4. 檢查防火牆

```bash
# 允許 MQTT 端口
sudo ufw allow 1883/tcp
sudo ufw status
```

#### 5. 在 Pico W 上檢查 WiFi 連接

確保 WiFi 連接成功，並且可以訪問網絡。

#### 6. 使用本地 Broker（如果外部無法連接）

如果 `172.20.10.3` 無法訪問，可以嘗試使用本機 IP：

```python
# 在 main.py 中修改
MQTT_BROKER = "localhost"  # 如果在同一設備上
# 或
MQTT_BROKER = "192.168.1.x"  # 您的 Raspberry Pi 實際 IP
```

### 其他常見錯誤碼

- **103 ECONNABORTED**: 連接被中止
- **110 ETIMEDOUT**: 連接超時
- **111 ECONNREFUSED**: 連接被拒絕（Broker 未運行或端口錯誤）
- **113 EHOSTUNREACH**: 無法到達主機（網絡路由問題）

### 解決方案

1. **使用重試機制**（已在代碼中實現）
   - 自動重試連接
   - 添加延遲避免過度請求

2. **增加 keepalive 時間**
   ```python
   client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, keepalive=60)
   ```

3. **檢查網絡穩定性**
   - 確保 WiFi 信號強度足夠
   - 檢查路由器設置

4. **使用本地 Broker**
   - 如果可能，在本地網絡設置 MQTT Broker
   - 避免使用外部不可靠的服務

### 測試步驟

1. 確認 Broker 運行：`sudo systemctl status mosquitto`
2. 測試本地連接：`mosquitto_sub -h localhost -t "test" -v`
3. 測試網絡連接：`mosquitto_pub -h 172.20.10.3 -t "test" -m "test"`
4. 運行 Pico W 程序並觀察錯誤訊息

