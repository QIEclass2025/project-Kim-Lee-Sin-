import tkinter as tk
import json

class ActivityRecommender:
    def __init__(self, root):
        self.root = root
        self.root.title("오늘 뭐하지?")
        self.root.geometry("600x400")

        self.selected_tags = set()
        self.load_data()

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
        # 태그 프레임
        tag_frame = tk.Frame(self.root, pady=10)
        tag_frame.pack(fill="x")

        self.tag_buttons = {}
        for tag in self.all_tags:
            btn = tk.Button(tag_frame, text=tag, relief="raised", command=lambda t=tag: self.toggle_tag(t))
            btn.pack(side="left", padx=5, pady=5)
            self.tag_buttons[tag] = btn

        # 활동 목록 프레임
        activity_frame = tk.Frame(self.root)
        activity_frame.pack(fill="both", expand=True)

        self.activity_listbox = tk.Listbox(activity_frame)
        self.activity_listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_tag(self, tag):
        if tag in self.selected_tags:
            self.selected_tags.remove(tag)
            self.tag_buttons[tag].config(relief="raised", bg="SystemButtonFace")
        else:
            self.selected_tags.add(tag)
            self.tag_buttons[tag].config(relief="sunken", bg="lightblue")
        
        self.update_activity_list()

    def update_activity_list(self):
        self.activity_listbox.delete(0, tk.END)

        if not self.selected_tags:
            filtered_activities = self.all_activities
        else:
            filtered_activities = []
            for activity in self.all_activities:
                if self.selected_tags.issubset(set(activity["tags"])):
                    filtered_activities.append(activity)

        for activity in filtered_activities:
            self.activity_listbox.insert(tk.END, activity["name"])

if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityRecommender(root)
    root.mainloop()
