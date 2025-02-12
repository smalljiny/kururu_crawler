import os
import pickle
import json
import zlib
import brotli
import zstandard as zstd

# https://pypi.org/project/selenium-wire/

def headers_to_dict(headers):
    return {key: value for key, value in headers}

def decode_content(content, encoding):
    try:
        if encoding == 'gzip':
            return zlib.decompress(content, zlib.MAX_WBITS | 16)
        elif encoding == 'deflate':
            return zlib.decompress(content)
        elif encoding == 'br':
            return brotli.decompress(content)
        elif encoding == 'zstd':
            dctx = zstd.ZstdDecompressor()
            # 스트리밍 방식으로 압축 해제
            with dctx.stream_reader(content) as reader:
                decompressed = reader.read()  # 전체 데이터를 읽어들임
            return decompressed
    except (zlib.error, brotli.error, zstd.ZstdError) as e:
        print(f"Decompression error: {e} / {encoding}")
        return content  # Return original content if decompression fails
    return content

def save_binary_content(content, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(content)

def collect_request_response_data(directory):
    data = []
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            request_file = os.path.join(root, dir_name, "request")
            response_file = os.path.join(root, dir_name, "response")
            
            entry = {"request": {}, "response": {}}
            
            if os.path.exists(request_file):
                with open(request_file, "rb") as f:
                    request = pickle.load(f)
                entry["id"] = request.id    
                entry["request"] = {
                    "url": request.url,
                    "method": request.method,
                    "headers": headers_to_dict(request.headers._headers),
                    "body": request.body,
                    "params": request.params,
                    "path": request.path,
                    "querystring": request.querystring,
                    "host": request.host,
                    "date": request.date,
                    "cert": request.cert,
                    "response": request.response,
                    "ws_messages": request.ws_messages
                }
            
            if os.path.exists(response_file):
                with open(response_file, "rb") as f:
                    response = pickle.load(f)
                
                content_encoding = response.headers.get('Content-Encoding', '')
                content_type = response.headers.get('Content-Type', '')
                body = decode_content(response.body, content_encoding)
                
                if 'text' in content_type or 'javascript' in content_type or 'json' in content_type:
                    body = body.decode('utf-8', errors='replace')
                    if 'json' in content_type:
                        try:
                            body = json.loads(body)
                        except json.JSONDecodeError:
                            pass
                elif 'image' in content_type:
                    save_path = os.path.join("/Users/jinchuljung/Workspace/kimg/kururu_crawler/result/images", request.path.lstrip('/'))
                    if not os.path.splitext(save_path)[1]:  # Ensure the path has a file extension
                        save_path = os.path.join(save_path, "image_file")
                    save_binary_content(body, save_path)
                    body = f"{save_path}"
                elif 'video' in content_type:
                    save_path = os.path.join("/Users/jinchuljung/Workspace/kimg/kururu_crawler/result/videos", request.path.lstrip('/'))
                    if not os.path.splitext(save_path)[1]:  # Ensure the path has a file extension
                        save_path = os.path.join(save_path, "video_file")
                    save_binary_content(body, save_path)
                    body = f"{save_path}"
                
                entry["response"] = {
                    "status_code": response.status_code,
                    "headers": headers_to_dict(response.headers._headers),
                    "body": body
                }
            
            data.append(entry)
    
    return data

if __name__ == "__main__":
    target_directory = "/Users/jinchuljung/Workspace/kimg/kururu_crawler/data/.seleniumwire/storage-ccd4a7c1-a245-4b74-985a-cc0c47cf23fa"
    data = collect_request_response_data(target_directory)
    
    with open("/Users/jinchuljung/Workspace/kimg/kururu_crawler/result/collected_data.json", "w") as f:
        json.dump(data, f, default=str, indent=4)
