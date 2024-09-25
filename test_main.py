from unittest.mock import patch, AsyncMock

import pytest

from main import check_url_methods, process_strings


@pytest.mark.asyncio
async def test_check_url_methods():
    url = "https://example.com"

    with patch('aiohttp.ClientSession') as mock_session:
        mock_session_instance = mock_session.return_value
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_session_instance.__aenter__.return_value.request = AsyncMock(return_value=mock_response)
        result = await check_url_methods(url)

        assert "GET" in result
        assert result["GET"] == 200


@pytest.mark.asyncio
async def test_process_strings():
    strings = ["https://example.com", "invalid_string"]

    with patch('main.check_url_methods', return_value={"GET": 200}):
        result = await process_strings(strings)

        assert "https://example.com" in result
        assert "GET" in result["https://example.com"]
        assert result["https://example.com"]["GET"] == 200
        assert "invalid_string" not in result
