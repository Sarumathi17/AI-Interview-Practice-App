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
    if "input_mode" not in st.session_state:
        st.session_state.input_mode = "Text"
    if "answer_text" not in st.session_state:
        st.session_state.answer_text = ""


# ---------- NAVIGATION ----------

def go_to_next_question():
    st.session_state.current_index = (st.session_state.current_index + 1) % len(QUESTION_IDS)
    st.session_state.current_qid = QUESTION_IDS[st.session_state.current_index]
    st.session_state.last_result = None
    st.session_state.show_result = False
    st.session_state.warning_message = ""
    st.session_state.answer_text = ""


# ---------- EVALUATION ----------

def evaluate_current_answer():
    user_ans = None
    mode = st.session_state.get("input_mode", "Text")
    qid = st.session_state.current_qid
    audio_key = f"audio_input_{qid}"

    # ----- TEXT MODE -----
    if mode == "Text":
        user_ans = st.session_state.get("answer_text", "").strip()

        if not user_ans:
            st.session_state.warning_message = "Please type your answer before evaluating 😊"
            return

    # ----- AUDIO MODE -----
    else:
        audio_data = st.session_state.get(audio_key)

        if audio_data is None:
            st.session_state.warning_message = "Please record your answer before evaluating 🎙️"
            return

        audio_bytes = audio_data.getvalue()

        duration = audio_duration_seconds(audio_bytes)

        if duration < MIN_AUDIO_SECONDS:
            st.session_state.warning_message = (
                f"Recording too short ({duration:.1f}s). "
                "Please record again and speak clearly 🎙️"
            )
            return

        transcript = transcribe_audio_file(audio_bytes)
        user_ans = transcript.strip()
        st.session_state.answer_text = user_ans

        if not user_ans:
            st.session_state.warning_message = "Transcription failed. Please try again."
            return

    # ----- FINAL EVALUATION -----
    st.session_state.warning_message = ""
    result = evaluate_answer(qid, user_ans)
    st.session_state.last_result = result
    st.session_state.show_result = True


# ---------- MAIN APP ----------

def main():
    st.set_page_config(page_title="ML Interview Practice", page_icon="🎤")
    init_session()

    st.title("🎤 ML Interview Practice – Text & Audio (Phase 2)")

    st.markdown("### Input Mode")
    st.session_state.input_mode = st.radio(
        "Choose how you want to answer:",
        ["Text", "Audio"],
        horizontal=True
    )

    mode = st.session_state.input_mode

    qid = st.session_state.current_qid
    question_data = QUESTIONS[qid]
    audio_key = f"audio_input_{qid}"

    st.markdown("### Question")
    st.write(question_data["question"])

    st.markdown("### Your Answer")

    if mode == "Text":
        st.text_area(
            "Type your answer here:",
            key="answer_text",
            height=200,
            label_visibility="collapsed"
        )
    else:
        st.write("🎤 Record your answer using the microphone.")
        audio_data = st.audio_input(
            "Record your answer here:",
            sample_rate=16000,
            key=audio_key
        )

        if st.button("🔁 Retry recording"):
            st.session_state.answer_text = ""
            st.session_state.last_result = None
            st.session_state.show_result = False
            st.success("Recording cleared. You can record again 🎤")

        if audio_data is not None:
            st.audio(audio_data)

        if st.session_state.answer_text:
            st.markdown("#### Detected Transcript")
            st.write(st.session_state.answer_text)

    col1, col2 = st.columns(2)

    with col1:
        st.button("✅ Evaluate my answer", on_click=evaluate_current_answer)

    with col2:
        st.button("⏭ Next question", on_click=go_to_next_question)

    if st.session_state.warning_message:
        st.warning(st.session_state.warning_message)

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
