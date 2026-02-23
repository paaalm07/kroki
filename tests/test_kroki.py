"""
    test_kroki
    ~~~~~~~~~~~~~~~~
    Test the kroki extension.
"""

import re
import pytest
from sphinx.application import Sphinx


def get_content(app: Sphinx) -> str:
    app.builder.build_all()

    index = app.outdir / "index.html"
    if hasattr(index, "read_text"):
        return index.read_text(encoding="utf-8")
    return index.text()


@pytest.mark.sphinx(
    "html", testroot="kroki", confoverrides={"master_doc": "index"}
)
def test_kroki_html(app, status, warning):
    content = get_content(app)
    html = (
        r'figure[^>]*?(?:kroki kroki-plantuml align-default)?" .*?>\s*'
        r'<img alt="bar -&gt; baz" class="kroki kroki-plantuml" .+?/>.*?'
        r'<span class="caption-text">caption of diagram</span>.*?</p>'
    )
    assert re.search(html, content, re.S)

    html = r'<p>Hello <img alt="bar -&gt; baz" class="kroki kroki-plantuml" .*?/> kroki world</p>'
    assert re.search(html, content, re.S)

    html = r'<img .+?class="kroki kroki-mermaid graph" .+?/>'
    assert re.search(html, content, re.S)

    html = r'<img .+?class="kroki kroki-graphviz" .*?/>'
    assert re.search(html, content, re.S)

    html = (
        r'figure[^>]*?kroki kroki-plantuml align-center" .*?>\s*?'
        r'<img alt="foo -&gt; bar ".*?/>.*?'
        r'<span class="caption-text">on <em>center</em></span>'
    )
    assert re.search(html, content, re.S)

    html = (
        r'<img[^>]*class="(?=[^"]*\bkroki\b)'
        r'(?=[^"]*\bkroki-ditaa\b)(?=[^"]*\balign-right\b)[^"]*"[^>]*/>'
    )
    assert re.search(html, content, re.S)
