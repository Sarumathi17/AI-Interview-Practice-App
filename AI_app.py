import streamlit as st
from questions import QUESTIONS
from evaluation import evaluate_answer

# Fixed order of questions
QUESTION_IDS = list(QUESTIONS.keys())

# ---------- AUDIO CONFIG ----------
MIN_AUDIO_SECONDS = 2.5


def audio_duration_seconds(audio_bytes: bytes, sample_rate=16000) -> float:
    return len(audio_bytes) / (sample_rate * 2)


def transcribe_audio_file(audio_bytes: bytes) -> str:
    """
    Placeholder Speech-to-Text.
    Replace later with Whisper / API.
    """
    return "This is a placeholder transcript from the recorded audio."


# ---------- SESSION STATE ----------
def init_session():
    defaults = {
        "current_index": 0,
        "current_qid": QUESTION_IDS[0],
        "last_result": None,
        "show_result": False,
        "warning_message": "",
        "input_mode": "Text",
        "prev_input_mode": "Text",
        "answer_text": "",
        "editable_transcript": ""
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ---------- NAVIGATION ----------
def go_to_next_question():
    st.session_state.current_index = (st.session_state.current_index + 1) % len(QUESTION_IDS)
    st.session_state.current_qid = QUESTION_IDS[st.session_state.current_index]

    # reset state
    st.session_state.last_result = None
    st.session_state.show_result = False
    st.session_state.warning_message = ""
    st.session_state.answer_text = ""
    st.session_state.editable_transcript = ""

    # clear audio widget
    audio_key = f"audio_input_{st.session_state.current_qid}"
    if audio_key in st.session_state:
        del st.session_state[audio_key]


# ---------- EVALUATION ----------
def evaluate_current_answer():
    qid = st.session_state.current_qid
    mode = st.session_state.input_mode
    audio_key = f"audio_input_{qid}"

    # -------- TEXT MODE --------
    if mode == "Text":
        user_ans = st.session_state.answer_text.strip()
        if not user_ans:
            st.session_state.warning_message = "Please type your answer before evaluating 😊"
            return

    # -------- AUDIO MODE --------
    else:
        audio_data = st.session_state.get(audio_key)
        if audio_data is None:
            st.session_state.warning_message = "Please record your answer before evaluating 🎙️"
            return

        audio_bytes = audio_data.getvalue()
        duration = audio_duration_seconds(audio_bytes)

        if duration < MIN_AUDIO_SECONDS:
            st.session_state.warning_message = (
                f"Recording too short ({duration:.1f}s). Please record again 🎙️"
            )
            return

        user_ans = st.session_state.editable_transcript.strip()
        if not user_ans:
            st.session_state.warning_message = "Transcript is empty. Please edit or retry recording."
            return

    # -------- FINAL EVALUATION --------
    st.session_state.warning_message = ""
    st.session_state.last_result = evaluate_answer(qid, user_ans)
    st.session_state.show_result = True


# ---------- MAIN APP ----------
def main():
    st.set_page_config(page_title="ML Interview Practice", page_icon="🎤")
    init_session()

    st.title("🎤 ML Interview Practice – Text & Audio (Phase 2)")

    # -------- Input Mode --------
    st.markdown("### Input Mode")
    st.session_state.input_mode = st.radio(
        "Choose how you want to answer:",
        ["Text", "Audio"],
        horizontal=True
    )

    # Reset when switching modes
    if st.session_state.input_mode != st.session_state.prev_input_mode:
        st.session_state.last_result = None
        st.session_state.show_result = False
        st.session_state.warning_message = ""
        st.session_state.answer_text = ""
        st.session_state.editable_transcript = ""
        st.session_state.prev_input_mode = st.session_state.input_mode

    mode = st.session_state.input_mode
    qid = st.session_state.current_qid
    question_data = QUESTIONS[qid]
    audio_key = f"audio_input_{qid}"

    # -------- Question --------
    st.markdown("### Question")
    st.write(question_data["question"])

    st.markdown("### Your Answer")

    # -------- TEXT MODE --------
    if mode == "Text":
        st.text_area(
            "Type your answer here:",
            key="answer_text",
            height=200,
            label_visibility="collapsed"
        )

    # -------- AUDIO MODE --------
    else:
        st.write("🎤 Record your answer using the microphone.")
        audio_data = st.audio_input(
            "Record your answer here:",
            sample_rate=16000,
            key=audio_key
        )

        if st.button("🔁 Retry recording"):
            if audio_key in st.session_state:
                del st.session_state[audio_key]
            st.session_state.editable_transcript = ""
            st.session_state.last_result = None
            st.session_state.show_result = False
            st.success("Recording cleared. You can record again 🎤")

        if audio_data is not None:
            st.audio(audio_data)

            # 🔹 AUTO-GENERATE TRANSCRIPT (ONCE)
            if not st.session_state.editable_transcript:
                st.session_state.editable_transcript = transcribe_audio_file(
                    audio_data.getvalue()
                )

        # 🔹 ALWAYS SHOW EDITOR IF TRANSCRIPT EXISTS
        if st.session_state.editable_transcript:
            st.markdown("#### ✏️ Edit Transcript Before Evaluation")
            st.text_area(
                "You can edit the transcribed text:",
                key="editable_transcript",
                height=150
            )

    # -------- Buttons --------
    col1, col2 = st.columns(2)
    with col1:
        st.button("✅ Evaluate my answer", on_click=evaluate_current_answer)
    with col2:
        st.button("⏭ Next question", on_click=go_to_next_question)

    # -------- Warning --------
    if st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    # -------- Result --------
    if st.session_state.show_result and st.session_state.last_result:
        result = st.session_state.last_result
        st.markdown("---")
        st.metric("Total Score (out of 10)", result["total_score"])
        st.write(f"Keyword score: {result['keyword_score']}")
        st.write(f"Length score: {result['length_score']}")
        st.markdown("### Feedback")
        st.write(result["feedback"])

        if result["missing_keywords"]:
            st.write("Missing points:", ", ".join(result["missing_keywords"]))

        with st.expander("💡 Show ideal answer"):
            st.write(result["ideal_answer"])


if __name__ == "__main__":
    main()
