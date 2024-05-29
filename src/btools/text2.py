#!/usr/bin/env python3

import click
from easytrajh5.fs import run, run_with_output
from path import Path

__doc__ = "cli convert between md|html|docx|pug"


def convert_md_to_html(md, html):
    run(f"pandoc --from markdown --to html '{md}' -o '{html}'")
    txt = run_with_output(f"beautify {html}")
    open(html, 'w').write(txt)


def convert_md_to_docx(md, docx):
    run(f"pandoc --from markdown --to docx '{md}' -o '{docx}'")


def convert_docx_to_md(docx, md):
    run(f"pandoc --from docx --to markdown '{docx}' -o '{md}'")


def convert_html_to_pug(html, pug):
    run(f"html2pug < {html} > {pug}")


def convert_pug_to_html(pug, html):
    temp_pug = Path(pug).with_suffix('.temp.pug')
    pug.copy(temp_pug)
    temp_html = temp_pug.with_suffix(".html")
    temp_html.remove_p()
    run(f"pug {temp_pug}  ")
    txt = run_with_output(f"beautify {temp_html}")
    open(html, 'w').write(txt)


def convert_html_to_md(html, md):
    run(f"pandoc --from html --to markdown {html} -o {md}")


@click.command(no_args_is_help=True)
@click.argument('in_fname')
@click.argument('out_fname')
def main(in_fname, out_fname):
    """
    Interconvert text-based formats: md, pug, docx, html

    Wrapper for executables: pandoc, pug, html2pug, beautify
    """

    in_fname = Path(in_fname)
    out_fname = Path(out_fname)

    in_ext = in_fname.ext.lower()
    out_ext = out_fname.ext.lower()
    if (in_ext, out_ext) == (".md", ".pug"):
        temp_html_fname = in_fname.with_suffix(".temp.html")
        convert_md_to_html(in_fname, temp_html_fname)
        convert_html_to_pug(temp_html_fname, out_fname)
    elif (in_ext, out_ext) == (".pug", ".md"):
        temp_html_fname = in_fname.with_suffix(".temp.html")
        convert_pug_to_html(in_fname, temp_html_fname)
        convert_html_to_md(temp_html_fname, out_fname)
    elif (in_ext, out_ext) == (".pug", ".html"):
        convert_pug_to_html(in_fname, out_fname)
    elif (in_ext, out_ext) == (".md", ".html"):
        convert_md_to_html(in_fname, out_fname)
    elif (in_ext, out_ext) == (".md", ".docx"):
        convert_md_to_docx(in_fname, out_fname)
    elif (in_ext, out_ext) == (".docx", ".md"):
        convert_docx_to_md(in_fname, out_fname)
    else:
        print(f"Error: can't handle .ext: {in_fname} -> {out_fname}")

    print(f">>> Made {out_fname}")

if __name__ == '__main__':
    main()
