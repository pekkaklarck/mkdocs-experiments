"""Python-Markdown extension for converting `{test}` markup to test or task.

In practice `{test}` is converted to this:

    <span><span class="robot-test">test</span><span class="robot-task">task</span></span>

Finding the pattern is case-insentive, but the case is taken into account in
conversion. For example, `{Test}` is converted to this:

    <span><span class="robot-test">Test</span><span class="robot-task">Task</span></span>

The idea is that external styles, possibly driven by Javascript, hide elements
that have either the `robot-test` class or the `robot-task` class.
"""

from xml.etree import ElementTree as ET

from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension


class TestOrTaskProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        test = m.group(1)
        root = ET.Element('span')
        root.extend([ET.Element('span', {'class': 'robot-test'}),
                     ET.Element('span', {'class': 'robot-task'})])
        root[0].text = test
        root[1].text = self.test_to_task(test)
        return root, m.start(), m.end()

    def test_to_task(self, test: str) -> str:
        """Convert 'test' to 'task' so that case is taken into account.

        For example, 'test' -> 'test' and 'Test' -> 'Task'.
        """
        lower = [c.islower() for c in test]
        return ''.join(c if low else c.upper() for c, low in zip('task', lower))


class TestOrTaskExtension(Extension):

    def extendMarkdown(self, md):
        processor = TestOrTaskProcessor(r'(?i)\{(test)\}', md)
        md.inlinePatterns.register(processor, 'test-or-task', 175)


def makeExtension(**kwargs):
    return TestOrTaskExtension(**kwargs)
