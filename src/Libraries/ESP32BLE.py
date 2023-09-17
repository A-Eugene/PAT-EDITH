"""
    ESP32BLE.py by A Eugene

    Bluetooth Low Energy manager library for ESP32 microcontroller.
"""

from machine import Pin, Timer
from time import sleep_ms
import ubluetooth

class ESP32_BLE():
    def __init__(self, name: str, blinkLED: bool):
        self.led = Pin(2, Pin.OUT)
        self.led.off()

        if blinkLED:
            self.btLEDTimer = Timer(0)
            self.btLEDTimer.deinit()
            self.btLEDTimer.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))
        
        # Default Properties
        self.name = name
        self.blinkLED = blinkLED
        self.connected = False
        self.message = ""
        
        # BLE stuffs
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

        # For Events
        self.on_connected_callbacks = []
        self.on_disconnected_callbacks = []
        self.on_message_callbacks = []

    # Register a permanent event handler
    def on(self, event: str, callback):
        if event == 'connected':
            self.on_connected_callbacks.append(callback)
        elif event == 'disconnected':
            self.on_disconnected_callbacks.append(callback)
        elif event == 'message':
            self.on_message_callbacks.append(callback)
        else:
            raise Exception('BLE event name is not recognized!')

    # On BLE event
    def ble_irq(self, event, data):
        if event == 1: #_IRQ_CENTRAL_CONNECT:
            if self.blinkLED:
                self.led.value(1)
                self.btLEDTimer.deinit()

            self.connected = True
            
            # Call all callbacks
            for callback in self.on_connected_callbacks:
                callback()

        elif event == 2: #_IRQ_CENTRAL_DISCONNECT:
            if self.blinkLED:
                self.btLEDTimer.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))

            self.advertiser()
            self.connected = False

            # Call all callbacks
            for callback in self.on_disconnected_callbacks:
                callback()
        elif event == 3: #_IRQ_GATTS_WRITE:
            message = self.ble.gatts_read(self.rx).decode('UTF-8') 

            # Call all callbacks
            for callback in self.on_message_callbacks:
                callback(message)
            
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02', 'UTF-8') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        # adv_data
        # raw: 0x02010209094553503332424C45 
        # b'x02x01x02ttESP32BLE'
        #
        # 0x02 - General discoverable mode
        # 0x01 - AD Type = 0x01
        # 0x02 - value = 0x02
        
        # https://jimmywongiot.com/2019/08/13/advertising-payload-format-on-ble/
        # https://docs.silabs.com/bluetooth/latest/general/adv-and-scanning/bluetooth-adv-data-basics
