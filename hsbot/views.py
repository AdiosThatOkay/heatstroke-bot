from datetime import datetime
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent
)
from hsbot import (
    app, db
)
from hsbot.models.users import User
from hsbot.utils.message_builder import MessageBuilder
from hsbot.utils.wbgt_api import (
    get_jikkyou, get_yohou
)

line_bot_api = LineBotApi(app.config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['LINE_CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text in ['いま', '今', 'now', 'きょう', '今日', 'today']:
        builder = get_message_builder(event)
        msg = builder.build_message_today()
    elif event.message.text in ['あした', 'あす', '明日', 'tomorrow']:
        builder = get_message_builder(event)
        msg = builder.build_message_later_date(1)
    elif event.message.text in ['あさって', '明後日', 'day after tomorrow']:
        builder = get_message_builder(event)
        msg = builder.build_message_later_date(2)
    else:
        msg = MessageBuilder.DEFAULT_MESSAGE

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id

    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name

    user = User(user_id, user_name)
    db.session.add(user)
    app.logger.info(f"followed by: {user}")
    db.session.commit()


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    user = db.session.query(User).filter(User.user_id == user_id).first()
    db.session.delete(user)
    app.logger.info(f"unfollowed by: {user}")
    db.session.commit()


@app.route('/')
def hello():
    return "This is Test."


def get_message_builder(event):
    user_id = event.source.user_id
    user = db.session.query(User).filter(User.user_id == user_id).first()
    observatory_code = user.nearest_observatory
    now_ym = datetime.now().strftime('%Y%m')
    now_wbgt = get_jikkyou(observatory_code, now_ym)
    yohou_wbgt = get_yohou(observatory_code)
    return MessageBuilder(now_wbgt, yohou_wbgt)
