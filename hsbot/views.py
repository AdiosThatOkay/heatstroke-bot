from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    TextMessage, TextSendMessage, LocationMessage,
    MessageEvent, PostbackEvent, FollowEvent, UnfollowEvent,
    PostbackAction, QuickReply, QuickReplyButton
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
from hsbot.utils.wbgt_api import (
    get_jikkyou, get_yohou
)
import datetime

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
    user = db.session.query(User).filter(User.user_id == user_id).first()
    observatory_code = user.nearest_observatory
    ym = datetime.datetime.now().strftime('%Y%m')
    now_wbgt = get_jikkyou(observatory_code, ym)
    yohou_wbgt = get_yohou(observatory_code)
    message_builder = MessageBuilder(now_wbgt, yohou_wbgt)

    if event.message.text in ['いま', '今', 'now', 'きょう', '今日', 'today']:
        msg = message_builder.build_message_today()
    elif event.message.text in ['あした', 'あす', '明日', 'tomorrow']:
        msg = message_builder.build_message_later_date(1)
    elif event.message.text in ['あさって', '明後日', 'day after tomorrow']:
        msg = message_builder.build_message_later_date(2)
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

    messages = TextSendMessage(
                   text=msg_text,
                   quick_reply=QuickReply(items=[
                       QuickReplyButton(action=PostbackAction(
                           label='はい',
                           data=f'change=1&code={nearest_observatory.code}')),
                       QuickReplyButton(action=PostbackAction(
                           label='いいえ',
                           data='change=0'))]))

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
    app.logger.info(f"{user} send data: {event.postback.data}")


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
    return "OK"


@app.route('/check')
def check():
    if request.remote_addr == "127.0.0.1":
        result_cache = {}
        all_users = db.session.query(User).all()
        for user in all_users:
            if user.notified is True:
                continue
            wbgt = result_cache.get(
                    user.nearest_observatory,
                    get_jikkyou(user.nearest_observatory,
                                datetime.datetime.strftime('%Y%m')))
            result_cache.setdefault(user.nearest_observatory, wbgt)
            if wbgt.risk() == '危険':
                msg = MessageBuilder.get_warning_message(wbgt)
                line_bot_api.push_message(user.user_id, messages=msg)
            user.notified = True
        db.session.commit()
    else:
        return abort(403)
    return "OK"


@app.route('/morning')
def morning():
    if request.remote_addr == "127.0.0.1":
        builder_cache = {}
        all_users = db.session.query(User).all()
        for user in all_users:
            user.notified is False
            message_builder = builder_cache.get(
                    user.nearest_observatory,
                    MessageBuilder(get_jikkyou(user.nearest_observatory,
                                               datetime.datetime.strftime('%Y%m')),
                                   get_yohou(user.nearest_observatory)))
            builder_cache.setdefault(user.nearest_observatory, message_builder)
            msg = message_builder.build_message_today()
            line_bot_api.push_message(user.user_id, messages=msg)
            if message_builder.now_wbgt.risk() == '危険':
                user.notified = True
        db.session.commit()
    else:
        return abort(403)
    return "OK"
