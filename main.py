import tkinter as tk
import json

# 활동 추천 프로그램을 위한 메인 클래스
class ActivityRecommender:
    # 생성자: 애플리케이션 초기화
    def __init__(self, root):
        self.root = root
        self.root.title("오늘 뭐하지?")  # 창 제목 설정
        self.root.geometry("600x400")  # 창 크기 설정

        # 사용자가 선택한 태그를 저장하는 집합(set)
        self.selected_tags = set()
        
        # JSON 파일에서 태그와 활동 데이터 불러오기
        self.load_data()

        # 화면에 위젯(버튼, 목록 등) 생성
        self.create_widgets()
        
        # 초기 활동 목록 업데이트
        self.update_activity_list()

    # JSON 파일에서 데이터를 불러오는 메서드
    def load_data(self):
        try:
            # 'tags.json' 파일 열기 (UTF-8 인코딩)
            with open("tags.json", "r", encoding="utf-8") as f:
                self.all_tags = json.load(f)
            # 'activities.json' 파일 열기 (UTF-8 인코딩)
            with open("activities.json", "r", encoding="utf-8") as f:
                self.all_activities = json.load(f)
        except FileNotFoundError:
            # 파일이 없을 경우 빈 리스트로 초기화
            self.all_tags = []
            self.all_activities = []

    # GUI 위젯을 생성하고 배치하는 메서드
    def create_widgets(self):
        # 태그 버튼을 담을 프레임 생성
        tag_frame = tk.Frame(self.root, pady=10)
        tag_frame.pack(fill="x")  # 부모 위젯에 프레임 추가

        # 각 태그에 대한 버튼을 저장할 딕셔너리
        self.tag_buttons = {}
        # 모든 태그에 대해 반복하여 버튼 생성
        for tag in self.all_tags:
            # 버튼 생성 (클릭 시 toggle_tag 메서드 호출)
            btn = tk.Button(tag_frame, text=tag, relief="raised", command=lambda t=tag: self.toggle_tag(t))
            btn.pack(side="left", padx=5, pady=5)  # 프레임에 버튼 추가
            self.tag_buttons[tag] = btn  # 딕셔너리에 버튼 저장

        # 활동 목록을 보여줄 프레임 생성
        activity_frame = tk.Frame(self.root)
        activity_frame.pack(fill="both", expand=True)

        # 활동 목록을 표시할 리스트 박스 생성
        self.activity_listbox = tk.Listbox(activity_frame)
        self.activity_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    # 태그 버튼을 클릭했을 때 호출되는 메서드 (ON/OFF 토글)
    def toggle_tag(self, tag):
        # 만약 태그가 이미 선택된 상태라면
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)  # 선택된 태그 목록에서 제거
            # 버튼 스타일을 원래대로 변경 (입체 효과)
            self.tag_buttons[tag].config(relief="raised", bg="SystemButtonFace")
        # 태그가 선택되지 않은 상태라면
        else:
            self.selected_tags.add(tag)  # 선택된 태그 목록에 추가
            # 버튼 스타일을 눌린 것처럼 변경 (평면 효과 및 색상 변경)
            self.tag_buttons[tag].config(relief="sunken", bg="lightblue")
        
        # 태그 선택이 변경되었으므로 활동 목록을 업데이트
        self.update_activity_list()

    # 활동 목록을 업데이트하는 메서드
    def update_activity_list(self):
        # 리스트 박스의 모든 항목 삭제
        self.activity_listbox.delete(0, tk.END)

        # 만약 선택된 태그가 하나도 없다면
        if not self.selected_tags:
            # 모든 활동을 필터링 없이 그대로 사용
            filtered_activities = self.all_activities
        # 선택된 태그가 있다면
        else:
            # 필터링된 활동을 저장할 빈 리스트 생성
            filtered_activities = []
            # 모든 활동에 대해 반복
            for activity in self.all_activities:
                # 현재 활동의 태그 목록이 선택된 모든 태그를 포함하는지 확인 (AND 연산)
                if self.selected_tags.issubset(set(activity["tags"])):
                    # 조건을 만족하면 필터링된 목록에 추가
                    filtered_activities.append(activity)

        # 필터링된 활동 목록을 화면에 표시
        for activity in filtered_activities:
            self.activity_listbox.insert(tk.END, activity["name"])

# 이 스크립트가 직접 실행될 때만 아래 코드 블록 실행
if __name__ == "__main__":
    root = tk.Tk()  # Tkinter 루트 윈도우 생성
    app = ActivityRecommender(root)  # ActivityRecommender 클래스의 인스턴스 생성
    root.mainloop()  # GUI 이벤트 루프 시작
