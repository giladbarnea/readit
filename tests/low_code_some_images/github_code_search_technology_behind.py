from pathlib import Path

from langchain.document_loaders import WebBaseLoader, BSHTMLLoader
from pytest import fixture
import requests

ARTICLE_URL: str = "https://github.blog/2023-02-06-the-technology-behind-githubs-new-code-search/"
ARTICLE_HTML_PATH: Path = Path(__file__).parent / "github_code_search_technology_behind.html"


@fixture(scope="module")
def article_html() -> str:
    from bs4 import BeautifulSoup

    html = requests.get(ARTICLE_URL).text
    soup = BeautifulSoup(html, "html.parser")
    soup.select_one("head").decompose()
    return soup.prettify()


def test_loads_fine():
    loader = WebBaseLoader(ARTICLE_URL)
    doc = loader.load()[0]
    assert "The technology behind GitHub’s new code search | The GitHub Blog" in doc.page_content
    assert (
        "We’re actively adding more repositories and fixing up the rough edges based on feedback from people just like"
        " you."
        in doc.page_content
    )


def test_github_code_search_technology_behind():
    loader = BSHTMLLoader(str(ARTICLE_HTML_PATH))
    doc = loader.load()[0]
    print()