from dotenv import load_dotenv

load_dotenv()

import streamlit as st
st.title("LLM機能を搭載したWebアプリ")

# --- アプリ概要 / 使い方 ---
st.markdown(
    """このWebアプリでは、入力テキストに対してLLMが回答します。  
下の手順で操作してください。

1. **専門家の種類** をラジオボタンで選択  
2. **入力テキスト** を入力して **送信** を押す  
"""
)

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# =========================
# 1) 専門家選択（ラジオ）
# =========================
expert_type = st.radio(
    "LLMに振る舞わせる専門家を選択してください",
    ["プログラムの専門家", "歴史の専門家"],
    horizontal=True,
)

# =========================
# 2) LLM呼び出し関数
# =========================
def ask_llm(input_text: str, selected_expert: str) -> str:
    """入力テキストと専門家の選択値を受け取り、LLMの回答を返す。"""
    if selected_expert == "プログラムの専門家":
        system_prompt = (
            "あなたはプログラミングの専門家です。"
            "初心者にも分かるように、正確で実用的な説明を日本語で行ってください。"
            "必要に応じて手順や注意点も補足してください。"
        )
    elif selected_expert == "歴史の専門家":
        system_prompt = (
            "あなたは歴史の専門家です。"
            "史実に基づき、可能な限り正確に日本語で説明してください。"
            "時代背景や因果関係も分かりやすく整理してください。"
        )
    else:
        system_prompt = "あなたは有能なアシスタントです。日本語で分かりやすく回答してください。"

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text),
    ]
    result = llm.invoke(messages)
    return result.content

# =========================
# 3) 入力 & 実行
# =========================
input_text = st.text_area("入力テキスト", height=140, placeholder="ここに質問や相談内容を入力してください")
send = st.button("送信")

if send:
    if not input_text.strip():
        st.warning("入力テキストを入力してください。")
    else:
        with st.spinner("回答を生成しています..."):
            answer = ask_llm(input_text=input_text, selected_expert=expert_type)
        st.markdown("### 回答")
        st.write(answer)
