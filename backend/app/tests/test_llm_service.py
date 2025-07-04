import pytest
from unittest.mock import MagicMock, patch
from app.llm_service import LLMService

@pytest.fixture
def mock_openai_client():
    """Fixture to mock the OpenAI client."""
    with patch("app.llm_service.OpenAI") as MockOpenAI:
        mock_instance = MagicMock()
        MockOpenAI.return_value = mock_instance

        # Mock the nested call: client.chat.completions.create(...)
        mock_instance.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="Paris is the capital of France."))
        ]

        yield mock_instance

def test_generate_response_with_openai(mock_openai_client):
    """Test LLMService with OpenAI."""
    llm_service = LLMService(model="gpt-3.5-turbo", use_ollama=False)

    # Act
    response = llm_service.generate_response(
        query="What is the capital of France?",
        context=["Paris is the capital of France.", "France is a country in Europe."]
    )

    # Assert
    assert response == "Paris is the capital of France."
    mock_openai_client.chat.completions.create.assert_called_once()