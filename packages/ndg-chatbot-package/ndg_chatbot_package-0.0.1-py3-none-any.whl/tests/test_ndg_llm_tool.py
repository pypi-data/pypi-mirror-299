import pytest
import unittest

from promptflow.connections import CustomConnection
from ndg_chatbot_package.tools.ndg_llm_tool import ndg_llm_tool


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_ndg_llm_tool(self, my_custom_connection):
        result = ndg_llm_tool(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()