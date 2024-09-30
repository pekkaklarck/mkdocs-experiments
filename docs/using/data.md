# Input data

- [Input data syntax](#input-data-syntax)
- [Files and directories](#files-and-directories)
- [Input data sections](#input-data-sections)
- [Supported file formats](#supported-file-formats)
- [Rules for parsing the data](#rules-for-parsing-the-data)
- [Localization](#localization)

## Input data syntax

This section covers Robot Framework's overall input data syntax. Input data being 
- test data to support test cases
- initial imported data, separated from tasks script code, for Robotic Process Automation (RPA) script use


## Files and directories

The hierarchical structure for arranging test cases/RPA tasks is designed as follows:

- Test cases/RPA tasks are created in `suite files`.
- A test case file automatically creates a `test suite` containing
  the test cases/tasks in that file.
- An RPA task file automatically creates a `task suite`containing
  the tasks in that file.
- A directory containing test case/task files forms a higher-level 
  suite. Such a `suite directory` has suites created from test
  case/task files as its child suites.
- A suite directory can also contain other suite directories,
  and this hierarchical structure can be as deeply nested as needed.
- Suite directories can have a special `initialization file`
  configuring the created test suite.

In addition, there are:
- `Libraries` containing the lowest-level keywords.
- `Resource files` with `variables` and higher-level `user keywords`.
- `Variable files` to provide more flexible ways to create variables than resource files.

Test case files, RPA suite files, suite initialization files and resource files are all created using Robot Framework input data syntax, whereas Libraries and variable files are created using "real" programming languages (most often, Python).


## Input data sections

Robot Framework input data is defined in different sections, often also
called tables, listed below:

|   Section  |                 Used for                                          |
|:---        |:---                                                               |  
| Settings   | <p>1) Importing `test libraries`, `resource files` and `variable files`.<br />2) Defining metadata for `test suites`and `test cases`.</p>|
| Variables  | Defining `variables` that can be used elsewhere in the input data.  |
| Test Cases | `Creating test cases` from available keywords.                    |
| Tasks      | `Creating tasks` using available keywords. Single file can only contain either tests or tasks. |
| Keywords   | `Creating user keywords` from existing lower-level keywords       |
| Comments   | Additional comments or data. Ignored by Robot Framework.          |  

Different sections are recognized by their header row and the recommended header format is `*** Settings ***`. The header is case-insensitive, surrounding spaces are optional and the number of asterisk characters can
vary as long as there is at least one asterisk at the beginning. For example, also `*settings` would be recognized as a valid section header.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Settings ***
   Library    BuiltIn

   ** Variables ***
   ${variable_name_here}     variable_value_here
   ```
</details>  
<br />

The header row can also contain other data besides that of the actual section header.
The extra data must be separated from the section header using the data format dependent separator (typically two or more spaces). These extra headers are ignored at parsing time, but they can be used for documenting
purposes. This is especially useful when creating test cases using the
`data-driven style`.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Settings ***    EU language support ok, South America & Antarctica to be added Release 2.0
   ```
</details>  
<br />


> &#128226; _**NOTE:** Any data which may be entered before the first section is ignored._  
> &#128226; _**NOTE:** Section headers can be localized. See the Translations appendix for supported translations._

## Supported file formats

>**TODO:**  stylise each of the file extension mentions  

The most common approach to create Robot Framework input data is using the
`space separated format` where pieces of the input data, such as keywords
and their arguments, are separated from each other with two or more spaces.
An alternative is using the `pipe separated format` where the separator is
the pipe character surrounded with spaces (`|`).

Suite files typically use the `.robot` file extension, but which files are
parsed `can be configured`. `Resource files` can use the `.robot` file extension as well, but using the dedicated `.resource` file extension is
recommended. Files containing non-ASCII characters must be saved using the UTF-8 encoding.

>**HACK:** removed "and may be mandated in the future" from above!

Robot Framework supports also reStructuredText files so that normal
input data is `embedded into code blocks`. Only files with
the `.robot.rst` file extension are parsed by default. If you would
rather use just `.rst` or `.rest`file extensions, they need to be
configured separately.

>**TODO:**  how to configure this is missing above!

Input data can also be created in the `JSON format` that is targeted
more for tool developers than normal Robot Framework users. Only JSON files
with the custom `.rbt` file extension are parsed by default.

>**TODO:**  what does "tool developer" mean here above?

Earlier Robot Framework versions also supported input data in HTML and TSV formats. The TSV format still works if the input data is compatible with the `space separated format`, but the support for the HTML format has been removed altogether.

If you encounter such input data files, you need to convert them to the plain text format to be able to use them with Robot Framework. The easiest
way to do that is using the `Tidy` tool, but you must use the version included with Robot Framework 3.1 because newer Robot Framework versions do not understand the HTML format at all.

>**TODO:**  should we say why the HTML was removed here?

### Space separated format

When Robot Framework parses input data, it first splits the input data to lines and then those lines to tokens such as keywords and arguments. When using the space separated format, the separator between tokens is two or more spaces, or alternatively one or more tab characters. In addition to the normal ASCII space, any Unicode character considered to be a space (i.e. non-breaking space) works as a separator also. The number of spaces used as a separator can vary, as long as there are at least two, making it possible to nicely align the input data when it makes the input data easier to understand.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Settings ***
   Documentation     Example using the space separated format.
   Library           OperatingSystem

   *** Variables ***
   ${MESSAGE}        Hello, world!

   *** Test Cases ***
   My Test
       [Documentation]    Example test.
       Log    ${MESSAGE}
       My Keyword    ${CURDIR}

   Another Test
       Should Be Equal    ${MESSAGE}    Hello, world!

   *** Keywords ***
   My Keyword
       [Arguments]    ${path}
       Directory Should Exist    ${path}
   ```
</details>  
<br />

Because tabs and consecutive spaces are considered separators, they must
be escaped if they are needed in keyword arguments or elsewhere
in the actual input data. It is possible to use special escape sequences  such as `\t` for tab, `\xA0` for a non-breaking space or the `built-in variables` `${SPACE}` and `${EMPTY}`. Please See the `Escaping` section for more details.


> &#128226; _**TIP:** Although using two spaces as a separator is enough, it is recommended to use four spaces to make the separator easier to recognize.


### Pipe separated format

The biggest problem of the space separated format is that visually
separating keywords from arguments can be tricky. This is a problem
especially if keywords take a lot of arguments and/or arguments
contain spaces. In such cases the pipe delimited variant can
work better because it makes the separator more visibly clearer and obvious.

One file can contain both space separated and pipe separated lines.
Pipe separated lines are recognized by the mandatory leading pipe character,
but the pipe at the end of the line is optional. There must always be at
least one space or tab on both sides of the pipe except at the beginning and
at the end of the line. There is no need to align the pipes, but often this does make the input data easier to read.


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   | *** Settings ***   |
   | Documentation      | Example using the pipe separated format.
   | Library            | OperatingSystem

   | *** Variables ***  |
   | ${MESSAGE}         | Hello, world!

   | *** Test Cases *** |                 |               |
   | My Test            | [Documentation] | Example test. |
   |                    | Log             | ${MESSAGE}    |
   |                    | My Keyword      | ${CURDIR}     |
   | Another Test       | Should Be Equal | ${MESSAGE}    | Hello, world!

   | *** Keywords ***   |                        |         |
   | My Keyword         | [Arguments]            | ${path} |
   |                    | Directory Should Exist | ${path} |
   ```
</details>  
<br />

When using the pipe separated format, consecutive spaces or tabs inside
arguments do not need to be escaped. Similarly empty columns do not need
to be escaped except `if they are at the end of the libe`. Possible pipes surrounded by spaces in the actual input data must be escaped with a backslash, however.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   | *** Test Cases *** |                 |                 |                      |
   | Escaping Pipe      | ${file count} = | Execute Command | ls -1 *.txt \| wc -l |
   |                    | Should Be Equal | ${file count}   | 42                   |
   ```
</details>  
<br />

### reStructuredText format

`reStructuredText` (reST) is an easy-to-read plain text markup syntax that
is commonly used for documentation of Python projects including Python itself. reST documents are most often compiled to HTML, but other output formats are supported also. Using reST with Robot Framework allows you to mix richly formatted documents and input data in a concise text format that is easy to work with using simple text editors, diff tools, and source control systems.

> &#128226; _**NOTE:** Using reStructuredText_ files with Robot Framework requires the Python `docutils` module to be installed.

When using Robot Framework with reStructuredText files, normal input data is embedded into so called code blocks. In standard reST, code blocks are
marked using the `code` directive, but Robot Framework also supports 
`code-block` or `sourcecode` directives used by the `Sphinx` tool.

>**TODO:**  normal input data used throughout here, better terminology or an initial explaination of this term would be good.

>**TODO:**  this is the 1st time Sphinx is introduced. Explain what it is further.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    This text is outside code blocks and thus ignored.

    .. code:: robotframework

       *** Settings ***
       Documentation    Example using the reStructuredText format.
       Library          OperatingSystem

       *** Variables ***
       ${MESSAGE}       Hello, world!

       *** Test Cases ***
       My Test
           [Documentation]    Example test.
           Log    ${MESSAGE}
           My Keyword    ${CURDIR}

       Another Test
           Should Be Equal    ${MESSAGE}    Hello, world!

    Also this text is outside code blocks and ignored. Code blocks not
    containing input data are ignored as well.

    .. code:: robotframework

       # Both space and pipe separated formats are supported.

       | *** Keywords ***  |                        |         |
       | My Keyword        | [Arguments]            | ${path} |
       |                   | Directory Should Exist | ${path} |

    .. code:: python

       # This code block is ignored.
       def example():
           print('Hello, world!')
   ```
</details>  
<br />

Robot Framework supports reStructuredText files using `.robot.rst`,
`.rst` and `.rest` file extensions. To avoid parsing unrelated
reStructuredText files, only files with the `.robot.rst` file extension
are parsed by default when executing a directory. Parsing files with
other file extensions `can be enabled` by using either :option:`--parseinclude`
or :option:`--extension` option.

>**TODO:**  though not in the runner/execution section, add an example block here.

When Robot Framework parses reStructuredText files, errors below the level
`SEVERE` are ignored to avoid noise about possible non-standard directives
and other such markup. This may hide also real errors, but they can be seen
when processing files using reStructuredText tooling normally.

>**TODO:**  bit developer-y, need to link to the section on different output levels here. Re-word non-standard directives possibly too


### JSON format

Robot Framework also supports input data also in the `JSON` format. This format is designed typically more for tool developers than for regular Robot Framework users and it is not meant to be edited manually. Its most important use cases are:
- Transferring input data between processes and machines. A suite can be converted to JSON on one machine and recreated back to a suite on another machine (serialization).
- Saving a suite (possibly a nested suite), constructed from normal input data into a single JSON file which is faster to parse.
- As an alternative input data format for external tools generating tests or tasks.

#### Converting suite to JSON

A suite structure can be serialized into JSON by using the `TestSuite.to_json`
method. When used without arguments, it returns JSON data as a string, but
it also accepts a path or an open file where to write JSON data along with
configuration options related to JSON formatting:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   from robot.running import TestSuite


   # Create suite based on input data on the file system.
   suite = TestSuite.from_file_system('/path/to/data')

   # Get JSON data as a string.
   data = suite.to_json()

   # Save JSON data to a file with custom indentation.
   suite.to_json('data.rbt', indent=2)
   ```
</details>  
<br />

If you would rather work with Python data and then convert that to JSON
or some other format yourself, you can use `TestSuite.to_dict` instead. For more information, please see: 
- https://robot-framework.readthedocs.io/en/master/au_c/robot.running.html#robot.running.model.TestSuite.to_json
- https://robot-framework.readthedocs.io/en/master/au_c/robot.running.html#robot.running.model.TestSuite.to_dict

#### Creating suite from JSON

A suite can be constructed from JSON data using the `TestSuite.from_json` 
method. It works both with JSON strings and paths to JSON files:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   from robot.running import TestSuite


   # Create suite from JSON data in a file.
   suite = TestSuite.from_json('data.rbt')

   # Create suite from a JSON string.
   suite = TestSuite.from_json('{"name": "Suite", "tests": [{"name": "Test"}]}')

   # Execute suite. Notice that log and report needs to be created separately.
   suite.run(output='example.xml')
   ```
</details>  
<br />

If you have data as a Python dictionary, you can use `TestSuite.from_dict` instead. Regardless of how a suite is recreated, it exists only in memory and
original data files on the file system are not recreated.

As the above example demonstrates, the created suite can be executed using
the `TestSuite.run` method. It may, however, be easier to execute a JSON file
directly as explained in the following section.For more information, please see: 

- https://robot-framework.readthedocs.io/en/master/au_c/robot.running.html#robot.running.model.TestSuite.from_json
- https://robot-framework.readthedocs.io/en/master/au_c/robot.running.html#robot.running.model.TestSuite.from_dict
- https://robot-framework.readthedocs.io/en/master/au_c/robot.running.html#robot.running.model.TestSuite.run

>**TODO:**  Following section likely needs to point to a different chapter later  
>**TODO:**  Are these suite serialisations & running topics related to test-data? are they in the best place here?  
>**TODO:**  Examples of JSON produced maybe useful here

#### Executing JSON files

When executing tests or tasks using the `robot` command, JSON files with
the custom `.rbt` file extension are parsed automatically. This includes
running individual JSON files such as `robot tests.rbt` and running directories
containing `.rbt` files. If you would rather use the standard
`.json` file extension, you need to `configure which files are parsed`.

#### Adjusting suite source

Suite source in the data obtained from `TestSuite.to_json` and `TestSuite.to_dict` is in absolute format. If a suite is recreated later on a different machine, the source thus, may not match the directory structure on that machine. To avoid this situation, it is possible to use the `TestSuite.adjust_source` method to make the suite source relative before obtaining the data and to add a correct root directory after the suite is recreated:

>**TODO:**  Explain absolute/relative here or link to it's definition online

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   from robot.running import TestSuite


   # Create a suite, adjust source and convert to JSON.
   suite = TestSuite.from_file_system('/path/to/data')
   suite.adjust_source(relative_to='/path/to')
   suite.to_json('data.rbt')

   # Recreate suite elsewhere and adjust source accordingly.
   suite = TestSuite.from_json('data.rbt')
   suite.adjust_source(root='/new/path/to')
   ```
</details>  
<br />

For more information, please see:  
- https://robot-framework.readthedocs.io/en/master/au_c/robot.model.html#robot.model.testsuite.TestSuite.adjust_source

#### JSON structure

Imports, variables and keywords created in suite files are included in the
generated JSON along with tests and tasks. The exact JSON structure is documented at `running.json` `schema file`.

## Rules for parsing the data

### Ignored data

When Robot Framework parses input data files, it ignores:

- All data before the first `test data or task data section`.
- Data in the `Comments` section.
- All empty rows.
- All empty cells at the end of rows when using the `pipe separated format`.
- All single backslashes (`\`) when not used for `escaping`.
- All characters following the hash character (`#`), when it is the first
  character of a cell. This means that hash symbols can be used to enter
  comments in the input data.

When Robot Framework ignores some input data, this input data is not available in any resulting reports or logs and additionally, most tools used with Robot
Framework also ignore them. To add information that is visible in
Robot Framework outputs, place it to the documentation or other metadata of
test cases, tasks or suites, or log it with the `BuiltIn` keywords `Log` or
`Comment`.

### Escaping

The escape character in Robot Framework input data is the backslash
(`\`) and additionally `built-in variables` `${EMPTY}` and `${SPACE}`
can often be used for escaping also. Different escaping mechanisms are
discussed in the sections below.

#### Escaping special characters

The backslash character can be used to escape special characters so that their literal values are used.

| Character | Meaning                                                            | Examples                 |
|:---       |:---                                                                |:---                      |
| `\$`      |  Dollar sign, never starts a `scalar variable`.                    | `\${notvar}`             |
| `\@`      |  At sign, never starts a `list variable`_.                         | `\@{notvar}`             |
| `\&`      |  Ampersand, never starts a `dictionary variable`_.                 | `\&{notvar}`             |
| `\%`      |  Percent sign, never starts an `environment variable`_.            | `\%{notvar}`             |
| `\#`      |  Hash sign, never starts a comment_.                               | `\# not comment`         |
| `\=`      |  Equal sign, never part of `named argument syntax`_.               | `not\=named`             |
| `\|`      |  Pipe character, not a separator in the `pipe separated format`.   | `ls -1 *.txt \| wc -l`   |
| `\`       |  Backslash character, never escapes anything.                      | `c:\\temp, \\${var}`     |

#### Forming escape sequences

The backslash character also allows creating special escape sequences that are recognized as characters that would otherwise be difficult or impossible to create in the input data.

| Sequence        |               Meaning                 |          Examples          |
|:---             |:---                                   |:---                        |
| `\n`            | Newline character.                    | `first line\n2nd line`     |
| `\r`            | Carriage return character             | `text\rmore text`          |
| `\t`            | Tab character.                        | `text\tmore text`          |
| `\xhh`          | Character with hex value `hh`.        | `null byte: \x00, ä: \xE4` |
| `\uhhhh`        | Character with hex value `hhhh`.      | `snowman: \u2603`          |
| `\Uhhhhhhhh`    | Character with hex value `hhhhhhhh`.  | `love hotel: \U0001f3e9`   |

> &#128226; _**NOTE:** All strings created in the input data, including characters like `\x02`, are Unicode and must be explicitly converted to byte strings if needed. This can be done, for example, using `Convert To Bytes` or `Encode String To Bytes` keywords in `BuiltIn` and `String` libraries respectively, or with `value.encode('UTF-8')` or similar in Python code.

> &#128226; _**NOTE:** If invalid hexadecimal values are used with `\x`, `\u` or `\U` escape sequences, the end result is the original value without the backslash character. For example, `\xAX` (not hex) and `\U00110000` (too large value) result with `xAX` and `U00110000` respectively. This behavior may change in future versions of Robot Framework, however.

> &#128226; _**NOTE:** `Built-in variable` `${\n}` can be used if an operating system-dependent line terminator is needed (`\r\n` on Windows and `\n` elsewhere).

#### Handling empty values

When using the `space separated format`, the number of spaces used as
a separator can vary and thus empty values cannot be recognized unless they
are escaped. Empty cells can be escaped either with the backslash character
or with `built-in variable` `${EMPTY}`. The latter is typically recommended
as it is easier to understand.


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Using backslash
       Do Something    first arg    \
       Do Something    \            second arg

   Using ${EMPTY}
       Do Something    first arg    ${EMPTY}
       Do Something    ${EMPTY}     second arg
   ```
</details>  
<br />

When using the `pipe separated format`, empty values need to be escaped
only when they are at the end of the row:


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   | *** Test Cases *** |              |           |            |
   | Using backslash    | Do Something | first arg | \          |
   |                    | Do Something |           | second arg |
   |                    |              |           |            |
   | Using ${EMPTY}     | Do Something | first arg | ${EMPTY}   |
   |                    | Do Something |           | second arg |
   ```
</details>  
<br />

#### Handling spaces

Spaces, especially consecutive spaces, as part of arguments for keywords or otherwise, are problematic for two reasons:

- Two or more consecutive spaces is considered a separator when using the
  `space separated format`.
- Leading and trailing spaces are ignored when using the
  `pipe separated format`.

In these cases spaces need to be escaped. Similarly as when escaping empty
values, it is possible to do this either by using the backslash character or
by using the `built-in variable`_ `${SPACE}`.

| Escaping with backslash     |         Escaping with `${SPACE}`  |Notes                                 |
|:---                         |:---                               |:---                                  |
| `\\ leading space`          | `${SPACE}leading space`           |                                      |
| `trailing space \\`         | `trailing space${SPACE}`          |  Backslash must be after the space.  |
| `\\ \\`                     | `${SPACE}`                        |  Backslash needed on both sides.     |
| `consecutive \\ \\ spaces`  | `consecutive${SPACE * 3}spaces`   |  Using `extended variable syntax`.   |

As the above examples show, using the `${SPACE}` variable often makes the input data easier to understand. It is especially useful in combination with the `extended variable syntax` when more than one space is needed.

### Dividing data to several rows

If there is more data than readily fits a row, it is possible to split it 
and start continuing rows with an ellipsis (`...`). Ellipses can be indented
to match the indentation of the starting row and they must always be followed
by the normal input data separator.

In most places, split lines have exact same semantics as lines which are not
split. Exceptions to this rule are `suite`, `test`, `task` and `keyword`  documentation
as well as `suite metadata`. With these, split values are automatically
`joined together with the newline character` to ease creating multiline values.

The `...` syntax also allows splitting variables in the `Variable section`.
When long scalar variables (i.e. `${STRING}`) are split to multiple rows,
the final value is obtained by concatenating the rows together. The separator is
a space by default, but that can be changed by starting the value with
`SEPARATOR=<sep>`.

>**TODO:**  Add an example here

Splitting lines is illustrated in the following two examples containing
exactly the same input data with and and without splitting.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Settings ***
   Documentation      Here we have documentation for this suite.\nDocumentation is often quite long.\n\nIt can also contain multiple paragraphs.
   Default Tags       default tag 1    default tag 2    default tag 3    default tag 4    default tag 5

   *** Variables ***
   ${STRING}          This is a long string. It has multiple sentences. It does not have newlines.
   ${MULTILINE}       This is a long multiline string.\nThis is the second line.\nThis is the third and the last line.
   @{LIST}            this     list     is    quite    long     and    items in it can also be long
   &{DICT}            first=This value is pretty long.    second=This value is even longer. It has two sentences.

   *** Test Cases ***
   Example
       [Tags]    you    probably    do    not    have    this    many    tags    in    real    life
       Do X    first argument    second argument    third argument    fourth argument    fifth argument    sixth argument
       ${var} =    Get X    first argument passed to this keyword is pretty long    second argument passed to this keyword is long too
   ```
</details>  
<br />

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Settings ***
   Documentation      Here we have documentation for this suite.
   ...                Documentation is often quite long.
   ...
   ...                It can also contain multiple paragraphs.
   Default Tags       default tag 1    default tag 2    default tag 3
   ...                default tag 4    default tag 5

   *** Variables ***
   ${STRING}          This is a long string.
   ...                It has multiple sentences.
   ...                It does not have newlines.
   ${MULTILINE}       SEPARATOR=\n
   ...                This is a long multiline string.
   ...                This is the second line.
   ...                This is the third and the last line.
   @{LIST}            this     list     is      quite    long     and
   ...                items in it can also be long
   &{DICT}            first=This value is pretty long.
   ...                second=This value is even longer. It has two sentences.

   *** Test Cases ***
   Example
       [Tags]    you    probably    do    not    have    this    many
       ...       tags    in    real    life
       Do X    first argument    second argument    third argument
       ...    fourth argument    fifth argument    sixth argument
       ${var} =    Get X
       ...    first argument passed to this keyword is pretty long
       ...    second argument passed to this keyword is long too
   ```
</details>  
<br />

## Localization

Robot Framework localization efforts were started in Robot Framework 6.0
and allow translation of `section headers`, `settings`,
`Given/When/Then prefixes` used in Behavior Driven Development (BDD) and
`true and false strings` used in automatic boolean argument conversion.
The plan is to extend localization support in the future - for example,
to log and report outputs and possibly also to control structures.

This section explains how to `activate languages`, what `built-in languages`
are supported, how to create `custom language files` and how new translations
can be contributed.

### Enabling languages

#### Using command line option

The main mechanism to activate languages is specifying them from the command line
using the `--language` option. When enabling `built-in languages`,
it is possible to use either the language name, such as `Finnish`, or the language
code, such as `fi`. Both names and codes are case and space insensitive and any hyphen (`-`) is ignored. To enable multiple languages, the `--language` option needs to be used multiple times:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    robot --language Finnish testit.robot
    robot --language pt --language ptbr testes.robot
   ```
</details>  
<br />

>**TODO:**  Update examples throughout for clarity, remove abbreviations etc.

The same `--language` option is used when activating `custom language files`. With them the value can be either a path to the file or, if the file is in the `module search path`, the module name:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    robot --language Custom.py tests.robot
    robot --language MyLang tests.robot
   ```
</details>  
<br />

For backwards compatibility reasons, and to support partial translations,
English is always activated automatically. Future versions may allow disabling
it.

#### Pre-file configuration

It is also possible to enable languages directly in data files by having
a line `Language: <value>` (case-insensitive) before any of the section
headers. The value after the colon is interpreted the same way as with
the `--language` option:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    Language: Finnish

    *** Asetukset ***
    Dokumentaatio        Example using Finnish.

   ```
</details>  
<br />

If there is a need to enable multiple languages, the `Language:` line
can be repeated. These configuration lines cannot be in comments so code resembling 
`# Language: Finnish` or similar, has no effect.

Due to technical limitations, the per-file language configuration also affects 
parsing subsequent files as well as the whole execution. This behavior is likely to change in the future and *should not* be relied upon. If you use per-file configuration, use it with all files or enable languages globally with the `--language` option.

>**TODO:**   Example needed above

### Built-in languages

The following languages are supported out-of-the-box. Click the language name
to see further details of the actual translations:

- `Bulgarian (bg)`
- `Bosnian (bs)`
- `Czech (cs)`
- `German (de)`
- `Spanish (es)`
- `Finnish (fi)`
- `French (fr)`
- `Hindi (hi)`
- `Italian (it)`
- `Dutch (nl)`
- `Polish (pl)`
- `Portuguese (pt)`
- `Brazilian Portuguese (pt-BR)`
- `Romanian (ro)`
- `Russian (ru)`
- `Swedish (sv)`
- `Thai (th)`
- `Turkish (tr)`
- `Ukrainian (uk)`
- `Vietnamese (vi)`
- `Chinese Simplified (zh-CN)`
- `Chinese Traditional (zh-TW)`

>**TODO:** Add hyperlinks to each language above

All these translations have been provided by the fantastic Robot Framework
community. If a language you are interested in is not included, you can
consider` contributing` it!

### Custom language files

If a language you desire is not available as a built-in language, or you
want to create a completely custom language for a specific need, you can easily
create a custom language file. Language files are Python files which contain
one or more language definitions that are all loaded when the language file
is taken into use. Language definitions are created by extending the
`robot.api.Language` base class and overriding class attributes as needed:


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    from robot.api import Language


    class Example(Language):
        test_cases_header = 'Validations'
        tags_setting = 'Labels'
        given_prefixes = ['Assuming']
        true_strings = ['OK', '\N{THUMBS UP SIGN}']
   ```
</details>  
<br />


Assuming the above code would be in file `example.py`, a path to that
file or just the module name `example` could be used when the language file
is `activated`.

The above example adds only some of the possible language translations, which is fine
because English is automatically enabled anyway. Most values must be specified
as strings, but BDD prefixes and true/false strings allow more than one value
and must be given as lists. For more examples, see Robot Framework's internal
`languages` module which contains the `Language` class as well as all built-in
language definitions.
- https://github.com/robotframework/robotframework/blob/master/src/robot/conf/languages.py

### Contributing translations

If you want to add translation for a new language or enhance an existing language, please head
to `Crowdin` which we use for collaboration. For more details, see the separate `Localization` project and for questions and free discussion join the `#localization` channel on our `Slack` pletform.
- https://robotframework.crowdin.com
- https://github.com/MarketSquare/localization
