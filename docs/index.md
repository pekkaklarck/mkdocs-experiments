# Robot Framework Manual

The Manual is generated from Markdown sources at https://github.com/pekkaklarck/rf-uk-mkdocs/.

:blue_book: :open_book:

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

Here's a link to [another page](using/data.md). And here's another to
link directly to a [section](using/data.md#json-format). Below we have an image.

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
