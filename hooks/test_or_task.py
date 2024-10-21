"""Convert `{test}` to markup that can be rendered either as `test` or `task`.

In practice `{test}` is converted to this:

    <span class="test">test</span><span class="task">task</span>

Finding the pattern is case-insentive, but the case is taken into account in
conversion. For example, `{Test}` is converted to this:

    <span class="test">Test</span><span class="task">Task</span>

The idea is that external styles, possibly driven by Javascript, hide elements
that have either the `robot-test` class or the `robot-task` class.
"""

import re


def on_page_markdown(markdown, page, config, files):
    return re.sub(r'(?i)(?<!`)\{(test)}', test_and_task, markdown)


def test_and_task(match: re.Match) -> str:
    test = match.group(1)
    task = test_to_task(test)
    return (f'<span class="test">{test}</span><span class="task">{task}</span>')


def test_to_task(test: str) -> str:
    """Convert 'test' to 'task' so that case is taken into account.

    For example, 'test' -> 'test' and 'Test' -> 'Task'.
    """
    lower = [c.islower() for c in test]
    return ''.join(c if low else c.upper() for c, low in zip('task', lower))
