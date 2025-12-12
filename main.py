import customtkinter as ctk
import json

# ==========================================
# 1. 기본 설정 및 테마 적용
# ==========================================
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

class ActivityRecommender(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --------------------------------------
        # 2. 메인 윈도우(창) 설정
        # --------------------------------------
        self.title("오늘 뭐하지? (CustomTkinter Ver.)")
        self.geometry("600x500")
        
        # --------------------------------------
        # 3. 데이터 및 변수 초기화
        # --------------------------------------
        self.selected_tags = set()
        self.btn_objects = {}
        
        self.load_data()
        
        # --------------------------------------
        # 4. 화면 구성 (위젯 배치)
        # --------------------------------------
        self.create_widgets()
        self.update_activity_list()

    def load_data(self):
        """JSON 파일에서 태그와 활동 데이터를 불러오는 함수"""
        try:
            with open("tags.json", "r", encoding="utf-8") as f:
                self.all_tags = json.load(f)
            with open("activities.json", "r", encoding="utf-8") as f:
                self.all_activities = json.load(f)
        except FileNotFoundError:
            self.all_tags = []
            self.all_activities = []

    def create_widgets(self):
        """화면에 보여질 버튼, 라벨, 리스트 등을 생성하는 함수"""
        
        # [제목 라벨]
        title_lbl = ctk.CTkLabel(self, text="어떤 활동을 원하세요?", font=("Pretendard", 20, "bold"))
        title_lbl.pack(pady=20)

        # [태그 버튼 영역]
        self.tag_frame = ctk.CTkScrollableFrame(self, height=60, orientation="horizontal", fg_color="transparent")
        self.tag_frame.pack(fill="x", padx=20)

        # [태그 버튼 생성]
        for tag in self.all_tags:
            btn = ctk.CTkButton(
                self.tag_frame, 
                text=tag, 
                command=lambda t=tag: self.toggle_tag(t),
                fg_color="gray",       # 기본: 회색
                hover_color="#555555", # 호버: 진한 회색
                width=80,
                corner_radius=15
            )
            btn.pack(side="left", padx=5)
            self.btn_objects[tag] = btn

        # [구분선]
        line = ctk.CTkFrame(self, height=2, fg_color="#E0E0E0")
        line.pack(fill="x", padx=20, pady=15)

        # [결과 리스트 영역]
        self.result_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def toggle_tag(self, tag):
        """태그 버튼 클릭 시 상태 변경 (ON/OFF 및 색상 변경)"""
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
            self.btn_objects[tag].configure(fg_color="gray", hover_color="#555555")
        else:
            self.selected_tags.add(tag)
            self.btn_objects[tag].configure(fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"])
        
        self.update_activity_list()

    def update_activity_list(self):
        """활동 목록 필터링 및 화면 표시 (장소 정보 추가됨)"""
        
        # 1. 초기화
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # 2. 필터링
        if not self.selected_tags:
            filtered = self.all_activities
        else:
            filtered = [act for act in self.all_activities if self.selected_tags.issubset(set(act["tags"]))]

        # 3. 화면 그리기
        for act in filtered:
            # 카드 배경
            card = ctk.CTkFrame(self.result_frame, corner_radius=10, fg_color=("white", "#2B2B2B"))
            card.pack(fill="x", pady=5)
            
            # [1] 활동 이름 (왼쪽 정렬)
            lbl_name = ctk.CTkLabel(card, text=act["name"], font=("Pretendard", 14, "bold"), anchor="w")
            lbl_name.pack(side="left", padx=(15, 5), pady=10)
            
            # [2] 태그 (맨 오른쪽 정렬)
            tags_str = " ".join(act["tags"])
            lbl_tags = ctk.CTkLabel(card, text=tags_str, font=("Arial", 10), text_color="gray", anchor="e")
            lbl_tags.pack(side="right", padx=15)

            # [3] 장소 이름 (이름 바로 오른쪽에 작게 표시)
            # 데이터에 'place' 정보가 있는지 확인 (안전장치)
            if "place" in act and "name" in act["place"]:
                place_name = f"📍 {act['place']['name']}" # 앞에 핀 아이콘 추가해서 예쁘게
                lbl_place = ctk.CTkLabel(
                    card, 
                    text=place_name, 
                    font=("Pretendard", 11),  # 작고
                    text_color=("gray60", "gray70"), # 연한 회색 (라이트/다크)
                    anchor="w"
                )
                lbl_place.pack(side="left", padx=0, pady=10) # 이름 바로 옆에 붙음

if __name__ == "__main__":
    app = ActivityRecommender()
    app.mainloop()