import linebot, openai, os, json
from linebot.models import MessageEvent, TextMessage, TextSendMessage

def lambda_handler(event, context):
    # メッセージを受信
    decoded_body = json.loads(event['body'])
    reply_token = decoded_body['events'][0]['replyToken']
    message= decoded_body['events'][0]['message']['text']

    # 返信メッセージを作成
    r_message = chat_completion(message)

    # メッセージの返信
    LINBOT_TOKEN = os.environ["LINE_BOT_TOKEN"]
    LINBOT_SECRET= os.environ["LINE_BOT_SECRET"]
    line_bot_api = linebot.LineBotApi(LINBOT_TOKEN)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=r_message))

    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}

# ChatGPTのAPIを呼び出す
def chat_completion(message):
    prompt = '''以下に目的地を記載します。おすすめの観光スポットを一つ教えてください。ただしドラゴンボールの孫悟空風でお願いします。一人称はオラ。孫悟空という単語は出さないで下さい。\n'''
    prompt += message

    # APIキーを環境変数から設定
    openai.api_key = os.environ["OPENAI_API_KEY"]    

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{'role': 'user', 'content' :prompt}]
    )
    # 応答からのChatGPTの返答を取り出して返す
    return response.choices[0]['message']['content']