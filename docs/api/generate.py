"""Generate API documentation.

API docs are part of the source code. This scripts generates references to
them as well as navigation.

Based on a `mkdocstrings` [recipe][] and a [script][] they use themselves.

[recipe]: https://mkdocstrings.github.io/recipes/#automatic-code-reference-pages
[script]: https://github.com/mkdocstrings/mkdocstrings/blob/main/scripts/gen_ref_nav.py
"""

from pathlib import Path

import mkdocs_gen_files


root = Path(__file__).parent.parent.parent
src = root / 'src'
nav = mkdocs_gen_files.Nav()

# Add a navigation entry to the static `docs/api/index.md`.
nav['API'] = 'index.md'


for path in sorted(src.rglob('*.py')):
    module = path.relative_to(src).with_suffix('').parts
    doc_path = path.relative_to(src).with_suffix('.md')
    full_doc_path = 'api' / doc_path

    if module[-1] == '__init__':
        module = module[:-1]
        doc_path = doc_path.with_name('index.md')
        full_doc_path = full_doc_path.with_name('index.md')
    elif module[-1][0] == '_':
        continue

    # Add navigation entry for each module with decoration.
    nav_parts = tuple(
        f'<code class="doc-symbol doc-symbol-nav doc-symbol-module"></code> {part}'
        for part in module
    )
    nav[nav_parts] = doc_path.as_posix()

    # Generate page with a reference.
    with mkdocs_gen_files.open(full_doc_path, 'w') as file:
        ident = '.'.join(module)
        file.write(f'---\ntitle: {ident}\n---\n\n::: {ident}')

    # Set correct edit path.
    mkdocs_gen_files.set_edit_path(full_doc_path, '..' / path.relative_to(root))


# Generate navigation file for `literal-nav`.
with mkdocs_gen_files.open('api/nav.md', 'w') as file:
    file.writelines(nav.build_literate_nav())
