"""Edge cases for retrieve_structure when a doc has no h1."""

from moffee.builder import retrieve_structure
from moffee.compositor import composite


def test_retrieve_structure_doc_starting_with_h2():
    """A doc whose first page has an h2 but no h1 must not duplicate page ids.

    Regression test: retrieve_structure indexed headings[-1] via the
    still-unset last_h1_idx (-1), so the page id was recorded twice on
    the h2 entry (page_ids == [0, 0]).
    """
    doc = "## OnlyHeading\np0\n"
    pages = composite(doc)
    assert [(p.h1, p.h2, p.h3) for p in pages] == [(None, "OnlyHeading", None)]
    struct = retrieve_structure(pages)
    assert struct["headings"] == [
        {"level": 2, "content": "OnlyHeading", "page_ids": [0]}
    ]
    assert struct["page_meta"] == [{"h1": None, "h2": "OnlyHeading", "h3": None}]


def test_retrieve_structure_doc_with_no_headings():
    """A doc with no headings at all yields no headings and neutral meta."""
    doc = "just text\nmore text\n"
    pages = composite(doc)
    struct = retrieve_structure(pages)
    assert struct["headings"] == []
    assert all(
        meta == {"h1": None, "h2": None, "h3": None}
        for meta in struct["page_meta"]
    )
