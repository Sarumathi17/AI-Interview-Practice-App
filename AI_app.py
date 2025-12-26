import streamlit as st
from questions import QUESTIONS
from evaluation import evaluate_answer

# Fixed order of questions
QUESTION_IDS = list(QUESTIONS.keys())

# ---------- AUDIO CONFIG ----------
MIN_AUDIO_SECONDS = 2.5


def audio_duration_seconds(audio_bytes: bytes, sample_rate=16000) -> float:
    """Estimate duration of audio in seconds."""
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
        "editable_transcript": "",
        "has_evaluated": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ---------- NAVIGATION ----------
def go_to_next_question():
    st.session_state.current_index = (st.session_state.current_index + 1) % len(QUESTION_IDS)
    st.session_state.current_qid = QUESTION_IDS[st.session_state.current_index]

    st.session_state.last_result = None
    st.session_state.show_result = False
    st.session_state.warning_message = ""
    st.session_state.answer_text = ""
    st.session_state.editable_transcript = ""
    st.session_state.has_evaluated = False

    audio_key = f"audio_input_{st.session_state.current_qid}"
    if audio_key in st.session_state:
        del st.session_state[audio_key]


# ---------- RESET WHEN USER EDITS ----------
def reset_after_edit():
    if st.session_state.get("has_evaluated", False):
        st.session_state.last_result = None
        st.session_state.show_result = False
        st.session_state.warning_message = ""
        st.session_state.has_evaluated = False


# ---------- EVALUATION ----------
def evaluate_current_answer():
    qid = st.session_state.current_qid
    mode = st.session_state.input_mode

    # -------- TEXT MODE --------
    if mode == "Text":
        user_ans = st.session_state.get("answer_text", "").strip()

        if not user_ans:
            st.session_state.warning_message = "Please type your answer before evaluating 😊"
            st.session_state.last_result = None
            st.session_state.show_result = False
            return

    # -------- AUDIO MODE --------
    else:
        audio_key = f"audio_input_{qid}"
        audio_data = st.session_state.get(audio_key)

        if audio_data is None:
            st.session_state.warning_message = "Please record your answer before evaluating 🎙️"
            st.session_state.last_result = None
            st.session_state.show_result = False
            return

        audio_bytes = audio_data.getvalue()
        duration = audio_duration_seconds(audio_bytes)

        if duration < MIN_AUDIO_SECONDS:
            st.session_state.warning_message = (
                f"Recording too short ({duration:.1f}s). Please record again 🎙️"
            )
            st.session_state.last_result = None
            st.session_state.show_result = False
            return

        user_ans = st.session_state.get("editable_transcript", "").strip()

        if not user_ans:
            st.session_state.warning_message = (
                "Transcript is empty. Please edit or retry recording."
            )
            st.session_state.last_result = None
            st.session_state.show_result = False
            return

    # -------- FINAL EVALUATION --------
    st.session_state.warning_message = ""
    st.session_state.last_result = evaluate_answer(qid, user_ans)
    st.session_state.show_result = True
    st.session_state.has_evaluated = True


# ---------- MAIN APP ----------
def main():
    st.set_page_config(page_title="ML Interview Practice", page_icon="🎤")
    init_session()

    st.title("🎤 ML Interview Practice – Text & Audio (Phase 3)")

    # -------- Input Mode --------
    st.markdown("### Input Mode")
    st.session_state.input_mode = st.radio(
        "Choose how you want to answer:",
        ["Text", "Audio"],
        horizontal=True,
    )

    if st.session_state.input_mode != st.session_state.prev_input_mode:
        st.session_state.last_result = None
        st.session_state.show_result = False
        st.session_state.warning_message = ""
        st.session_state.answer_text = ""
        st.session_state.editable_transcript = ""
        st.session_state.has_evaluated = False
        st.session_state.prev_input_mode = st.session_state.input_mode

    mode = st.session_state.input_mode
    qid = st.session_state.current_qid
    audio_key = f"audio_input_{qid}"

    # -------- Question --------
    st.markdown("### Question")
    st.write(QUESTIONS[qid]["question"])

    st.markdown("### Your Answer")

    # -------- TEXT MODE --------
    if mode == "Text":
        st.text_area(
            "Type your answer here:",
            key="answer_text",
            height=200,
            on_change=reset_after_edit,
        )

    # -------- AUDIO MODE --------
    else:
        st.write("🎤 Record your answer using the microphone.")
        audio_data = st.audio_input(
            "Record your answer here:",
            sample_rate=16000,
            key=audio_key,
        )

        if st.button("🔁 Retry recording"):
            if audio_key in st.session_state:
                del st.session_state[audio_key]
            st.session_state.editable_transcript = ""
            st.session_state.last_result = None
            st.session_state.show_result = False
            st.session_state.has_evaluated = False
            st.success("Recording cleared. You can record again 🎙️")

        if audio_data is not None:
            st.audio(audio_data)
            st.info("🎙 Audio recorded. You can edit the transcript or evaluate.")

            if not st.session_state.editable_transcript:
                st.session_state.editable_transcript = transcribe_audio_file(
                    audio_data.getvalue()
                )

        if st.session_state.editable_transcript:
            st.markdown("#### ✏️ Edit Transcript Before Evaluation")
            st.text_area(
                "Edit transcript:",
                key="editable_transcript",
                height=150,
                on_change=reset_after_edit,
            )

    # -------- Buttons --------
    col1, col2 = st.columns(2)
    with col1:
        st.button("✅ Evaluate my answer", on_click=evaluate_current_answer)
    with col2:
        st.button("⏭ Next question", on_click=go_to_next_question)

    # -------- Messages --------
    if st.session_state.show_result and st.session_state.last_result:
        st.success("✅ Answer evaluated.")

    if st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

    # -------- Result --------
    if st.session_state.show_result and st.session_state.last_result:
        result = st.session_state.last_result

        st.markdown("---")
        st.metric("Total Score (out of 10)", result["total_score"])
        st.write(f"Keyword score: {result['keyword_score']}")
        st.write(f"Length score: {result['length_score']}")
        st.write(f"Semantic score: {result['semantic_score']}")

        st.markdown("### Feedback")
        st.write(result["feedback"])

        if result["missing_keywords"]:
            st.write("Missing points:", ", ".join(result["missing_keywords"]))

        with st.expander("💡 Show ideal answer"):
            st.write(result["ideal_answer"])


if __name__ == "__main__":
    main()
