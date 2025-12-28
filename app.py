
from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

# =========================
# 環境変数の読み込み
# =========================
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY が設定されていません。.env または Secrets を確認してください。")
    st.stop()

# OpenAI クライアント
client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# LLM呼び出し関数
# =========================
def get_llm_response(user_text: str, expert_type: str) -> str:
    if expert_type == "A：ITコンサルタント":
        system_message = "あなたは経験豊富なITコンサルタントです。専門的かつ実務的に回答してください。"
    elif expert_type == "B：教育分野の専門家":
        system_message = "あなたは教育分野の専門家です。初心者にも分かりやすく丁寧に説明してください。"
    else:
        system_message = "あなたは有能な専門家です。"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_text},
        ],
        temperature=0.5,
    )

    # ✅ OpenAI SDK v1.0以降の正しい取得方法
    return response.choices[0].message.content

# =========================
# Streamlit UI
# =========================
st.title("LLM専門家相談アプリ")

st.markdown("""
### アプリ概要
このアプリでは、質問内容を入力し、専門家の種類を選択することで  
AI（LLM）が専門家として回答します。

**使い方**
1. 質問を入力  
2. 専門家の種類を選択  
3. 「送信」をクリック
""")

user_input = st.text_input("質問を入力してください")

expert_type = st.radio(
    "専門家を選択してください",
    ("A：ITコンサルタント", "B：教育分野の専門家"),
)

if st.button("送信"):
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("AIが考えています..."):
            answer = get_llm_response(user_input, expert_type)
            st.success("AIの回答")
            st.write(answer)


