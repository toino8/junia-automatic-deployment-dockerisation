import pytest
from streamlit.testing.v1 import AppTest


@pytest.mark.parametrize(
    argnames="temp_mapping",
    argvalues=[
        "Accurate",
        "Balanced",
        "Creative",
    ],
)
def test_temp_selector(temp_mapping):
    at = AppTest.from_file("main.py").run()

    at.radio(key="temperature").set_value(temp_mapping).run()

    assert at.radio(key="temperature").value == temp_mapping
