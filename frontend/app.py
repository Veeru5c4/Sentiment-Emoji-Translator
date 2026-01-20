import os

import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def main() -> None:
    st.set_page_config(
        page_title="AI Summary & Sentiment/Emoji Translator",
        page_icon="✨",
        layout="centered",
    )

    st.title("AI Summary & Sentiment/Emoji Translator")
    st.caption(
        "Paste up to a few pages of text. The app will create a four-line summary, "
        "detect sentiment, and highlight key sentences with emojis."
    )

    with st.expander("OpenAI API key options", expanded=False):
        st.markdown(
            "- **Option 1**: Use the server's configured OpenAI key (recommended for team setups).\n"
            "- **Option 2**: Enter your own OpenAI key below. It is sent only to the backend for this request."
        )
        user_api_key = st.text_input(
            "Optional: Your OpenAI API key",
            type="password",
            help="Leave empty to use the backend's configured key.",
        )

    text = st.text_area(
        "Paste your text here",
        height=260,
        placeholder="Paste 1–2 pages of text to summarize and analyze sentiment...",
    )

    analyze_clicked = st.button("Analyze ✨", type="primary", use_container_width=True)

    if analyze_clicked:
        if not text.strip():
            st.warning("Please paste some text to analyze.")
            return

        with st.spinner("Analyzing with OpenAI..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/analyze",
                    json={"text": text, "api_key": user_api_key or None},
                    timeout=60,
                )
            except requests.RequestException as exc:
                st.error(f"Failed to contact backend at {BACKEND_URL}: {exc}")
                return

        if response.status_code != 200:
            try:
                detail = response.json().get("detail")
            except Exception:  # noqa: BLE001
                detail = response.text
            st.error(f"Backend error ({response.status_code}): {detail}")
            return

        data = response.json()
        summary = data.get("summary", "")
        sentiment = data.get("sentiment", "").lower()
        highlights = data.get("highlights", [])

        st.subheader("Summary")
        st.markdown(
            f"```text\n{summary}\n```",
            help="Four-line summary generated from your input.",
        )

        st.subheader("Sentiment")
        sentiment_emoji = {
            "positive": "😊",
            "neutral": "😐",
            "negative": "😞",
        }.get(sentiment, "🤔")

        sentiment_color = {
            "positive": "✅",
            "neutral": "⚪️",
            "negative": "❌",
        }.get(sentiment, "⚪️")

        st.markdown(
            f"**Overall Sentiment**: {sentiment_color} {sentiment_emoji} `{sentiment or 'unknown'}`"
        )

        st.subheader("Highlight Sentences with Emojis")
        if not highlights:
            st.info("No highlight sentences were returned.")
        else:
            for item in highlights:
                sentence = item.get("sentence", "")
                emoji = item.get("emoji", "")
                st.markdown(f"- {emoji} {sentence}")


if __name__ == "__main__":
    main()


