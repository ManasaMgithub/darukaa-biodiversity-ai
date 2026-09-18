import json
import re

import streamlit as st

from src.conversation import (
    update_environment_state,
    conversation_status,
)
from src.reasoning import analyze_environment


st.set_page_config(
    page_title="Darukaa Earth",
    page_icon="🌱",
    layout="wide",
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "environment_state" not in st.session_state:
    st.session_state.environment_state = {}


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

st.title("🌱 Darukaa Earth")
st.subheader("AI Biodiversity & Environmental Intelligence")

st.write(
    "Describe an environmental situation and receive "
    "evidence-grounded, multi-metric biodiversity recommendations."
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.header("🌍 Environmental Context")

    state = st.session_state.environment_state

    if state:
        st.success("Environmental profile detected")

        for factor, value in state.items():
            label = factor.replace("_", " ").title()

            st.markdown(f"**{label}**")
            st.caption(str(value))

    else:
        st.info(
            "Environmental information will appear here "
            "as you describe the situation."
        )

    st.divider()

    st.header("📥 Input Format")

    input_mode = st.radio(
        "Choose input type:",
        ["Natural Language", "JSON"],
    )

    st.divider()

    st.caption(
        "The system combines environmental variables, "
        "retrieved scientific evidence, and multi-metric reasoning."
    )


# ---------------------------------------------------------
# DISPLAY PREVIOUS CHAT
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

if input_mode == "Natural Language":

    user_input = st.chat_input(
        "Describe your environmental situation..."
    )

else:

    user_input = st.chat_input(
        'Example: {"soil_organic_carbon": 0.3, '
        '"rainfall": "low", '
        '"land_use": "wheat monoculture"}'
    )


# ---------------------------------------------------------
# PROCESS USER INPUT
# ---------------------------------------------------------

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)


    # -----------------------------------------------------
    # JSON INPUT
    # -----------------------------------------------------

    if input_mode == "JSON":

        try:

            data = json.loads(user_input)

            if not isinstance(data, dict):

                raise ValueError(
                    "JSON input must contain an object."
                )

            for key, value in data.items():

                st.session_state.environment_state[key] = str(value)

            environment_state = (
                st.session_state.environment_state
            )

        except (json.JSONDecodeError, ValueError) as error:

            response = (
                "⚠️ **Invalid JSON input.**\n\n"
                "Please provide a valid JSON object."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response,
                }
            )

            with st.chat_message("assistant"):
                st.error(str(error))

            st.stop()


    # -----------------------------------------------------
    # NATURAL LANGUAGE INPUT
    # -----------------------------------------------------

    else:

        environment_state = update_environment_state(
            st.session_state.environment_state,
            user_input,
        )


    # -----------------------------------------------------
    # CHECK REQUIRED ENVIRONMENTAL VARIABLES
    # -----------------------------------------------------

    status = conversation_status(
        environment_state
    )


    # -----------------------------------------------------
    # ASK CLARIFICATION QUESTIONS
    # -----------------------------------------------------

    if not status["complete"]:

        questions = status["questions"]

        response = (
            "I need a little more environmental information "
            "before I can make a grounded recommendation.\n\n"
        )

        response += "\n".join(
            f"{i}. {question}"
            for i, question in enumerate(questions, 1)
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        with st.chat_message("assistant"):
            st.info(response)


    # -----------------------------------------------------
    # RUN AI ENVIRONMENTAL ANALYSIS
    # -----------------------------------------------------

    else:

        context_parts = []

        for factor, value in environment_state.items():

            context_parts.append(
                f"{factor.replace('_', ' ')}: {value}"
            )

        combined_query = "\n".join(
            context_parts
        )

        combined_query += (
            f"\nUser description: {user_input}"
        )


        with st.chat_message("assistant"):

            with st.spinner(
                "🔬 Analyzing environmental interactions "
                "and scientific evidence..."
            ):

                try:

                    result = analyze_environment(
                        combined_query
                    )

                    response = result["answer"]


                    # -------------------------------------------------
                    # MAIN AI RESPONSE
                    # -------------------------------------------------

                    st.markdown(
                        "## 🌍 Environmental Intelligence"
                    )

                    st.markdown(response)


                    # -------------------------------------------------
                    # RETRIEVED EVIDENCE
                    # -------------------------------------------------

                    st.divider()

                    st.markdown(
                        "## 📚 Retrieved Scientific Evidence"
                    )

                    st.caption(
                        "Evidence retrieved from the biodiversity "
                        "knowledge base using semantic search."
                    )


                    for i, source in enumerate(
                        result["sources"],
                        1,
                    ):

                        similarity = source.get(
                            "score",
                            0,
                        )

                        source_name = source.get(
                            "source",
                            "Scientific source",
                        )

                        with st.expander(
                            f"Evidence {i}  •  "
                            f"Similarity {similarity:.3f}"
                        ):

                            st.markdown(
                                f"**Source:** {source_name}"
                            )

                            st.progress(
                                min(
                                    max(
                                        float(similarity),
                                        0.0,
                                    ),
                                    1.0,
                                )
                            )

                            st.markdown(
                                source.get(
                                    "text",
                                    "",
                                )
                            )


                    # -------------------------------------------------
                    # RETRIEVAL SUMMARY
                    # -------------------------------------------------

                    st.divider()

                    st.markdown(
                        "### 🔎 Knowledge Retrieval Summary"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Evidence Retrieved",
                            len(result["sources"]),
                        )

                    with col2:

                        if result["sources"]:

                            avg_similarity = (
                                sum(
                                    source.get(
                                        "score",
                                        0,
                                    )
                                    for source in result["sources"]
                                )
                                / len(result["sources"])
                            )

                            st.metric(
                                "Avg. Similarity",
                                f"{avg_similarity:.3f}",
                            )

                        else:

                            st.metric(
                                "Avg. Similarity",
                                "N/A",
                            )

                    with col3:

                        st.metric(
                            "Environmental Variables",
                            len(environment_state),
                        )


                    # -------------------------------------------------
                    # SAVE RESPONSE
                    # -------------------------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response,
                        }
                    )


                except Exception as error:

                    error_message = (
                        "⚠️ An error occurred while analyzing "
                        "the environmental situation."
                    )

                    st.error(error_message)

                    st.exception(error)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Darukaa Earth — Evidence-grounded biodiversity intelligence"
)