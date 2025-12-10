import customtkinter as ctk
import json

# ==========================================
# 1. 기본 설정 및 테마 적용
# ==========================================
# 시스템 설정에 따라 라이트/다크 모드 자동 적용 ("System", "Dark", "Light")
ctk.set_appearance_mode("System")  
# 위젯의 기본 색상 테마 설정 ("blue", "green", "dark-blue")
ctk.set_default_color_theme("blue")  

class ActivityRecommender(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --------------------------------------
        # 2. 메인 윈도우(창) 설정
        # --------------------------------------
        self.title("오늘 뭐하지? (CustomTkinter Ver.)") # 창 제목
        self.geometry("600x500") # 창 크기 (가로x세로)
        
        # --------------------------------------
        # 3. 데이터 및 변수 초기화
        # --------------------------------------
        self.selected_tags = set() # 사용자가 선택한 태그들을 담을 집합(Set)
        self.btn_objects = {}      # 생성된 버튼 객체들을 저장할 딕셔너리 (나중에 색상 변경용)
        
        # JSON 파일에서 데이터 불러오기
        self.load_data()
        
        # --------------------------------------
        # 4. 화면 구성 (위젯 배치)
        # --------------------------------------
        self.create_widgets()
        
        # 프로그램 시작 시 전체 리스트 한 번 출력
        self.update_activity_list()

    def load_data(self):
        """JSON 파일에서 태그와 활동 데이터를 불러오는 함수"""
        try:
            # 태그 목록 불러오기
            with open("tags.json", "r", encoding="utf-8") as f:
                self.all_tags = json.load(f)
            # 활동 목록 불러오기
            with open("activities.json", "r", encoding="utf-8") as f:
                self.all_activities = json.load(f)
        except FileNotFoundError:
            # 파일이 없을 경우 빈 리스트로 초기화하여 에러 방지
            self.all_tags = []
            self.all_activities = []

    def create_widgets(self):
        """화면에 보여질 버튼, 라벨, 리스트 등을 생성하는 함수"""
        
        # [제목 라벨]
        title_lbl = ctk.CTkLabel(self, text="어떤 활동을 원하세요?", font=("Pretendard", 20, "bold"))
        title_lbl.pack(pady=20) # 상하 여백 20

        # [태그 버튼 영역] - 태그가 많아질 수 있으므로 스크롤 가능한 프레임 사용
        self.tag_frame = ctk.CTkScrollableFrame(self, height=60, orientation="horizontal", fg_color="transparent")
        self.tag_frame.pack(fill="x", padx=20) # 가로로 꽉 채우기

        # [태그 버튼 생성 반복문]
        for tag in self.all_tags:
            btn = ctk.CTkButton(
                self.tag_frame, 
                text=tag, 
                command=lambda t=tag: self.toggle_tag(t), # 클릭 시 실행할 함수 연결
                
                # === [수정됨] 초기 상태 (OFF) 설정 ===
                fg_color="gray",       # 1. 기본 배경색 (회색)
                hover_color="#555555", # 2. 마우스 올렸을 때 색상 (진한 회색)
                # ===================================
                
                width=80,              # 버튼 너비
                corner_radius=15       # 모서리 둥글기 (이미지 없이 둥근 버튼 구현)
            )
            btn.pack(side="left", padx=5) # 왼쪽부터 차례대로 쌓기
            self.btn_objects[tag] = btn   # 나중에 제어하기 위해 딕셔너리에 저장

        # [구분선] - 디자인 요소
        line = ctk.CTkFrame(self, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", padx=20, pady=15)

        # [결과 리스트 영역] - 스크롤 가능한 프레임
        self.result_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def toggle_tag(self, tag):
        """태그 버튼을 클릭했을 때 실행되는 로직 (ON/OFF 토글 및 색상 변경)"""
        
        # === [수정됨] 상태별 색상 상세 분기 ===
        if tag in self.selected_tags:
            # [CASE 1: 켜져 있던 걸 끄는 경우 (ON -> OFF)]
            self.selected_tags.remove(tag)
            
            # 버튼 색상을 '비활성화 스타일'로 변경
            self.btn_objects[tag].configure(
                fg_color="gray",       # 배경: 회색
                hover_color="#555555"  # 호버: 진한 회색 (OFF 상태임을 명확히 함)
            )
            
        else:
            # [CASE 2: 꺼져 있던 걸 켜는 경우 (OFF -> ON)]
            self.selected_tags.add(tag)
            
            # 버튼 색상을 '활성화 스타일'로 변경
            self.btn_objects[tag].configure(
                fg_color=["#3B8ED0", "#1F6AA5"],   # 배경: 파란색 (라이트모드, 다크모드)
                hover_color=["#36719F", "#144870"] # 호버: 더 진한 파란색 (ON 상태임을 명확히 함)
            )
        # =====================================
        
        # 태그 선택 상태가 변했으니 리스트 새로고침
        self.update_activity_list()

    def update_activity_list(self):
        """현재 선택된 태그에 맞춰 활동 목록을 필터링하고 화면에 표시하는 함수"""
        
        # 1. 기존에 표시된 목록 싹 지우기 (초기화)
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # 2. 필터링 로직
        if not self.selected_tags:
            # 선택된 태그가 없으면 전체 목록 보여주기
            filtered = self.all_activities
        else:
            # 선택된 태그가 있다면, 해당 태그들을 '모두' 포함하는 활동만 교집합으로 추출
            filtered = [act for act in self.all_activities if self.selected_tags.issubset(set(act["tags"]))]

        # 3. 화면에 카드 형태로 그리기
        for act in filtered:
            # 카드 배경 (둥근 사각형 프레임)
            card = ctk.CTkFrame(self.result_frame, corner_radius=10, fg_color=("white", "#2B2B2B"))
            card.pack(fill="x", pady=5)
            
            # 활동 이름 텍스트
            lbl_name = ctk.CTkLabel(card, text=act["name"], font=("Pretendard", 14, "bold"), anchor="w")
            lbl_name.pack(side="left", padx=15, pady=10)
            
            # 우측 태그 텍스트 (작게 표시)
            tags_str = " ".join(act["tags"])
            lbl_tags = ctk.CTkLabel(card, text=tags_str, font=("Arial", 10), text_color="gray", anchor="e")
            lbl_tags.pack(side="right", padx=15)

if __name__ == "__main__":
    app = ActivityRecommender()
    app.mainloop()