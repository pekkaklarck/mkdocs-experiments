# Robot Framework Manual

This site is a playground for testing [Material for Mkdocs](https://squidfunk.github.io/mkdocs-material/)
features to be used with the [Robot Framework Manual](https://pekkaklarck.github.io/manual/latest/)
that is going to replace the old [Robot Framework User Guide](https://robotframework.org/robotframework/#user-guide).
To see the source code, click the edit button on right or go to the
https://github.com/pekkaklarck/mkdocs-experiments repository.

## Test or task?

Use the toggle in the header to choose. The next chapter changes based on that.

Should we use {test}? **{Test}s** we'll use!

## Emojis and icons

Lot of emojis and icons are [supported](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/):

- Emojis: :robot: :blue_book: :open_book:
- [Material Design](https://materialdesignicons.com/): :material-atv: :material-bug:
- [FontAwesome](https://fontawesome.com/search?m=free): :fontawesome-solid-handshake: :fontawesome-brands-github-alt:
- [Octicons](https://octicons.github.com/): :octicons-bug-16: :octicons-key-16:
- [Simple Icons](https://simpleicons.org/): :simple-git: :simple-robotframework:
- Custom icons: :robot-logo:

Being able to add custom icons is handy, but because Simple Icons
already has :simple-robotframework:, having also custom :robot-logo:
may not be useful.

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

<Keyword:> is a term in our [glossary](glossary.md). Term lookup is
case-insensitive and takes plural forms into account, so we can
refer to a term specified as `Library keyword` like <library keywords:>.

Glossary functionality is provided by the
[mkdocs-ezglossary](https://github.com/realtimeprojects/mkdocs-ezglossary) plugin.

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

## Versioning

Versioning has been set up using [mike](https://github.com/jimporter/mike) as
[Material for Mkdocs documentation](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/)
recommends and automated using [GitHub Actions](https://docs.github.com/en/actions).

### How it works

This is how versioning works for users viewing the docs and for developers writing them:

- When a normal commit is pushed, documentation for the `dev` version is generated
  automatically. New documentation overrides the existing `dev` docs.
- When a new stable release tag in format like `v0.1` or `v2.0.1` is pushed,
  documentation is generated for that release.
- Release documentation versions use only two components like `2.0`. If new releases
  in same series are created, they override existing documentation for that release.
  For example, if there is first release `2.0` (generated from tag `v2.0`) and then
  `2.0.1` is released (from tag `v2.0.1`), the shown `2.0` docs contain documentation
  for version `2.0.1`.
- Separate documentation is not generated for pre-releases like `2.1rc1`. It is
  possible to view the `dev` docs instead.
- `latest` version is an alias that always points to the docs of the latest release.
- Opening the documentation root automatically redirects to `latest`.
- It is possible to switch between versions using the widget in the page header.
- Viewing any other documentation version than latest causes a warning to be shown.

### Setting it up

This is how versioning has been set up:

- `mike` is listed in `requirements.txt`.
- Possible old docs from `gh-pages` root should be removed or moved to a dedicated
  directory. Running `mike delete --all --push` nukes everything, but you need to
  make sure your local `gh-pages` branch is in sync with the origin (and that there
  is nothing valuable that should not be removed).
- `mkdocs.yml` configuration:
  - Versioning is configured under `extra`.
  - `mike` itself is configured under `plugins`.
  - `site_url` should, for some reason, contain a trailing `/`.
  - `theme/custom_dir` sets up the directory containing template for outdated version
    warning. That directory is also listed under `watch`.
- `overrides/main.html` contains the aforementioned outdated version warning.
- `.github/workflows/dev-docs.yml` contains configuration for generating `dev` docs.
- `.github/workflows/release-docs.yml` contains configuration for generating release docs.
- The following commands needs to be run once to configure the default version.
  > mike set-default --push --allow-undefined latest
- To get social cards working when someone refers to the documentation root, copy
  related `og:xxx` (and `twitter:xxx`) meta tags from `latest/index.html` to
  `/index.html`. See this project's [index.html](https://github.com/pekkaklarck/mkdocs-experiments/blob/gh-pages/index.html)
  for an example.

!!! warning

    If workflows for generating `dev` and release docs are run at the same time, they
    may conflict when they try to push changes to `gh-pages`. They should be configured
    to wait for each others, but that didn't seem to be straightforward. Until that's
    done, care must be taken not to push release tags until `dev` doc generation has
    finished.
