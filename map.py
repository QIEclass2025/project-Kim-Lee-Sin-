import json
import webbrowser
import os
import sys
import http.server
import socketserver
import threading
import time

# 1. JSON 데이터 파일 읽기

with open('activities.json', 'r', encoding='utf-8') as f:
    all_activities = json.load(f)

target_name = "수원 화성 행궁동 카페거리 가기"
recommended_list = []

for item in all_activities:
    if item.get('name') == target_name:
        recommended_list.append(item)

with open('map_template.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

json_str = json.dumps(recommended_list, ensure_ascii=False)
final_html = html_content.replace('/* PYTHON_DATA_HERE */', json_str)

output_path = 'result_map.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

PORT = 8000

def open_browser():
    webbrowser.open(url = f'http://localhost:{PORT}/{output_path}')

threading.Thread(target=open_browser).start()

print(f"로컬서버가 시작되었습니다. (http://localhost:{PORT})")

Handler = http.server.SimpleHTTPRequestHandler
try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except OSError:
    print(f"오류: {PORT}번 포트가 이미 사용 중입니다. 실행 중인 다른 서버를 끄거나 포트를 변경하세요.")
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
