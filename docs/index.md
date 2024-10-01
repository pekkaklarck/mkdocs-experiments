# Robot Framework Manual

The Manual is generated from Markdown sources at https://github.com/pekkaklarck/rf-uk-mkdocs/.

:blue_book: :open_book:

## Code snippets

Here's a simple Robot Framework example to get us started! :rocket:

```robotframework
*** Test Case ***
Example
    Log    Hello, world!
```

And here's another example using :fontawesome-brands-python::

```python
def example():
    print('Hello, world!')
```

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

Below we have an image. It uses link-like syntax as well. It also has a custom
anchor.

[](){#custom-anchor}
![Logo](styles/logo.png)

## Glossary

<Keyword:> is an important term for us. We'd also like to use it case-insensitively
like <keyword:>, but apparently that [doesn't work](https://github.com/realtimeprojects/mkdocs-ezglossary/issues/21).
<Library keyword:> is an important term as well.

## Notes

!!! note

    Content is only for testing purposes.

    ```python
    a = 1 + 2    # superfences!
    ```

!!! warning

    Did you read the above?

!!! quote "Is this the end?"

    No, this is just the beginning!
