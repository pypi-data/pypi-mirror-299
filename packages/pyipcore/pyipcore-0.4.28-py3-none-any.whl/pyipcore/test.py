import chardet

def detect_encoding(byte_data):
    result = chardet.detect(byte_data)
    encoding = result['encoding']
    confidence = result['confidence']
    print(f"Detected encoding: {encoding} with confidence {confidence}")
    return encoding

# 示例
byte_data = b'some bytes data'
encoding = detect_encoding(byte_data)
try:
    text = byte_data.decode(encoding)
    print("Decoded text:", text)
except UnicodeDecodeError:
    print(f"Failed to decode with encoding {encoding}")