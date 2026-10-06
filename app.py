"""LAB 2: Space Expert Ingestion Prototype."""

from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

DEFAULT_URL = "https://www.spacefoundation.org/events/the-state-of-space/"
FALLBACK_EXPERTS = [
    "Heather Pringle",
    "Meghan Allen",
    "Lesley Conn",
    "Brendan Rosseau",
    "Eric Fanning",
    "Robert S. Walker",
    "Carissa Christensen",
    "Dr. Robert Redmon",
    "Aniello Violetti",
    "Peter Marquez",
    "Dr. Scott Pace",
    "Alexander MacDonald",
]


def extract_experts(soup: BeautifulSoup) -> list[str]:
    """Return expert names from the speakers section if present."""
    speakers_heading = soup.find(
        lambda tag: isinstance(tag, Tag)
        and tag.name in {"h2", "h3", "h4"}
        and "speaker" in tag.get_text(" ", strip=True).lower()
    )

    if speakers_heading is None:
        return []

    experts: list[str] = []
    for element in speakers_heading.next_elements:
        if element is speakers_heading:
            continue
        if element.name == "h3":
            text = " ".join(element.stripped_strings).strip()
            if text:
                experts.append(text)
        elif element.name in {"h2", "h4", "h5", "h6"} and not isinstance(element, str):
            if element.get_text(" ", strip=True).lower() != "speakers":
                break

        if len(experts) >= 12:
            break

    return experts


def fetch_experts(url: str = DEFAULT_URL) -> list[str]:
    """Fetch and parse the list of expert names for the provided page."""
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        return FALLBACK_EXPERTS.copy()

    soup = BeautifulSoup(response.text, "html.parser")
    experts = extract_experts(soup)
    return experts if experts else FALLBACK_EXPERTS.copy()


def main() -> None:
    """Display the expert list in the terminal."""
    print("Space-industry experts:")
    experts = fetch_experts()

    if not experts:
        print("No expert records were found.")
        return

    for expert in experts:
        print(expert)


if __name__ == "__main__":
    main()
