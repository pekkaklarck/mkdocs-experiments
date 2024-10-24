# Using Robot Framework

Introduction to the usage section. We have another references to the <keyword:>
term here. We are talking about **{tests}** because the test/task switch is in
*the {test} mode*.

```robotframework
*** Test Cases ***    # (1)!
Example
    Log    This is a {test}!    # (2)!
```

1. Header is set based on the test/task mode (now {test}).
2. This message changes as well.
