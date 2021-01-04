import wifiConnector
import network

network_station = network.WLAN(network.STA_IF)

connector = wifiConnector.WiFiConnector(network_station, "SBG6900AC-E2B1E", "02a781cb4a")
# connector = wifiConnector.WiFiConnector(network_station, "wifi-iot", "!!P1l@rRDMC!!")
connector.connect()


