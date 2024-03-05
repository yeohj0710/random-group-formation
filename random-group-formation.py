import tkinter as tk
from tkinter import messagebox
import secrets
import os
import sys


def secure_shuffle(data):
    shuffled_data = data[:]
    secrets.SystemRandom().shuffle(shuffled_data)
    return shuffled_data


def make_teams(two_members, one_members):
    shuffled_two_members = secure_shuffle(two_members)
    num_teams = len(shuffled_two_members) // 2
    teams = [
        shuffled_two_members[i : i + 2] for i in range(0, len(shuffled_two_members), 2)
    ]

    for one_member in one_members:
        teams.append([one_member])

    return teams


def display_results(result_text):
    result_window = tk.Tk()
    result_window.minsize(width=500, height=100)
    result_window.title("조 구성 결과")

    result_label = tk.Label(result_window, text=result_text, font=("Helvetica", 12))
    result_label.pack()

    close_button = tk.Button(result_window, text="닫기", command=result_window.destroy)
    close_button.pack()

    result_window.mainloop()


def get_input():
    window = tk.Tk()
    window.title("의약통계학 텀페이퍼 조 구성")

    window.minsize(width=500, height=300)

    tk.Label(
        window,
        text="2인 1조를 희망하는 사람들의 이름을 한 줄에 한 명씩 입력해 주세요.",
        font=("Helvetica", 12),
    ).pack()
    two_member_entry = tk.Text(window, height=10, width=20, font=(10))
    two_member_entry.pack()

    tk.Label(
        window,
        text="1인 1조를 희망하는 사람들의 이름을 한 줄에 한 명씩 입력해 주세요.",
        font=("Helvetica", 12),
    ).pack()
    one_member_entry = tk.Text(window, height=10, width=20, font=(10))
    one_member_entry.pack()

    def on_submit():
        two_members = [
            name.strip()
            for name in two_member_entry.get("1.0", "end-1c").split("\n")
            if name.strip()
        ]
        one_members = [
            name.strip()
            for name in one_member_entry.get("1.0", "end-1c").split("\n")
            if name.strip()
        ]

        teams = make_teams(two_members, one_members)

        all_members = [member for team in teams for member in team]
        duplicate_members = [
            member for member in all_members if all_members.count(member) > 1
        ]

        if duplicate_members:
            messagebox.showwarning(
                "주의", f"중복된 이름이 있습니다: {', '.join(duplicate_members)}"
            )

        result = "[조 구성 결과]\n"
        for i, team in enumerate(teams, start=1):
            result += f"{i}조: {', '.join(team)}\n"

        # 실행 파일로 패키징되었는지 확인
        if getattr(sys, "frozen", False):
            # 실행 파일로 패키징되었다면 실행 파일이 있는 경로 선택
            current_dir = os.path.dirname(sys.executable)
        else:
            # 실행 파일로 패키징되지 않았다면 스크립트가 있는 경로 선택
            current_dir = os.path.abspath(os.path.dirname(__file__))

        file_path = os.path.join(current_dir, "조 구성 결과.txt")

        with open(file_path, "w+") as file:
            file.write(result)

        result += "\n결과가 현재 폴더에 '조 구성 결과.txt'로 저장되었습니다."

        display_results(result)

        window.destroy()

    submit_button = tk.Button(window, text="조 구성하기", command=on_submit)
    submit_button.pack()

    window.mainloop()


if __name__ == "__main__":
    get_input()
