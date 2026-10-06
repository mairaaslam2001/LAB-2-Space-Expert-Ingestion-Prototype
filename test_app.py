from bs4 import BeautifulSoup

import app


def test_extract_experts_from_valid_speakers_section():
    html = """
    <html><body>
    <h2>Speakers</h2>
    <h3>Alice</h3>
    <h3>Bob</h3>
    <h3>Charlie</h3>
    </body></html>
    """
    soup = BeautifulSoup(html, "html.parser")

    experts = app.extract_experts(soup)

    assert experts == ["Alice", "Bob", "Charlie"]


def test_extract_experts_returns_empty_list_when_section_missing():
    html = "<html><body><h2>Agenda</h2></body></html>"
    soup = BeautifulSoup(html, "html.parser")

    experts = app.extract_experts(soup)

    assert experts == []
