from src.conversation import (
    update_environment_state,
    conversation_status,
)


def test_incomplete_environment():

    state = {}

    state = update_environment_state(
        state,
        "My biodiversity is declining."
    )

    status = conversation_status(state)

    assert status["complete"] is False

    assert "soil_organic_carbon" in status["missing"]
    assert "rainfall" in status["missing"]
    assert "land_use" in status["missing"]


def test_complete_environment():

    state = {}

    state = update_environment_state(
        state,
        "My farm has SOC 0.3%, low rainfall and wheat monoculture."
    )

    status = conversation_status(state)

    assert status["complete"] is True
    assert status["missing"] == []