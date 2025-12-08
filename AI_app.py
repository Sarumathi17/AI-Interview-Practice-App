# app.py

import streamlit as st
from questions import QUESTIONS
from evaluation import evaluate_answer

# Fixed order of questions
QUESTION_IDS = list(QUESTIONS.keys())


def init_session():
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "current_qid" not in st.session_state:
        st.session_state.current_qid = QUESTION_IDS[0]
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "show_result" not in st.session_state:
        st.session_state.show_result = False
    if "warning_message" not in st.session_state:
        st.session_state.warning_message = ""
    # IMPORTANT: do NOT touch 'answer_text' here.
    # Let the text_area widget create and update it.


def go_to_next_question():
    """Move to the next question and clear answer/result."""
    st.session_state.current_index = (st.session_state.current_index + 1) % len(QUESTION_IDS)
    st.session_state.current_qid = QUESTION_IDS[st.session_state.current_index]

    # Reset for new question
    st.session_state.last_result = None
    st.session_state.show_result = False
    st.session_state.warning_message = ""
    st.session_state.answer_text = ""   # clear the text box for the next question


def evaluate_current_answer():
    """Evaluate the answer for the CURRENT question only."""
    user_ans = st.session_state.get("answer_text", "").strip()

    if not user_ans:
        st.session_state.last_result = None
        st.session_state.show_result = False
        st.session_state.warning_message = "Please type your answer before evaluating 😊"
        return

    st.session_state.warning_message = ""
    qid = st.session_state.current_qid
    result = evaluate_answer(qid, user_ans)
    st.session_state.last_result = result
    st.session_state.show_result = True


def main():
    st.set_page_config(page_title="ML Interview Practice", page_icon="🎤")
    init_session()

    st.title("🎤 ML Interview Practice – MVP")
    st.write(
        "The app shows one **ML interview question** at a time.\n\n"
        "1. Read the question\n"
        "2. Type your answer\n"
        "3. Click **Evaluate my answer**\n"
        "4. Compare with the ideal answer\n"
        "5. Click **Next question** to move on"
    )

    # ----- Current question -----
    qid = st.session_state.current_qid
    question_data = QUESTIONS[qid]

    st.markdown("### Question")
    st.write(question_data["question"])

    # ----- Answer input -----
    st.markdown("### Your Answer")
    st.text_area(
        "Type your answer here:",
        key="answer_text",      # Streamlit manages this in session_state
        height=200,
        label_visibility="collapsed"
    )

    # ----- Buttons -----
    col1, col2 = st.columns(2)

    with col1:
        st.button("✅ Evaluate my answer", on_click=evaluate_current_answer)

    with col2:
        st.button("⏭ Next question", on_click=go_to_next_question)

    # ----- Warning (if any) -----
    if st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    # ----- Show result -----
    if st.session_state.show_result and st.session_state.last_result:
        result = st.session_state.last_result

        st.markdown("---")
        st.markdown("### 🧮 Your Score")
        st.metric("Total Score (out of 10)", result["total_score"])
        st.write(f"**Keyword score:** {result['keyword_score']}")
        st.write(f"**Length score:** {result['length_score']}")

        st.markdown("### ✍️ Feedback")
        st.write(result["feedback"])

        if result["missing_keywords"]:
            st.markdown("**Missing important points:**")
            st.write(", ".join(result["missing_keywords"]))

        with st.expander("💡 Show ideal answer"):
            st.write(result["ideal_answer"])

    st.markdown("---")
    st.caption("MVP version – ML questions only. Audio & advanced features coming later 🚀")


if __name__ == "__main__":
    main()