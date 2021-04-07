from web_control.lighting_request import LightingRequest
import json

raw_request_template = b"""PUT /lighting HTTP/1.1\r\nHost: 192.168.0.2\r\nConnection: keep-alive\r\nContent-Length: 
54\r\nPostman-Token: 0dcb8d52-e83a-3642-0228-f002a1600693\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (
Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 
Safari/537.36\r\nContent-Type: application/json\r\nAccept: */*\r\nOrigin: 
chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,
en;q=0.9\r\n\r\n[commands] """


def create_request(commands):
    raw_request = raw_request_template.replace(b"[commands]", json.dumps(commands).encode("utf-8"))
    return LightingRequest(raw_request)
