import customtkinter as ctk
import json
import random
import threading
import webbrowser
import os
import http.server
import socketserver
import time

# -----------------------------
# CustomTkinter 기본 설정
# -----------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# -----------------------------
# 맵 생성 및 서버 실행 로직 (map.py 기반)
# -----------------------------

# 웹 서버의 포트 번호
PORT = 8000
# 생성될 HTML 파일 이름
OUTPUT_HTML = 'result_map.html'

def start_http_server():
    """백그라운드 스레드에서 웹 서버를 시작합니다."""
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        # 127.0.0.1 (localhost) 에서만 접근 가능하도록 설정
        with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
            print(f"로컬 서버가 시작되었습니다. (http://127.0.0.1:{PORT})")
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"오류: {PORT}번 포트가 이미 사용 중입니다. (에러 메시지: {e})")
        else:
            print(f"서버 실행 중 오류 발생: {e}")
    except Exception as e:
        print(f"서버 실행 중 알 수 없는 오류 발생: {e}")

def generate_and_serve_map(target_name):
    import json
    import webbrowser
    import os
    import sys
    import http.server
    import socketserver
    import threading
    import time

    with open('activities.json', 'r', encoding='utf-8') as f:
        all_activities = json.load(f)

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
        webbrowser.open(url=f'http://localhost:{PORT}/{output_path}')

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


