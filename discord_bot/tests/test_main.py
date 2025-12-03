import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from bot.main import (
    hello_handler,
    prompt_handler,
    client,
)
from bot.env_loader import user_id


@pytest_asyncio.fixture
async def mock_interaction():
    """Cria um mock básico de discord.Interaction."""
    interaction = MagicMock()
    interaction.user = MagicMock()
    interaction.user.id = user_id  # usuário autorizado
    interaction.user.mention = "@User"
    interaction.guild = MagicMock()
    interaction.guild.id = "123"

    interaction.channel = MagicMock()
    interaction.channel.id = "456"

    # response / followup mocks
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()

    return interaction


@pytest.mark.asyncio
async def test_hello_handler(mock_interaction):
    await hello_handler(mock_interaction)

    mock_interaction.response.send_message.assert_called_once_with(
        "Hello, @User!"
    )


@pytest.mark.asyncio
async def test_prompt_handler_authorized(mock_interaction):
    """Testa o fluxo normal com usuário autorizado."""

    with patch("bot.main.requests.post") as mock_post:
        mock_post.return_value.status_code = 200

        await prompt_handler(mock_interaction, "qual o sentido da vida?", "http://fake-url")

        # resposta imediata no Discord
        mock_interaction.response.send_message.assert_called_with(
            "qual o sentido da vida?"
        )

        # chamada HTTP enviada para o webhook
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        assert args[0] == "http://fake-url"
        assert kwargs["json"]["prompt"] == "qual o sentido da vida?"
        assert kwargs["json"]["user_id"] == str(user_id)
        assert kwargs["json"]["channel_id"] == "456"


@pytest.mark.asyncio
async def test_prompt_handler_unauthorized(mock_interaction):
    """Testa quando o usuário não é autorizado."""
    mock_interaction.user.id = "999999"  # id diferente

    await prompt_handler(mock_interaction, "oi?", "http://fake-url")

    mock_interaction.response.send_message.assert_called_once_with(
        "sorry @User, but I can't pay for all this token :'("
    )


@pytest.mark.asyncio
async def test_prompt_handler_http_error(mock_interaction):
    """Testa exceção ao chamar webhook."""
    with patch("bot.main.requests.post") as mock_post:
        mock_post.side_effect = Exception("HTTP ERROR")

        await prompt_handler(mock_interaction, "teste erro", "http://fake-url")

        mock_interaction.followup.send.assert_called_once()
        args, kwargs = mock_interaction.followup.send.call_args

        assert "HTTP ERROR" in args[0]
