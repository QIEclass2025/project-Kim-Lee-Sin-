import customtkinter as ctk
import json
import random
import threading
import webview
from flask import Flask, send_from_directory, render_template_string
import os

# -----------------------------
# CustomTkinter 기본 설정
# -----------------------------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# -----------------------------
# Flask + WebView 설정
# -----------------------------
app = Flask(__name__, static_folder='.')
HTML_FILE = "index.html"   # 실행할 HTML 파일 이름 (필요하면 바꾸면 됨)


@app.route('/')
def index():
    if os.path.exists(HTML_FILE):
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html = f.read()
        return render_template_string(html)
    else:
        return "<h1>HTML 파일(index.html) 을 찾을 수 없습니다.</h1>"


@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)


def start_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)


def open_html_window():
    """HTML 파일을 WebView 창으로 띄움"""
    threading.Thread(target=start_flask, daemon=True).start()

    webview.create_window(
        title="HTML 실행 (Kakao Map 등)",
        url="http://127.0.0.1:5000",
        width=900,
        height=900
    )
    webview.start()


# -----------------------------
# 기존 조건 선택 추천 프로그램
# -----------------------------
class IntegratedRecommender(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("오늘 뭐하지? (조건 선택 Ver.)")
        self.geometry("600x720")

        # JSON 로딩
        self.load_data()
        self.assign_ids()

        # 선택값 저장 변수
        self.place_var = None
        self.motion_var = None
        self.group_var = None

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
        except:
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

        # ========================================================
        # 장소 선택
        # ========================================================
        self.place_var = ctk.StringVar(value="전체")
        frame_place = ctk.CTkFrame(self, corner_radius=10)
        frame_place.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_place, text="🗺 장소 선택", font=("Pretendard", 16, "bold")).pack(pady=8)

        for txt in ["실내", "실외", "전체"]:
            ctk.CTkRadioButton(frame_place, text=txt, variable=self.place_var, value=txt).pack(anchor="w", padx=20, pady=2)

        # ========================================================
        # 활동성 선택
        # ========================================================
        self.motion_var = ctk.StringVar(value="전체")
        frame_motion = ctk.CTkFrame(self, corner_radius=10)
        frame_motion.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_motion, text="🏃 활동성 선택", font=("Pretendard", 16, "bold")).pack(pady=8)

        for txt in ["정적", "동적", "전체"]:
            ctk.CTkRadioButton(frame_motion, text=txt, variable=self.motion_var, value=txt).pack(anchor="w", padx=20, pady=2)

        # ========================================================
        # 그룹 선택
        # ========================================================
        self.group_var = ctk.StringVar(value="전체")
        frame_group = ctk.CTkFrame(self, corner_radius=10)
        frame_group.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_group, text="🧑‍🤝‍🧑 그룹 선택", font=("Pretendard", 16, "bold")).pack(pady=8)

        for txt in ["혼자", "함께", "전체"]:
            ctk.CTkRadioButton(frame_group, text=txt, variable=self.group_var, value=txt).pack(anchor="w", padx=20, pady=2)

        # ========================================================
        # 추천 버튼
        # ========================================================
        btn = ctk.CTkButton(self, text="✨ 행동 추천 받기", font=("Pretendard", 16, "bold"), command=self.recommend)
        btn.pack(pady=20)

        # ========================================================
        # HTML 실행 버튼 (새로 추가됨)
        # ========================================================
        html_btn = ctk.CTkButton(
            self,
            text="🌐 HTML 지도 열기",
            font=("Pretendard", 16, "bold"),
            fg_color="#1F6AA5",
            hover_color="#144870",
            command=open_html_window
        )
        html_btn.pack(pady=10)

        # ========================================================
        # 추천 결과
        # ========================================================
        result_label = ctk.CTkLabel(
            self,
            textvariable=self.result_str,
            font=("Pretendard", 14),
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
            return

        chosen = random.choice(filtered)

        self.result_str.set(
            f"🎉 **추천 활동**\n"
            f"✔ 이름: {chosen['name']}\n"
            f"✔ ID: {chosen['id']}"
        )


# ---------------------------------------
# 실행부
# ---------------------------------------
if __name__ == "__main__":
    app_ctk = IntegratedRecommender()
    app_ctk.mainloop()
