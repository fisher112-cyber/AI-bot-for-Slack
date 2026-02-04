import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai import OpenAI

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
NEWS_CHANNEL = os.getenv("NEWS_CHANNEL")
ESCALATION_CHANNEL = os.getenv("ESCALATION_CHANNEL")

app = App(token=SLACK_BOT_TOKEN)
handler = SocketModeHandler(app, SLACK_APP_TOKEN)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Ты — корпоративный инфо-бот компании.
Твои задачи:
1) Публикуешь новости (/newsbot).
2) Отвечаешь сотрудникам в DM.
3) Эскалируешь запросы при низкой уверенности.
Пиши кратко, официально и по делу.
"""


def gpt_answer(text: str) -> str:
    r = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ]
    )
    return r.choices[0].message.content


@app.command("/newsbot")
def newsbot(ack, respond, command):
    ack()
    draft = command["text"]
    final_msg = gpt_answer(f"Сформируй корпоративную новость: {draft}")
    app.client.chat_postMessage(channel=NEWS_CHANNEL, text=final_msg)
    respond(f"Новость опубликована → {NEWS_CHANNEL}")


@app.event("message")
def direct_message(event, say):
    if event.get("channel_type") != "im":
        return

    text = event.get("text", "")
    user = event.get("user")

    ai = gpt_answer(text)

    if ai.startswith("ESCALATE:"):
        reason = ai.replace("ESCALATE:", "").strip()
        app.client.chat_postMessage(
            channel=ESCALATION_CHANNEL,
            text=(
                f"🚨 *Эскалация запроса*\n"
                f"От: <@{user}>\n"
                f"*Причина:* {reason}\n"
                f"*Запрос:* ```{text}```"
            )
        )
        say("Ваш запрос передан ИТ.")
    else:
        say(ai)


@app.event("app_mention")
def mention(event, say):
    user = event.get("user")
    text = event.get("text", "")

    ai = gpt_answer(text)

    if ai.startswith("ESCALATE:"):
        reason = ai.replace("ESCALATE:", "").strip()
        app.client.chat_postMessage(
            channel=ESCALATION_CHANNEL,
            text=(
                f"🚨 *Эскалация из канала*\n"
                f"От: <@{user}>\n"
                f"*Причина:* {reason}\n"
                f"*Сообщение:* ```{text}```"
            )
        )
        say("Запрос эскалирован в ИТ.")
    else:
        say(ai)


if __name__ == "__main__":
    handler.start()
