import customtkinter as ctk
import json

# 기본 테마 설정 (시스템에 따라 라이트/다크 모드 자동 적용)
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  # 기본 색상 테마 (blue, dark-blue, green 등)

class ActivityRecommender(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. 기본 창 설정
        self.title("오늘 뭐하지? (CustomTkinter Ver.)")
        self.geometry("600x500")
        
        # 데이터 로드
        self.selected_tags = set()
        self.btn_objects = {} # 버튼 객체 저장용
        self.load_data()
        
        # 2. 화면 구성 (위젯 배치)
        self.create_widgets()
        self.update_activity_list()

    def load_data(self):
        try:
            with open("tags.json", "r", encoding="utf-8") as f:
                self.all_tags = json.load(f)
            with open("activities.json", "r", encoding="utf-8") as f:
                self.all_activities = json.load(f)
        except FileNotFoundError:
            self.all_tags = []
            self.all_activities = []

    def create_widgets(self):
        # [제목]
        title_lbl = ctk.CTkLabel(self, text="어떤 활동을 원하세요?", font=("Pretendard", 20, "bold"))
        title_lbl.pack(pady=20)

        # [태그 버튼 영역] - 스크롤 가능한 프레임 사용 (태그가 많아질 경우 대비)
        self.tag_frame = ctk.CTkScrollableFrame(self, height=60, orientation="horizontal", fg_color="transparent")
        self.tag_frame.pack(fill="x", padx=20)

        # [태그 버튼 생성]
        for tag in self.all_tags:
            btn = ctk.CTkButton(
                self.tag_frame, 
                text=tag, 
                command=lambda t=tag: self.toggle_tag(t),
                fg_color="gray",       # 기본 색상 (꺼짐)
                hover_color="#555555", # 마우스 올렸을 때 색상
                width=80,
                corner_radius=15       # 모서리 둥글게 (이미지 없이 가능!)
            )
            btn.pack(side="left", padx=5)
            self.btn_objects[tag] = btn

        # [구분선]
        line = ctk.CTkFrame(self, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", padx=20, pady=15)

        # [결과 리스트 영역] - 스크롤 가능한 프레임
        self.result_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def toggle_tag(self, tag):
        # 상태 변경 로직
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
            # 버튼 색상 원래대로 (회색)
            self.btn_objects[tag].configure(fg_color="gray")
        else:
            self.selected_tags.add(tag)
            # 버튼 색상 강조 (파란색 - 테마 기본색)
            self.btn_objects[tag].configure(fg_color=["#3B8ED0", "#1F6AA5"]) 
        
        self.update_activity_list()

    def update_activity_list(self):
        # 기존 목록 지우기 (result_frame 내부 위젯 모두 삭제)
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # 필터링 로직
        if not self.selected_tags:
            filtered = self.all_activities
        else:
            filtered = [act for act in self.all_activities if self.selected_tags.issubset(set(act["tags"]))]

        # 목록 표시 (Label이 아니라 둥근 카드로 예쁘게 표시)
        for act in filtered:
            card = ctk.CTkFrame(self.result_frame, corner_radius=10, fg_color=("white", "#2B2B2B")) # 라이트/다크 모드별 색상
            card.pack(fill="x", pady=5)
            
            # 활동 이름
            lbl_name = ctk.CTkLabel(card, text=act["name"], font=("Pretendard", 14, "bold"), anchor="w")
            lbl_name.pack(side="left", padx=15, pady=10)
            
            # 태그 표시 (작게 옆에 보여주기)
            tags_str = " ".join(act["tags"])
            lbl_tags = ctk.CTkLabel(card, text=tags_str, font=("Arial", 10), text_color="gray", anchor="e")
            lbl_tags.pack(side="right", padx=15)

if __name__ == "__main__":
    app = ActivityRecommender()
    app.mainloop()