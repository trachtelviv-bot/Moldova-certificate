from docx import Document
from docx.shared import Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROWS_MAIN = 17
ROWS_SECOND = 5
COLS = 20


# =====================================================
# HELPERS
# =====================================================
def merge_cells(table, r1, c1, r2, c2):
    table.cell(r1, c1).merge(table.cell(r2, c2))


def add_field(run, field):
    fld_begin = OxmlElement('w:fldChar')
    fld_begin.set(qn('w:fldCharType'), 'begin')

    instr = OxmlElement('w:instrText')
    instr.text = field

    fld_end = OxmlElement('w:fldChar')
    fld_end.set(qn('w:fldCharType'), 'end')

    run._r.extend([fld_begin, instr, fld_end])


# =====================================================
# MAIN GENERATOR
# =====================================================
def generate_document(output_file: str):
    doc = Document()
    section = doc.sections[0]

    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1)
    section.header_distance = Cm(1)
    section.footer_distance = Cm(1)

    # ================== TABLE 1 ==================
    table1 = doc.add_table(rows=ROWS_MAIN, cols=COLS)
    table1.style = "Table Grid"
    table1.autofit = False

    MERGES_TABLE_1 = [
        (0, 0, 0, 19),
        (1, 0, 7, 0),
        (1, 10, 1, 17),
        (1, 18, 1, 19),
        (2, 10, 2, 19),
        (3, 10, 3, 19),
        (1, 1, 3, 9),
        (4, 1, 4, 9),
        (4, 10, 4, 19),
        (5, 1, 5, 4),
        (5, 5, 5, 9),
        (5, 10, 5, 14),
        (5, 15, 5, 19),
        (6, 1, 6, 9),
        (6, 10, 6, 19),
        (7, 1, 7, 9),
        (7, 10, 7, 19),
        (8, 0, 9, 9),
        (8, 10, 8, 19),
        (9, 10, 9, 19),
        (10, 0, 11, 9),
        (10, 10, 10, 19),
        (11, 10, 11, 19),
        (12, 0, 12, 9),
        (12, 10, 12, 19),
        (13, 0, 13, 9),
        (13, 10, 13, 19),
        (14, 0, 14, 19),
        (15, 0, 15, 9),
        (15, 10, 15, 19),
        (16, 0, 16, 19),
    ]

    for m in MERGES_TABLE_1:
        merge_cells(table1, *m)

    doc.add_page_break()

    # ================== TABLE 2 ==================
    table2 = doc.add_table(rows=ROWS_SECOND, cols=COLS)
    table2.style = "Table Grid"
    table2.autofit = False

    MERGES_TABLE_2 = [
        (0, 0, 4, 0),
        (0, 1, 0, 9),
        (0, 10, 0, 17),
        (0, 18, 0, 19),
        (1, 1, 1, 19),
        (2, 1, 2, 19),
        (3, 1, 3, 19),
        (4, 1, 4, 19),
    ]

    for m in MERGES_TABLE_2:
        merge_cells(table2, *m)

    doc.add_page_break()

    # ================== FOOTER ==================
    footer = section.footer
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = 1

    r = p.add_run("page ")
    add_field(r, "PAGE")
    r = p.add_run(" of ")
    add_field(r, "NUMPAGES")

    doc.save(output_file)

