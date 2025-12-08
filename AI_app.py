# app.py

import streamlit as st
from questions import QUESTIONS
from evaluation import evaluate_answer

# Fixed order of questions
QUESTION_IDS = list(QUESTIONS.keys())


# ---------- AUDIO TRANSCRIPTION (placeholder) ----------

def transcribe_audio_file(audio_bytes: bytes) -> str:
    """
    Placeholder function for audio transcription.

    In the future, integrate a real Speech-to-Text model here
    (e.g., Whisper or any cloud STT service).

    For now, it just returns a dummy transcript so the flow works.
    """
    # TODO: Replace with real STT logic later
    return "This is a placeholder transcript from the recorded audio."


# ---------- SESSION STATE SETUP ----------

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
        st.session_state.input_mode = "Text"  # "Text" or "Audio"
    if "answer_text" not in st.session_state:
        st.session_state.answer_text = ""


# ---------- NAVIGATION ----------

def go_to_next_question():
    """Move to the next question and clear answer/result."""
    st.session_state.current_index = (st.session_state.current_index + 1) % len(QUESTION_IDS)
    st.session_state.current_qid = QUESTION_IDS[st.session_state.current_index]

    # Reset for new question
    st.session_state.last_result = None
    st.session_state.show_result = False
    st.session_state.warning_message = ""
    st.session_state.answer_text = ""   # text box should start empty


# ---------- EVALUATION ----------

def evaluate_current_answer():
    """Evaluate the answer for the CURRENT question only, from text or audio."""
    mode = st.session_state.get("input_mode", "Text")
    qid = st.session_state.current_qid

    # we'll use a per-question key for audio
    audio_key = f"audio_input_{qid}"

    # ----- TEXT MODE -----
    if mode == "Text":
        user_ans = st.session_state.get("answer_text", "").strip()

        if not user_ans:
            st.session_state.last_result = None
            st.session_state.show_result = False
            st.session_state.warning_message = "Please type your answer before evaluating 😊"
            return

    # ----- AUDIO MODE -----
    else:
        audio_data = st.session_state.get(audio_key, None)
        if audio_data is None:
            st.session_state.last_result = None
            st.session_state.show_result = False
            st.session_state.warning_message = "Please record your answer before evaluating 🎙️"
            return

        # Get raw bytes from mic recording
        audio_bytes = audio_data.getvalue()

        # Transcribe (placeholder)
        transcript = transcribe_audio_file(audio_bytes)

        # Store transcript so UI can show it
        st.session_state.answer_text = transcript
        user_ans = transcript.strip()

        if not user_ans:
            st.session_state.last_result = None
            st.session_state.show_result = False
            st.session_state.warning_message = "Transcription returned empty text. Please try again."
            return

    # ----- COMMON EVALUATION PART -----
    st.session_state.warning_message = ""
    result = evaluate_answer(qid, user_ans)
    st.session_state.last_result = result
    st.session_state.show_result = True


# ---------- MAIN APP ----------

def main():
    st.set_page_config(page_title="ML Interview Practice", page_icon="🎤")
    init_session()

    st.title("🎤 ML Interview Practice – Text + Audio (Phase 2)")
    st.write(
        "The app shows one **ML interview question** at a time.\n\n"
        "You can answer using either **text** or **audio**.\n\n"
        "1. Choose input mode (Text / Audio)\n"
        "2. Read the question\n"
        "3. Answer in the selected mode\n"
        "4. Click **Evaluate my answer**\n"
        "5. Compare with the ideal answer\n"
        "6. Click **Next question** to move on"
    )

    # ----- Input mode selection -----
    st.markdown("### Input Mode")
    st.session_state.input_mode = st.radio(
        "Choose how you want to answer:",
        options=["Text", "Audio"],
        horizontal=True,
        key="input_mode_radio",
    )

    mode = st.session_state.input_mode

    # ----- Current question -----
    qid = st.session_state.current_qid
    question_data = QUESTIONS[qid]

    st.markdown("### Question")
    st.write(question_data["question"])

    # per-question key for audio widget
    audio_key = f"audio_input_{qid}"

    # ----- Answer input -----
    st.markdown("### Your Answer")

    if mode == "Text":
        st.text_area(
            "Type your answer here:",
            key="answer_text",
            height=200,
            label_visibility="collapsed"
        )
    else:
        st.write("🎤 Record a short audio answer using your microphone.")
        audio_data = st.audio_input(
            "Record your answer here:",
            sample_rate=16000,
            key=audio_key
        )

        # Optional: preview audio for this question
        if audio_data is not None:
            st.write("Recording captured. You can now click **Evaluate my answer**.")
            st.audio(audio_data)

        # Show transcript if already generated (after evaluation)
        if st.session_state.get("answer_text", ""):
            st.markdown("#### Detected Transcript (from audio)")
            st.write(st.session_state.answer_text)

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
    st.caption("Phase 2 – Mic recording ready. Plug real Speech-to-Text into transcribe_audio_file(). 🚀")


if __name__ == "__main__":
    main()
