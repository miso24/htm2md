from htm2md.tag import *


def create_tag_with_content(tag_kind: Tag, attrs: Dict[str, str], s: str) -> Tag:
    new_tag = tag_kind(attrs)
    new_tag.append_child(Content(s))
    return new_tag


def test_a():
    a = create_tag_with_content(A, {"href": "https://example.com"}, "example")
    assert a.to_str() == "[example](https://example.com)"


def test_b():
    b = create_tag_with_content(B, {}, "test")
    assert b.to_str() == "**test**"


def test_blockquote_single_line():
    blkquote = create_tag_with_content(Blockquote, {}, "test")
    assert blkquote.to_str() == "> test\n"


def test_blockquote_multi_line():
    blkquote = Blockquote({})
    blkquote.append_child(Content("test\n"))
    blkquote.append_child(Content("hoge\n"))
    blkquote.append_child(Content("fuga\n"))
    assert blkquote.to_str() == "> test\n> \n> hoge\n> \n> fuga\n"


def test_nested_blockquote():
    bq1, bq2 = Blockquote({}), Blockquote({})
    bq1.append_child(Content("parent 1\n"))
    bq2.append_child(Content("child\n"))
    bq1.append_child(bq2)
    bq1.append_child(Content("parent 2\n"))
    print(bq1.to_str())
    assert bq1.to_str() == "> parent 1\n> \n> > child\n> \n> parent 2\n"


def test_blockquote_ul():
    bq = Blockquote({})
    ul = Ul({})
    ul.append_child(create_tag_with_content(Li, {}, "hoge"))
    ul.append_child(create_tag_with_content(Li, {}, "fuga"))
    bq.append_child(ul)
    assert bq.to_str() == ">   - hoge\n>   - fuga\n"


def test_code_single_line():
    code = Code({})
    code.append_child(Content("test"))
    assert code.to_str() == "`test`"


def test_code_multi_line():
    code = Code({})
    code.append_child(Content("test\n"))
    code.append_child(Content("hoge\n"))
    code.append_child(Content("fuga\n"))
    assert code.to_str() == """```\ntest\nhoge\nfuga\n```\n"""


def test_code_lang():
    code = Code({"class": "lang-python"})
    code.append_child(Content("def hello():\n"))
    code.append_child(Content('    print("Hello,World!")\n'))
    assert (
        code.to_str()
        == """```python\ndef hello():\n    print(\"Hello,World!\")\n```\n"""
    )


def test_del():
    _del = create_tag_with_content(Del, {}, "test")
    assert _del.to_str() == "~~test~~"


def test_em():
    em = create_tag_with_content(Em, {}, "emphasis")
    assert em.to_str() == "*emphasis*"


def test_hr():
    assert Hr({}).to_str() == "---\n"


def test_ul():
    ul_tag = Ul({})
    li_tags = [
        create_tag_with_content(Li, {}, "hoge"),
        create_tag_with_content(Li, {}, "fuga"),
    ]

    ul_tag.append_child(li_tags[0])
    ul_tag.append_child(li_tags[1])
    assert ul_tag.to_str() == "  - hoge\n  - fuga\n"


def test_ol():
    ol_tag = Ol({})
    li_tags = [
        create_tag_with_content(Li, {}, "hoge"),
        create_tag_with_content(Li, {}, "fuga"),
    ]

    ol_tag.append_child(li_tags[0])
    ol_tag.append_child(li_tags[1])
    assert ol_tag.to_str() == "  1. hoge\n  1. fuga\n"


def test_nested_tags():
    ul1, ul2 = Ul({}), Ul({})
    ol = Ol({})

    ul2.append_child(create_tag_with_content(Li, {}, "hoge"))
    ul2.append_child(create_tag_with_content(Li, {}, "fuga"))

    ol.append_child(create_tag_with_content(Li, {}, "hoge"))
    ol.append_child(ul2)
    ol.append_child(create_tag_with_content(Li, {}, "fuga"))

    ul1.append_child(create_tag_with_content(Li, {}, "hoge"))
    ul1.append_child(ol)
    ul1.append_child(create_tag_with_content(Li, {}, "fuga"))

    expected = (
        "  - hoge\n    1. hoge\n      - hoge\n      - fuga\n    1. fuga\n  - fuga\n"
    )
    assert ul1.to_str() == expected


def test_p():
    p = create_tag_with_content(P, {}, "paragraph")
    assert p.to_str() == "paragraph\n"


def test_strong():
    strong = create_tag_with_content(Strong, {}, "strong")
    assert strong.to_str() == "**strong**"


def test_simple_table():
    table = Table({})
    head_tr, body_tr = Tr({}), Tr({})

    th = create_tag_with_content(Th, {}, "head")
    td = create_tag_with_content(Td, {}, "data")

    head_tr.append_child(th)
    body_tr.append_child(td)
    table.append_child(head_tr)
    table.append_child(body_tr)

    print(table.head)
    print(table.body)
    assert table.to_str() == "|head|\n|---|\n|data|\n"


def test_complex_table():
    table = Table({})
    caption = Caption({})
    thead, tbody = Thead({}), Tbody({})
    head_tr, body_tr = Tr({}), Tr({})

    th1 = create_tag_with_content(Th, {}, "head1")
    th2 = create_tag_with_content(Th, {}, "head2")

    td1 = create_tag_with_content(Th, {}, "data1")
    td2 = create_tag_with_content(Th, {}, "data2")

    # table <- caption
    caption.append_child(Content("caption"))
    table.append_child(caption)
    # head_tr <- th, body_tr <- td
    head_tr.append_child(th1)
    head_tr.append_child(th2)
    body_tr.append_child(td1)
    body_tr.append_child(td2)
    # thead <- tr, tbody <- tr
    thead.append_child(head_tr)
    tbody.append_child(body_tr)
    # table <- thead, tbody
    table.append_child(thead)
    table.append_child(tbody)

    assert table.to_str() == "caption\n|head1|head2|\n|---|---|\n|data1|data2|\n"
