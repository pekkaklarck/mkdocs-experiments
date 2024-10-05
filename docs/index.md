# Robot Framework Manual

Click the edit button on right to see the source code.

:blue_book: :open_book: :smile:

Versioning ought to work now! :tada: Starting from v0.6, there should be
a warning when viewing older docs.

## Code snippets

Here's a simple Robot Framework example to get us started! :rocket:

```robotframework
*** Test Case ***
Example
    Log    Hello, world!    # (1)!
```

1. Code annotations work also with :robot: examples! :exploding_head:

Did you see the plus sign above? It's a *code annotation*. Click it!

And here's another example using :fontawesome-brands-python::

```python
def example():
    print('Hello, world!')
```

Above examples used fenced code blocks. Here's another Python example using
a simple indented code block:

    def example():
        print('Hello, world!')    # (1)!

1. Python is configured to be the default language for intended code blocks.

## Links

Standard Markdown syntax:

- Link to [section](#code-snippets) on the same page.
- Link to [another page](using/data.md).
- Link to a [section](using/data.md#json-format) on another page.
- Link to a [different site](http://robotframework).
- Link to a [custom target][].
- Link to a custom target having a [custom text][custom target].
- Link to [somewhere](#code-snippets "This is a title") with a title.

[custom target]: http://robotframework.org

Features provided by the [autorefs](https://mkdocstrings.github.io/autorefs/) plugin:

- Link to [header][code-snippets] on the same page.
- Link to a [section][json-format] on another page.
- Link to a [custom anchor][custom-anchor].

Features provided by the [MagicLink](https://facelessuser.github.io/pymdown-extensions/extensions/magiclink/) plugin:

- URIs like http://robotframework.org are converted to links.
- Repository URIs like https://github.com/facelessuser/pymdown-extensions are shortened.
- With a bit of configuration, issues like #42 and users like @pekkaklarck become links as well!

Below we have an image. It uses link-like syntax as well. It also has a custom
anchor.

[](){#custom-anchor}
![Logo](styles/logo.png)

## Glossary

It is convenient to refer to terms in the [glossary](glossary.md) like <keyword:>. Unfortunately
the term lookup is case-sensitive and doesn't handle plurals. <keyword:|Keyword>
and <library keyword:|library keywords> are alternatives.

## Tabs

=== "Tab 1"
    Tabs can be really useful for us!

    They are provided by the [pymdownx.tabbed](https://facelessuser.github.io/pymdown-extensions/extensions/tabbed) plugin.

=== "Tab 2"
    Markdown **content**.

    - list item a
    - list item b
    - :tada:

=== "Library"

    ```python
    def greet(name):
        print(f'Hello, {name}!')
    ```

=== "Test Case"

    ```robotframework
    *** Test Cases ***
    Example
        Greet    Robot
    ```

## Admonitions

!!! note

    All this content is only for experimenting purposes.

    ```python
    a = 1 + 2    # superfences!
    ```

!!! tip

    "Normal" admonitions are provided by the standard
    [admonition](https://python-markdown.github.io/extensions/admonition/) plugin.

??? quote "Collapsed!"

    Some initially hidden content here.

???+ success

    Collapsible admonitions can be initially expendad. They are provided by
    the [pymdownx.details](https://facelessuser.github.io/pymdown-extensions/extensions/details) plugin.