# -----------------------------
# 기존 조건 선택 추천 프로그램 (renewal.py 기반)
# -----------------------------
class IntegratedRecommender(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("오늘 뭐하지? (조건 선택 Ver.)")
        self.geometry("600x750") # HTML 버튼 추가로 인해 높이 확장

        # JSON 로딩
        self.load_data()
        self.assign_ids()

        # 선택값 저장 변수
        self.place_var = None
        self.motion_var = None
        self.group_var = None
        
        # <<< 추가: 추천된 활동 이름을 저장하는 변수 >>>
        self.last_recommended_name = None

        # 결과 문자열
        self.result_str = ctk.StringVar(value="조건을 선택한 후 아래 버튼을 눌러 주세요!")

        # 화면 구성
        self.create_widgets()

    # -----------------------------
    # JSON 파일 불러오기
    # -----------------------------
    def load_data(self):
        try:
            with open("activities.json", "r", encoding="utf-8") as f:
                self.activities = json.load(f)
            print(f"✅ activities.json 로딩 성공. 총 {len(self.activities)}개 항목.")
        except Exception as e:
            print(f"❌ Error loading activities.json: {e}")
            self.activities = []

        try:
            with open("tags.json", "r", encoding="utf-8") as f:
                self.tags = json.load(f)
        except:
            self.tags = []

    # -----------------------------
    # ID 자동 생성
    # -----------------------------
    def assign_ids(self):
        for idx, act in enumerate(self.activities, start=1):
            act["id"] = idx

    # -----------------------------
    # UI 구성
    # -----------------------------
    def create_widgets(self):
        title = ctk.CTkLabel(self, text="원하는 조건을 선택하세요!", font=("Pretendard", 20, "bold"))
        title.pack(pady=15)

        # 장소 선택
        self.place_var = ctk.StringVar(value="전체")
        frame_place = ctk.CTkFrame(self, corner_radius=10)
        frame_place.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_place, text="🗺 장소 선택", font=("Pretendard", 16, "bold")).pack(pady=8)
        for txt in ["실내", "실외", "전체"]:
            ctk.CTkRadioButton(frame_place, text=txt, variable=self.place_var, value=txt).pack(anchor="w", padx=20, pady=2)

        # 활동성 선택
        self.motion_var = ctk.StringVar(value="전체")
        frame_motion = ctk.CTkFrame(self, corner_radius=10)
        frame_motion.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_motion, text="🏃 활동성 선택", font=("Pretendard", 16, "bold")).pack(pady=8)
        for txt in ["정적", "동적", "전체"]:
            ctk.CTkRadioButton(frame_motion, text=txt, variable=self.motion_var, value=txt).pack(anchor="w", padx=20, pady=2)

        # 그룹 선택
        self.group_var = ctk.StringVar(value="전체")
        frame_group = ctk.CTkFrame(self, corner_radius=10)
        frame_group.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(frame_group, text="🧑‍🤝‍🧑 그룹 선택", font=("Pretendard", 16, "bold")).pack(pady=8)
        for txt in ["혼자", "함께", "전체"]:
            ctk.CTkRadioButton(frame_group, text=txt, variable=self.group_var, value=txt).pack(anchor="w", padx=20, pady=2)

        # 추천 버튼
        btn = ctk.CTkButton(self, text="✨ 행동 추천 받기", font=("Pretendard", 16, "bold"), command=self.recommend)
        btn.pack(pady=20)

        # HTML 실행 버튼 (맵 생성 및 실행)
        html_btn = ctk.CTkButton(
            self,
            text="🌐 추천 활동 지도 열기",
            font=("Pretendard", 16, "bold"),
            fg_color="#1F6AA5",
            hover_color="#144870",
            command=self.open_map_window # 새로운 메서드 연결
        )
        html_btn.pack(pady=10)

        # 추천 결과
        result_label = ctk.CTkLabel(
            self,
            textvariable=self.result_str,
            font=("Pretendard", 18, "bold"),
            wraplength=480,
            justify="left"
        )
        result_label.pack(pady=20)

    # -----------------------------
    # 추천 기능
    # -----------------------------
    def recommend(self):
        map_dict = {
            "정적": "정적인",
            "동적": "동적인",
            "실내": "실내",
            "실외": "실외",
            "혼자": "혼자",
            "함께": "함께",
            "전체": None
        }

        required = []
        if self.place_var.get() != "전체":
            required.append("#" + map_dict[self.place_var.get()])
        if self.motion_var.get() != "전체":
            required.append("#" + map_dict[self.motion_var.get()])
        if self.group_var.get() != "전체":
            required.append("#" + map_dict[self.group_var.get()])

        filtered = []
        for act in self.activities:
            tags = set(act["tags"])
            if all(tag in tags for tag in required):
                filtered.append(act)

        if not filtered:
            self.result_str.set("❌ 조건에 맞는 활동이 없습니다.")
            self.last_recommended_name = None # 추천 활동 초기화
            return

        chosen = random.choice(filtered)
        
        # <<< 핵심 수정: 추천된 활동 이름을 클래스 변수에 저장 >>>
        self.last_recommended_name = chosen['name'] 
        
        print("--- 추천 활동 데이터 ---")
        print(chosen)
        print(f"-> 추천된 활동 이름 저장: {self.last_recommended_name}")
        print("------------------------")
        
        place_name = chosen.get('place', {}).get('name', '장소 정보가 누락되었습니다.')

        self.result_str.set(
            f"🎉 **추천 활동**\n"
            f"✔ 이름: {chosen['name']}\n"
            f"✔ **장소**: {place_name}"
        )

    # -----------------------------
    # HTML 지도 열기 기능 (map.py 기능 호출)
    # -----------------------------
    def open_map_window(self):
        """저장된 추천 활동 이름으로 지도 생성 및 실행 함수를 호출합니다."""
        
        if not self.last_recommended_name:
            self.result_str.set("❌ 먼저 '✨ 행동 추천 받기' 버튼을 눌러 활동을 추천 받아야 합니다.")
            print("❌ 지도 열기 실패: 추천 활동 이름이 저장되지 않았습니다.")
            return

        print(f"▶️ 지도 열기 요청: 추천 활동 이름 '{self.last_recommended_name}'")
        
        # 저장된 추천 활동 이름을 인자로 전달하며 지도 생성 및 서버 실행 함수 호출
        generate_and_serve_map(self.last_recommended_name)

# ---------------------------------------
# 실행부
# ---------------------------------------
if __name__ == "__main__":
    app_ctk = IntegratedRecommender()
    app_ctk.mainloop()
