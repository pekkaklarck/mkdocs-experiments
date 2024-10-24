"""Handle `{test}` markup as well as `*** Test Cases ***` headers.

The `{test}` markup is converted to this:

    <span class="test">test</span><span class="task">task</span>

Finding the pattern is case-insensitive, but the case is taken into account in
conversion. There can also be `s` at the end of the pattern. For example, `{Tests}`
is converted to this:

    <span class="test">Tests</span><span class="task">Tasks</span>

Test case headers have already been converted to HTML and look like this initially:

    <span class="gh">*** Test Cases ***</span>

They are converted to:

    <span class="gh test">*** Test Cases ***</span><span class="gh task">*** Tasks ***</span>

The idea is that CSS and/or Javascript hides elements that have either the `test`
class or the `task` class.
"""

import re


def on_page_content(html: str, page, config, files) -> str:
    return handle_test_cases_header(handle_test_marker(html))


def handle_test_marker(html: str) -> str:
    def handle_marker(match: re.Match) -> str:
        test = match.group(1)
        lower = [c.islower() for c in test]
        task = ''.join(c if low else c.upper() for c, low in zip('tasks', lower))
        return (f'<span class="test">{test}</span><span class="task">{task}</span>')

    return re.sub(r'(?i)(?<!`)\{(tests?)}', handle_marker, html)


def handle_test_cases_header(html: str) -> str:
    return html.replace('<span class="gh">*** Test Cases ***</span>',
                        '<span class="gh test">*** Test Cases ***</span>'
                        '<span class="gh task">*** Tasks ***</span>')
