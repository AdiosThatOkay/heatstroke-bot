from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextMessage, TextSendMessage, LocationMessage, TemplateSendMessage,
    ConfirmTemplate, MessageEvent, PostbackEvent, FollowEvent, UnfollowEvent,
    PostbackAction
)
from hsbot import (
    app, db
)
from hsbot.models.users import User
from hsbot.models.observatories import Observatory
from hsbot.utils.message_builder import MessageBuilder
from hsbot.utils.utils import (
    get_nearest_observatory, postback_data_to_dict
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
    user_id = event.source.user_id
    if event.message.text in ['いま', '今', 'now', 'きょう', '今日', 'today']:
        builder = MessageBuilder.get_message_builder(user_id)
        msg = builder.build_message_today()
    elif event.message.text in ['あした', 'あす', '明日', 'tomorrow']:
        builder = MessageBuilder.get_message_builder(user_id)
        msg = builder.build_message_later_date(1)
    elif event.message.text in ['あさって', '明後日', 'day after tomorrow']:
        builder = MessageBuilder.get_message_builder(user_id)
        msg = builder.build_message_later_date(2)
    else:
        msg = MessageBuilder.get_default_message()

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    user_id = event.source.user_id
    user = db.session.query(User).filter(User.user_id == user_id).first()
    registered_observatory = db.session.query(Observatory).filter(
        Observatory.code == user.nearest_observatory).first()

    user_lat = event.message.latitude
    user_lon = event.message.longitude
    nearest_observatory = get_nearest_observatory(user_lat, user_lon)

    msg_text = f"現在登録している観測地点:\n  {registered_observatory}\n"
    msg_text += f"最寄りの観測地点:\n  {nearest_observatory}\nに変更しますか？"

    messages = TemplateSendMessage(
        alt_text='位置情報を送信しました',
        template=ConfirmTemplate(
            text=msg_text,
            actions=[
                PostbackAction(
                    label='はい',
                    data=f'change=1&code={nearest_observatory.code}'),
                PostbackAction(
                    label='いいえ',
                    data='change=0')]))

    line_bot_api.reply_message(event.reply_token, messages)
    app.logger.info(f"{user} send location [{user_lat}, {user_lon}]")


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    user = db.session.query(User).filter(User.user_id == user_id).first()
    postback_data = postback_data_to_dict(event.postback.data)
    if postback_data['change']:
        user.nearest_observatory = postback_data['code']
        db.session.commit()
        msg = "観測地点を変更しました。"
    else:
        msg = "観測地点の変更を中止しました。"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
    app.logger.info(f"{user} send {postback_data}")


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
