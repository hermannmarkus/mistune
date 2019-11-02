import re

__all__ = ["plugin_table"]

TABLE_PATTERN = re.compile(
    r" {0,3}\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*"
)
NP_TABLE_PATTERN = re.compile(
    r" {0,3}(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*"
)
HEADER_SUB = re.compile(r"^ *| *\| *$")
HEADER_SPLIT = re.compile(r" *\| *")
ALIGN_SUB = re.compile(r" *|\| *$")
ALIGN_SPLIT = re.compile(r" *\| *")


def parse_table(self, m, state):
    thead, aligns = _process_table(m)

    text = re.sub(r"(?: *\| *)?\n$", "", m.group(3))
    rows = []
    for i, v in enumerate(text.split("\n")):
        v = re.sub(r"^ *\| *| *\| *$", "", v)
        rows.append(_process_row(v, aligns))

    children = [thead, {"type": "table_body", "children": rows}]
    return {"type": "table", "children": children}


def parse_nptable(self, m, state):
    thead, aligns = _process_table(m)

    text = re.sub(r"\n$", "", m.group(3))
    rows = []
    for i, v in enumerate(text.split("\n")):
        rows.append(_process_row(v, aligns))

    children = [thead, {"type": "table_body", "children": rows}]
    return {"type": "table", "children": children}


def _process_table(m):
    header = HEADER_SUB.sub("", m.group(1))
    headers = HEADER_SPLIT.split(header)
    align = ALIGN_SUB.sub("", m.group(2))
    aligns = ALIGN_SPLIT.split(align)

    cells = []
    for i, v in enumerate(aligns):
        if not v.strip():
            break
        if re.search(r"^ *-+: *$", v):
            aligns[i] = "right"
        elif re.search(r"^ *:-+: *$", v):
            aligns[i] = "center"
        elif re.search(r"^ *:-+ *$", v):
            aligns[i] = "left"
        else:
            aligns[i] = None

        cells.append(
            {"type": "table_cell", "text": headers[i], "params": (aligns[i], True)}
        )

    thead = {"type": "table_head", "children": cells}
    return thead, aligns


def _process_row(row, aligns):
    cells = []
    for i, s in enumerate(re.split(r" *(?<!\\)\| *", row)):
        cells.append(
            {
                "type": "table_cell",
                "text": re.sub(r"\\\|", "|", s),
                "params": (aligns[i], False),
            }
        )

    return {"type": "table_row", "children": cells}


def render_html_table(text):
    return "<table>\n" + text + "</table>\n"


def render_html_table_head(text):
    return "<thead>\n<tr>\n" + text + "</tr>\n</thead>\n"


def render_html_table_body(text):
    return "<tbody>\n" + text + "</tbody>\n"


def render_html_table_row(text):
    return "<tr>\n" + text + "</tr>\n"


def render_html_table_cell(text, align=None, is_head=False):
    if is_head:
        tag = "th"
    else:
        tag = "td"

    html = "  <" + tag
    if align:
        html += ' style="text-align:' + align + '"'

    return html + ">" + text + "</" + tag + ">\n"


def render_ast_table_cell(children, align=None, is_head=False):
    return {
        "type": "table_cell",
        "children": children,
        "align": align,
        "is_head": is_head,
    }


def plugin_table(md):
    md.block.register_rule("table", TABLE_PATTERN, parse_table)
    md.block.register_rule("nptable", NP_TABLE_PATTERN, parse_nptable)
    md.block.rules.append("table")
    md.block.rules.append("nptable")

    if md.renderer.NAME == "html":
        md.renderer.register("table", render_html_table)
        md.renderer.register("table_head", render_html_table_head)
        md.renderer.register("table_body", render_html_table_body)
        md.renderer.register("table_row", render_html_table_row)
        md.renderer.register("table_cell", render_html_table_cell)

    elif md.renderer.NAME == "ast":
        md.renderer.register("table_cell", render_ast_table_cell)
