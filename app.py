from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import csv
import datetime

app = Flask(__name__)

# line_bot_api = LineBotApi(os.getenv("ACCESS_TOKEN"))
# handler = WebhookHandler(os.getenv("SECRET"))

ACCESS_TOKEN = "38Be5uBTrlqnY9d+CQToiVTEPCXHQFt7kUJJElJRtxibM/IESXmxOdrPsjo4Zyc6XVaeJ/s9OmbjoxEnrd/lIOfJohrq47bUNlr24sT1cg+G6R9CnUgEIShMz/PIW/5urANQQO8ShTwc4FvJgPzQnwdB04t89/1O/w1cDnyilFU="
SECRET = "b318448d3c466a165e919d60399bc41a"

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)



@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


@app.route("/sendSchedule", methods=["POST"])
def sendSchedule():
    text = "通知テスト"
    dt_now = datetime.datetime.now()
    today = f"{dt_now.month}/{dt_now.day}"

    with open("plan.csv", "r") as f:
        reader = csv.reader(f)
        for line in reader:
            if today == line[0]:
                if (
                    dt_now + datetime.timedelta(minutes=30)
                    <= datetime.datetime(
                        int(dt_now.year),
                        int(dt_now.month),
                        int(dt_now.day),
                        int(line[1].split(":")[0]),
                        int(line[1].split(":")[1]),
                        0,
                    )
                    <= dt_now + datetime.timedelta(hours=1)
                ):
                    text += "次のスケジュール\n"
                    text += "----------\n"
                    text += f"時間：{line[0]} {line[1]}\n"
                    text += f"場所：{line[2]}\n"
                    text += f"{line[3]}\n"
                    text += f"内容：{line[4]}\n"
                    text += "----------"
    print(text)
    try:
        line_bot_api.broadcast(messages=TextSendMessage(text=text))
    except InvalidSignatureError:
        abort(400)


if __name__ == "__main__":
    app.run()
