import csv
import datetime

text = ""

dt_now = datetime.datetime.now()
today = f"{dt_now.month}/{dt_now.day}"

with open("plan.csv", "r") as f:
    reader = csv.reader(f)
    for line in reader:
        if today == line[0]:
            if (
                dt_now + datetime.timedelta(minutes=30)
                < datetime.datetime(
                    int(dt_now.year),
                    int(dt_now.month),
                    int(dt_now.day),
                    int(line[1].split(":")[0]),
                    int(line[1].split(":")[1]),
                    0,
                )
                < dt_now + datetime.timedelta(hours=1)
            ):
                text += "次のスケジュール\n"
                text += "----------\n"
                text += f"時間：{line[0]} {line[1]}\n"
                text += f"場所：{line[2]}\n"
                text += f"{line[3]}\n"
                text += f"内容：{line[4]}\n"
                text += "----------\n"

print(text)
