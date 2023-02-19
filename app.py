from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run()
