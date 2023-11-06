from pathlib import Path
import sys

from marko import Markdown # https://marko-py.readthedocs.io/en/latest/
import marko
import marko.md_renderer
import marko.inline

def get_module_path() -> Path:
    path = Path(__file__)
    return path.parent

class TocGenerator:
    def __init__(
        self,
        prefix: str,
        max_level: int,
    ):
        self.prefix = prefix
        self.max_level = max_level

def header_to_link(header_text: str, prefix: str) -> str:
    suffix = header_text.strip().lower().translate(str.maketrans(' ','-', '<>.,;:#"\'*!§$%&/()=?^°\\#'))
    if prefix:
        return prefix + '#' + suffix
    else:
        return suffix

def walk(result: list[marko.block.BlockElement], node: marko.block.BlockElement, prefix: str, max_level: int):
    if  isinstance(node, marko.block.BlockElement):
        if node.children:
            for child in node.children:
                walk(result, child, prefix, max_level)

    if isinstance(node, marko.block.Heading) and node.level <= max_level:
        heading_text = node.children[0].children
        ref = header_to_link(heading_text, prefix)
        # print(f'add toc: [{heading_text}]({ref}, level: {node.level})')
        result.append((node.level, heading_text, ref, prefix))

def collect_headings(file_name: Path, prefix: str, max_level: int) -> list[marko.block.BlockElement]:
    md = Markdown(renderer=marko.md_renderer.MarkdownRenderer)
    with open(file_name) as f:
        doc = f.read()
    ast = md.parse(doc)
    toc_entries = []
    for child in ast.children:
        walk(toc_entries, child, prefix, max_level)
    return toc_entries

def generate_toc(out_file_name: str, toc_entries: list[marko.block.BlockElement]):
    print(f'Generating toc in {out_file_name}')
    with open(out_file_name, 'w') as f:
        counters = {}
        last_level = -1
        current_file = ''
        for toc in toc_entries:
            level = toc[0]
            if level < last_level:
                for i in range(level+1, len(counters)+1):
                    counters[i] = 0

            if counters.get(level):
                counters[level] = counters[level] + 1
            else:
                counters[level] = 1
            last_level = level
            num_str = ' '*(level-1)*2 + '* '
            for l in range(0, level):
                num_str += str(counters[l+1]) + '.'
            print(f'{num_str}[{toc[1]}]({toc[2]})', file=f)


def get_toc_entries(root_dir: str, working_dir:  Path, toc_entries: list[marko.block.BlockElement], max_level: int=3):
    all_files = sorted(Path(working_dir).rglob('[0-9][0-9]-*.md'))
    for file in all_files:
        # print(f' parsing file {file}')
        rel_path = file.relative_to(root_dir)
        toc = collect_headings(file, prefix=str(rel_path), max_level=max_level)
        toc_entries.extend(toc)

def traverse_spec_markdowns(root_dir: str, out_file_name: str):
    print(root_dir)
    toc_entries = []
    get_toc_entries(root_dir, root_dir, toc_entries)
    generate_toc(out_file_name, toc_entries)


def traverse_tree(root_dir: str, out_file_name: str):
    print(f'Generating TOC for tree in {root_dir}')
    toc_entries = []
    all_dirs = sorted((Path(root_dir) / 'doc').glob('[0-9][0-9]-*'))
    all_dirs = [ dir for dir in all_dirs if dir.is_dir() ] # filter directories
    toc_entries = []
    for dir in all_dirs:
        print(f' processing dir {dir}')
        _, chapter_name = dir.name.split('-')
        toc_entries.append((1, chapter_name.title(), f'docs/{dir.name}/README.md', None))
        get_toc_entries(root_dir, dir, toc_entries, 2)
        print(f' found {len(toc_entries)} entries')

    # Adjust all levels by one because we introduced a new top level
    for i, toc in enumerate(toc_entries):
        if toc[3]:  # keep root level entries, increment all others
            toc_entries[i] = (toc[0]+1, toc[1], toc[2], toc[3])
            # print(f'Tupel: {toc_entries[i]}')

    generate_toc(out_file_name, toc_entries)


def main():
    out_file_name = 'toc.md'
    root_dir = Path('.')

    if Path.exists(root_dir / 'doc'):
        # generate global TOC
        print('Generating global TOC')
        traverse_tree(root_dir, out_file_name)
    else:
        # generate TOC for all files (01...md, 02...md, ....)
        print('Generating chapter TOC')
        traverse_spec_markdowns(root_dir, out_file_name)


if __name__ == '__main__':
    main()
