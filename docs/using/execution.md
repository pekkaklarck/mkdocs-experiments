# Executing test cases and tasks

- [Starting test execution](#starting-test-execution)
- [Test execution](#test-execution)
- [Task execution](#task-execution)
- [Post-processing outputs](#post-processing-outputs)
- [Configuring execution](#configuring-execution)
- [Output files](#)
- [Basic usage](#)

## Basic usage

>**TODO:**  Some form of info box here?

Robot Framework test cases and RPA tasks are executed from the command line. The default resulting files generated are 
- `XML format output`
- `HTML report`
- `log file` 

Post-execution, output files can be combined and otherwise post-processed with the Rebot tool.

### Starting test execution
***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    robot [options] data
    python -m robot [options] data
    python path/to/robot/ [options] data

   ```
</details>  
<br />
Execution is possible through multiple ways:

- `robot command:` typically using the robot command  created as part of installation.
- `robot module via Python interpreter:` execution of the installed robot module using the selected Python interpreter (this is especially convenient if Robot Framework has been installed under multiple Python versions). 
- `python:` using Python if you know where the installed robot directory exists, it can be executed using Python as well.

Regardless of execution approach, the path(s) to the input data to be executed are provided as an argument after the command. Additionally, different command line options can be used to alter the test execution or generated outputs in many ways.

#### Specifying input data to be executed
Robot Framework test cases and/or RPA tasks are created in files and directories and they are executed by providing the path to the file or directory in question, to the selected runner script. The path can be absolute or, more commonly, relative to the directory where tasks are executed from. The given file or directory creates the top-level suite, which, by default, gets its name from the file or directory name. Different execution possibilities are illustrated in the examples below. Note that in these examples, as well as in other examples in this section, only the robot script is used, but other execution approaches could be used similarly.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    robot tests.robot
    robot path/to/my_tests/
    robot c:\robot\tests.robot
   ```
</details>  
<br />

> &#128226; _**NOTE:** When executing a directory, all files and directories starting with a dot (.) or an underscore (_) are ignored and by default, only files with the .robot extension are executed. See the Selecting files to parse section for more details.

It is also possible to give paths to several test case files or directories at once, separated with spaces. In this case, Robot Framework creates the top-level test suite automatically, and the specified files and directories become its child suites. The name of the created suite originates from child suite names by concatenating them togethser with an ampersand (&) and spaces. For example, the name of the top-level suite in the first example below is My Tests & Your Tests. These automatically created names are often quite long and complicated. In most cases, it is thus better to use the --name option for overriding it, as in the second example below:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    robot my_tests.robot your_tests.robot
    robot --name Example path/to/tests/pattern_*.robot
   ```
</details>  
<br />
Starting from Robot Framework 6.1, it is also possible to define a test suite initialisation file for the automatically created top-level suite. The path to the init file is given similarly to the test case files:
***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    robot __init__.robot my_tests.robot other_tests.robot
   ```
</details>  
<br />

### Using command line options
Robot Framework provides a number of command line options which can be used to control how test cases and RPA tasks are executed and what outputs are generated. This section explains the option syntax, and which options actually exist. How they can be used is discussed elsewhere in this chapter.

#### Using options
When options are used, they must always be given between the runner script and the data sources. For example:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot -L debug my_tests.robot
   robot --include smoke --variable HOST:10.0.0.42 path/to/tests/
   ```
</details>  
<br />

#### Short and long options
Options always have a long name, such as --name and the most frequently needed options also have a short name, such as -N. In addition to that, long options can be shortened as long as they are unique. For example, --logle DEBUG works, while --lo log.html does not, because the former matches only --loglevel, but the latter matches several options. Short and shortened options are practical when executing test cases manually, but long options are recommended in start-up scripts, because they are easier to understand.

The long option names are case-insensitive and hyphen-insensitive, which facilitates writing option names in an easy-to-read format. For example, --SuiteStatLevel and --suite-stat-level are equivalent to, but easier to read than, --suitestatlevel.

> &#128226; _**NOTE:** Long options being hyphen-insensitive is new in Robot Framework 6.1.

#### Setting option values
Most of the options require a value, which is given after the option name. Both short and long options accept the value separated from the option name with a space, as in --include tag or -i tag. With long options, the separator can also be the equals sign, for example --include=tag, and with short options the separator can be omitted, as in -itag.

Some options can be specified several times. For example, --variable VAR1:value --variable VAR2:another sets two variables. If the options that take only one value are used several times, the value provided last is effective.

#### Disabling options accepting no values
Options accepting no values can be disabled by using the same option again with no prefix added or dropped. The last option has precedence regardless of how many times options are used. For example, --dryrun --dryrun --nodryrun --nostatusrc --statusrc would not activate the dry-run mode and would return normal status rc.

#### Simple patterns
Many command line options take arguments as simple patterns. These glob-like patterns are matched according to the following rules:

- `*` matches any string, even an empty string.
- `?` matches any single character.
- `[abc]` matches one character in the bracket.
- `[!abc]` matches one character not in the bracket.
- `[a-z]` matches one character from the range in the bracket.
- `[!a-z]` matches one character not from the range in the bracket.

Unlike with glob patterns normally, path separator characters / and \ and the newline character \n are matches by the above wildcards.
Unless noted otherwise, pattern matching is case, space, and underscore insensitive.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   --test Example*        # Matches tests with name starting 'Example'.
   --test Example[1-2]    # Matches tests 'Example1' and 'Example2'.
   --include f??          # Matches tests with a tag that starts with 'f' is three characters long.
   ```
</details>  
<br />

All matches in the above examples are case, space and underscore insensitive. For example, the second example would also match test named example 1.

If the matched text happens to contain some of the wildcard characters and they need to be matched literally, it is possible to do that by using the [...] syntax. The pattern [*] matches the literal * character, [?] matches ?, and [[] matches [. Lone [ and ] do not need to be escaped.

> &#128226; _**NOTE:** Support for brackets such as [abc] and [!a-z] is new in Robot Framework 3.1.

#### Tag patterns
Most tag related options accept arguments as tag patterns. They support same wildcards as simple patterns (e.g. examp??, ex*le), but they also support AND, OR and NOT operators explained below. These operators can be used for combining two or more individual tags or patterns together.

##### AND or &
The whole pattern matches if all individual patterns match. AND and & are equivalent:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include fooANDbar     # Matches tests containing tags 'foo' and 'bar'.
   --exclude xx&yy&zz      # Matches tests containing tags 'xx', 'yy', and 'zz'.
   ```
</details>  
<br />

##### OR
The whole pattern matches if any individual pattern matches:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include fooORbar      # Matches tests containing either tag 'foo' or tag 'bar'.
   --exclude xxORyyORzz    # Matches tests containing any of tags 'xx', 'yy', or 'zz'.
   ```
</details>  
<br />

##### NOT
The whole pattern matches if the pattern on the left side matches but the one on the right side does not. If used multiple times, none of the patterns after the first NOT must not match:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include fooNOTbar     # Matches tests containing tag 'foo' but not tag 'bar'.
   --exclude xxNOTyyNOTzz  # Matches tests containing tag 'xx' but not tag 'yy' or tag 'zz'.
   ```
</details>  
<br />

The pattern can also start with NOT in which case the pattern matches if the pattern after NOT does not match:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include NOTfoo        # Matches tests not containing tag 'foo'
   --include NOTfooANDbar  # Matches tests not containing tags 'foo' and 'bar'
   ```
</details>  
<br />

The above operators can also be used together. The operator precedence, from highest to lowest, is AND, OR and NOT:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include xANDyORz      # Matches tests containing either tags 'x' and 'y', or tag 'z'.
   --include xORyNOTz      # Matches tests containing either tag 'x' or 'y', but not tag 'z'.
   --include xNOTyANDz     # Matches tests containing tag 'x', but not tags 'y' and 'z'.
   ```
</details>  
<br />

Although tag matching itself is case-insensitive, all operators are case-sensitive and must be written with upper case letters. If tags themselves happen to contain upper case AND, OR or NOT, they need to specified using lower case letters to avoid accidental operator usage:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include port          # Matches tests containing tag 'port', case-insensitively
   --include PORT          # Matches tests containing tag 'P' or 'T', case-insensitively
   --exclude handoverORportNOTnotification
   ```
</details>  
<br />

#### ROBOT_OPTIONS and REBOT_OPTIONS environment variables
Environment variables ROBOT_OPTIONS and REBOT_OPTIONS can be used to specify default options for execution and result post-processing, respectively. The options and their values must be defined as a space separated list and they are placed in front of any explicit options on the command line. The main use case for these environment variables is setting global default values for certain options to avoid the need to repeat them every time tests/tasks are run or Rebot is used.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   export ROBOT_OPTIONS="--outputdir results --tagdoc 'mytag:Example doc with spaces'"
   robot tests.robot
   export REBOT_OPTIONS="--reportbackground blue:red:yellow"
   rebot --name example output.xml
   ```
</details>  
<br />

### Test results
#### Command line output
The most visible output from test execution is the output displayed in the command line. All executed suites and test cases/RPA tasks, as well as their statuses, are shown there in real time. The example below shows the output from executing a simple test suite with only two test cases:

>**TODO:**  Alter below with escape sequence. CSS? image?


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
\==============================================================================

\Example test suite

\==============================================================================

\First test :: Possible test documentation                             | PASS |

\------------------------------------------------------------------------------

\Second test                                                           | FAIL |

\Error message is displayed here

\==============================================================================

\Example test suite                                                    | FAIL |

\2 tests, 1 passed, 1 failed

\==============================================================================

\Output:  /path/to/output.xml

\Report:  /path/to/report.html

\Log:     /path/to/log.html
   ```
</details>  
<br />

There is also a notification on the console whenever a top-level keyword in a test case/RPA task ends. A green dot is used if a keyword passes and a red F if it fails. These markers are written to the end of line and they are overwritten by the execution status when the execution itself ends. Writing the markers is disabled if console output is redirected to a file.

#### Generated output files
The command line output is very limited and separate output files are usually needed for investigating the execution results. As the example above shows, three output files are generated by default. The first one is in XML format and contains all the information about test execution. The second is a higher-level report and the third is a more detailed log file. These files and other possible output files are discussed in more detail in the section Different output files.

#### Return codes
Runner scripts communicate the overall execution status to the system running them using return codes. When the execution starts successfully and no tests/RPA tasks fail, the return code is zero. All possible return codes are explained in the table below.

*Possible return codes*
|   Return code |                 Explanation                       |
|:---           |:---                                               |  
|   0	        |   All tests passed.                               |   
|   1-249	    |   Returned number of tests failed.                |   
|   250     	|   250 or more failures.                           |   
|   251	        |   Help or version information printed.            |   
|   252	        |   Invalid input data or command line options.     |   
|   253	        |   Test execution stopped by user.                 |   
|   255	        |   Unexpected internal error.                      |   

Return codes should always be easily available after the execution, which makes it easy to automatically determine the overall execution status. For example, in a bash shell the return code is in special variable $?, and in Windows it is in %ERRORLEVEL% variable. If you use another external tool for running tests, consult its documentation for how to retrieve the return code.

The return code can be set to 0 even if there are failures using the --NoStatusRC command line option. This might be useful, for example, in continuous integration servers where post-processing of results is needed before the overall status of execution can be determined.

> &#128226; _**NOTE:** Same return codes are also used with Rebot.

#### Errors and warnings during execution
During the test execution there can be unexpected problems such as failing to import a library or a resource file, or a keyword being deprecated, for example. Depending on the severity, such problems are categorized as errors or warnings and they are written into the console (using the standard error stream), shown on a separate Test/Task Execution Errors section in log files and also written into Robot Framework's own system log. Normally these errors and warnings are generated by Robot Framework itself, but libraries can also log errors and warnings. The example below illustrates how errors and warnings appear in the log file.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   20090322 19:58:42.528	ERROR	Error in file '/home/robot/tests.robot' in table 'Setting' in element on row 2: Resource file 'resource.robot' does not exist
   20090322 19:58:43.931	WARN	Keyword 'SomeLibrary.Example Keyword' is deprecated. Use keyword `Other Keyword` instead.
   
   ```
</details>  
<br />

### Argument files
Argument files allow placing all or some command line options and arguments into an external file where they will be read. This avoids the problems with characters which are problematic on the command line. If many options or arguments are needed, argument files also prevent the command which is used on the command line, growing too long.

Argument files are taken into use with --argumentfile (-A) option along with possible other command line options.

> &#128226; _**NOTE:** Unlike other long command line options, --argumentfile cannot be given in shortened format like --argumentf.

#### Argument file syntax
Argument files can contain both command line options and paths to the input data, one option or data source per line. Both short and long options are supported, but the latter are recommended because they are easier to understand. Argument files can contain any characters without escaping, but spaces in the beginning and end of lines are ignored. Additionally, empty lines and lines starting with a hash mark (#) are ignored:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --doc This is an example (where "special characters" are ok!)
   --metadata X:Value with spaces
    --variable VAR:Hello, world!
   # This is a comment
   path/to/my/tests
   ```
</details>  
<br />

In the above example the separator between options and their values is a single space. It is possible to use either an equal sign (=) or any number of spaces. As an example, the following three lines are identical:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --name An Example
   --name=An Example
   --name       An Example
   ```
</details>  
<br />

If argument files contain non-ASCII characters, they must be saved using UTF-8 encoding.

#### Using argument files
Argument files can be used either alone so that they contain all the options and paths to the input data, or along with other options and paths. When an argument file is used with other arguments, its contents are placed into the original list of arguments to the same place where the argument file option was. This means that options in argument files can override options before it, and its options can be overridden by options after it. It is possible to use --argumentfile option multiple times or even recursively:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --argumentfile all_arguments.robot
   robot --name Example --argumentfile other_options_and_paths.robot
   robot --argumentfile default_options.txt --name Example my_tests.robot
   robot -A first.txt -A second.txt -A third.txt tests.robot
   ```
</details>  
<br />

#### Reading argument files from standard input
A special argument file name STDIN can be used to read arguments from the standard input stream instead of a file. This can be useful when generating arguments with a script:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   generate_arguments.sh | robot --argumentfile STDIN
   generate_arguments.sh | robot --name Example --argumentfile STDIN tests.robot
   ```
</details>  
<br />

### Getting help and version information
Both when executing test cases and when post-processing outputs, it is possible to get command line help with the option --help (-h). These help texts have a short general overview and briefly explain the available command line options.

All runner scripts also support getting the version information with the option --version. This information also contains both the Python version and the platform type:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   $ robot --version
   Robot Framework 7.0 (Python 3.12.1 on darwin)
   
   C:\>rebot --version
   Rebot 6.1.1 (Python 3.11.0 on win32)
   ```
</details>  
<br />

### Creating start-up scripts
Test cases/RPA tasks are often executed automatically by a continuous integration system or some other automated mechanism. In such cases, there is a need to have a script for starting the execution and possibly also for post-processing outputs somehow. Similar scripts are also useful when executing manually, especially if a large number of command line options are needed or setting up the test environment is complicated.

In UNIX-like environments, shell scripts provide a simple but powerful mechanism for creating custom start-up scripts. Windows batch files can also be used, but they are more limited and often also more complicated. A platform-independent alternative is using Python or some other high-level programming language. Regardless of the language, it is recommended that long option names are used, because they are easier to understand than the short names.

#### Shell script example
In this example, the same web tests/tasks in the login directory are executed with different browsers and the results are combined afterwards using Rebot. The script also accepts command line options itself and simply forwards them to the robot command using the handy $* variable:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   #!/bin/bash
   robot --name Firefox --variable BROWSER:Firefox --output out/fx.xml --log none --report none $* login
   robot --name IE --variable BROWSER:IE --output out/ie.xml --log none --report none  $* login
   rebot --name Login --outputdir out --output login.xml out/fx.xml out/ie.xml
   ```
</details>  
<br />

#### Batch file example
Implementing the above shell script example using batch files is not very complicated either. Notice that arguments to batch files can be forwarded to executed commands using %*:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   @echo off
   robot --name Firefox --variable BROWSER:Firefox --output out\fx.xml --log none --report none %* login
   robot --name IE --variable BROWSER:IE --log none --output out\ie.xml --report none %* login
   rebot --name Login --outputdir out --output login.xml out\fx.xml out\ie.xml
   ```
</details>  
<br />

> &#128226; _**NOTE:**Prior to Robot Framework 3.1 robot and rebot commands were implemented as batch files on Windows and using them in another batch file required prefixing the whole command with call.

#### Python example
When start-up scripts get more complicated, implementing them using shell scripts or batch files is not so convenient. This is especially true if both variants are needed and same logic needs to be implemented twice. In such situations it is often better to switch to Python. It is possible to execute Robot Framework from Python using the subprocess module, but often using Robot Framework's own programmatic API is more convenient. The easiest APIs to use are robot.run_cli and robot.rebot_cli that accept same command line arguments than the robot and rebot commands.

The following example implements the same logic as the earlier shell script and batch file examples. In Python, arguments to the script itself are available in sys.argv:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   #!/usr/bin/env python
   import sys
   from robot import run_cli, rebot_cli
   
   common = ['--log', 'none', '--report', 'none'] + sys.argv[1:] + ['login']
   run_cli(['--name', 'Firefox', '--variable', 'BROWSER:Firefox', '--output', 'out/fx.xml'] + common, exit=False)
   run_cli(['--name', 'IE', '--variable', 'BROWSER:IE', '--output', 'out/ie.xml'] + common, exit=False)
   rebot_cli(['--name', 'Login', '--outputdir', 'out', 'out/fx.xml', 'out/ie.xml'])
   ```
</details>  
<br />

> &#128226; _**NOTE:** exit=False is needed because by default, run_cli exits to system with the correct return code. rebot_cli does that also, but in the above example that is fine.

### Making *.robot files executable
On UNIX-like operating systems it is possible to make *.robot files executable by giving them execution permission and adding a shebang like in this example:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   #!/usr/bin/env robot
   
   *** Test Cases ***
   Example
          Log to console    Executing!
   
   ```
</details>  
<br />

If the above content would be in a file example.robot and that file would be executable, it could be executed from the command line as  below. Starting from Robot Framework 3.2, individually executed files can have any extension, or no extension at all, so the same would work also if the file would be named just example.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   ./example.robot
   ```
</details>  
<br />

This trick does not work when executing a directory but can be useful when executing a single file. It is probably more often useful when automating tasks than when automating tests.

### Debugging problems
A test case can fail because the system under test/RPA system does not work correctly, in which case the test/task has found a bug, or because the test/task itself is buggy. The error message explaining the failure is shown on the command line output and in the report file, and sometimes the error message alone is enough to pinpoint the problem. More often that not, however, log files are needed because they also contain other log messages and they show which keyword actually failed.

When a failure is caused by the application, the error message and log messages ought to be enough to understand what caused it. If that is not the case, the executed library does not provide enough information and needs to be enhanced. In this situation running the same test/task manually, if possible, may also reveal more information about the issue.

Failures caused by test cases/RPA tasks themselves or by keywords they use can sometimes be difficult to debug. If the error message, for example, tells that a keyword is used with wrong number of arguments fixing the problem is obviously easy, but if a keyword is missing or fails in unexpected way finding the root cause can be harder. The first place to look for more information is the execution errors section in the log file. For example, an error about a failed library import may well explain why a test/task has failed due to a missing keyword.

If the log file does not provide enough information by default, it is possible to execute tests with a lower log level. For example tracebacks showing where in the code the failure occurred are logged using the DEBUG level, and this information is invaluable when the problem is in an individual library keyword.

Logged tracebacks do not contain information about methods inside Robot Framework itself. If you suspect an error is caused by a bug in the framework, you can enable showing internal traces by setting the environment variable ROBOT_INTERNAL_TRACES to any non-empty value.

If the log file still does not detail enough information, it is a good idea to enable the syslog and see what information it provides. It is also possible to add some keywords to the test cases/RPA tasks to further see what is going on. Especially BuiltIn keywords Log and Log Variables are useful. If nothing else works, it is always possible to search help from mailing lists or elsewhere.

>**TODO:**  Video demos of each example could be useful!

#### Using the Python debugger (pdb)
It is also possible to use the pdb module from the Python standard library to set a break point and interactively debug a running test. The typical way of invoking pdb, by inserting the following code at the location you want to break into debugger, will not work correctly with Robot Framework, as the standard output stream is redirected during keyword execution.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   import pdb; pdb.set_trace()
   ```
</details>  
<br />

Instead, you can use the following code from within a python library

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
   ```
</details>  
<br />

or alternatively this code instead can be used directly in a test case/RPA task.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   Evaluate    pdb.Pdb(stdout=sys.__stdout__).set_trace()    modules=sys, pdb
   ```
</details>  
<br />


## Test execution
This section describes how the suite structure created from the parsed input data is executed, how Test status is determined, how to continue executing a test case if there are failures and how to stop the whole execution gracefully.

### Execution flow
#### Executed suites and tests
test cases are always executed within a suite. A suite created from a suite file has tests directly, whereas suites created from directories have child suites which either have tests or their own child suites. By default all the tests in an executed suite are run, but it is possible to select specific ones using options --test, --suite, --include and --exclude. Suites containing no tests are ignored.

The execution starts from the top-level suite. If the suite has tests they are executed one-by-one, and if it has suites they are executed recursively in depth-first order. When an individual test case is executed, the keywords it contains are run in a sequence. Normally the execution of the current Test ends if any of the keywords fails, but it is also possible to continue after failures. The exact execution order and how possible setups and teardowns affect the execution are discussed in the following sections.

#### Setups and teardowns
Setups and teardowns can be used on suite, test case and user keyword levels.

##### Suite setup
If a suite has a setup, it is executed before its tests and child suites. If the suite setup passes, execution continues normally. If it fails, all the test cases the suite and its child suites contain are marked failed. The tests and possible suite setups and teardowns in the child suites are not executed.

Suite setups are often used for setting up the execution environment. Because tests are not run if the suite setup fails, it is easy to use suite setups for verifying that the environment is in state in which the tests can be executed.

##### Suite teardown
If a suite has a teardown, it is executed after all its test cases and child suites. Suite teardowns are executed regardless of the execution status and even if the matching suite setup fails. If the suite teardown fails, all tests in the suite are marked failed afterwards in reports and logs.

Suite teardowns are mostly used for cleaning up the test environment after the execution. To ensure that all these tasks are done, all the keywords used in the teardown are executed even if some of them fail.

##### Test setup
Possible Test setup is executed before the keywords of the test case. If the setup fails, the keywords are not executed. The main use for Test setups is setting up the environment for that particular test case.

##### Test teardown
Possible Test teardown is executed after the test case has been executed. It is executed regardless of the execution status and also if Test setup has failed.

Similarly as suite teardown, Test teardowns are used mainly for cleanup activities. Also they are executed fully even if some of their keywords fail.

##### User keyword setup
User keyword setup is executed before the keyword body. If the setup fails, the body is not executed. There is not much difference between the keyword setup and the first keyword in the body.

> &#128226; _**NOTE:** User keyword setups are new in Robot Framework 7.0.

##### User keyword teardown
User keyword teardown is run after the keyword is executed otherwise, regardless the status. User keyword teardowns are executed fully even if some of their keywords would fail.

#### Execution order
test cases in a suite are executed in the same order as they are defined in the test case file. Suites inside a higher level suite are executed in a case-insensitive alphabetical order based on the file or directory name. If multiple files and/or directories are provided from the command line, they are executed in the order they are provided.

If there is a need to use a certain test execution order inside a directory, it is possible to add prefixes such as 01 and 02 into file and directory names. Such prefixes are not included in the generated suite name if they are separated from the base name of the suite with two underscores:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   01__my_suite.robot -> My Suite
   02__another_suite.robot -> Another Suite
   ```
</details>  
<br />

If the alphabetical ordering of suites inside suites is problematic, a good workaround is providing  them separately in the required order. This easily leads to overly long start-up commands, but argument files allow listing files nicely one file per line.

It is also possible to randomize the execution order using the --randomize option.

### Test and suite statuses
This section explains how tests can get PASS, FAIL or SKIP status and how the suite status is determined based on Test statuses.

> &#128226; _**NOTE:** The SKIP status is new in Robot Framework 4.0.

#### PASS
A Test gets the PASS status if it is executed and none of the keywords it contains fails.

##### Prematurely passing tests
Typically, all keywords are executed, but it is also possible to use BuiltIn keywords Pass Execution and Pass Execution If to stop execution with the PASS status and not to continue run the remaining keywords.

How Pass Execution and Pass Execution If behave in different situations is explained below:

* When used in any setup or teardown (suite, Test or keyword), these keywords pass that setup or teardown. Possible teardowns of the started keywords are executed. Test execution or statuses are not affected otherwise.
* When used in a test case outside setup or teardown, the keywords pass that particular test case. 
* Possible test and keyword teardowns are executed.
* Possible continuable failures that occur before these keyword are used, as well as failures in teardowns executed afterwards, will fail the execution.
* It is mandatory to give an explanation message why execution was interrupted, and it is also possible to modify test case tags. For more details, and usage examples, see the documentation of these keywords.

Passing execution in the middle of a Test, setup or teardown should be used with care. In the worst case it leads to tests which skip all the parts that could actually uncover problems in the tested application. In cases where execution cannot continue do to external factors, it is often safer to skip the Test.

#### FAIL
The most common reason for a Test to be assigned the FAIL status is that one of the keywords it contains fails. The keyword itself can fail by raising an exception or the keyword can be called incorrectly. Other reasons for failures include syntax errors and the Test being empty.

If a suite setup fails, tests in that suite are marked failed without running them. If a suite teardown fails, tests are marked failed retroactively.

#### SKIP
Starting from Robot Framework 4.0, tests can get also SKIP status in addition to PASS and FAIL. There are many different ways to get this status.

##### Skipping before execution
The command line option --skip can be used to skip specified tests without running them at all. It works based on tags and supports tag patterns like examp?? and tagANDanother. If it is used multiple times, all tests matching any of specified tags or tag patterns are skipped:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --skip require-network
   --skip windowsANDversion9?
   --skip python2.* --skip python3.[0-6]
   ```
</details>  
<br />

Starting from Robot Framework 5.0, a test case can also be skipped by tagging the test with the reserved tag robot:skip:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
       [Tags]    robot:skip
       Log       This is not executed
   ```
</details>  
<br />

The difference between --skip and --exclude is that with the latter, tests are omitted from the execution altogether and they will not be shown in logs and reports. With the former they are included, but not actually executed, and they will be visible in logs and reports.

##### Skipping dynamically during execution
Tests can get the skip status during execution in various ways:

* Using the BuiltIn keyword Skip anywhere in the test case, including setup or teardown. Using Skip keyword has two effects: the test gets the SKIP status and rest of the Test is not executed. However, if the Test has a teardown, it will be run.
* Using the BuiltIn keyword Skip If which takes a condition and skips the Test if the condition is true.
* Library keywords may also trigger skip behavior by using a special exceptions. This is explained the Skipping tests section in the Creating libraries chapter.
* If suite setup is skipped using any of the above means, all tests in the suite are skipped without executing them.
* If suite teardown is skipped, all tests will be marked skipped retroactively.

##### Automatically skipping failed tests
The command line option --skiponfailure can be used to automatically mark failed tests skipped. It works based on tags and supports tag patterns like the --skip option discussed above:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --skiponfailure not-ready
   --skiponfailure experimentalANDmobile
   ```
</details>  
<br />

Starting from RF 5.0, the reserved tag robot:skip-on-failure can alternatively be used to achieve the same effect as above:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
       [Tags]    robot:skip-on-failure
       Fail      this Test will be marked as skipped instead of failed
   ```
</details>  
<br />

The motivation for this functionality is allowing execution of tests which are not yet ready or that are executing a functionality which is not yet ready. Instead of such tests failing, they will be marked skipped and their tags can be used to separate them from possible other skipped tests.

#### Migrating from criticality to SKIP
The first Robot Framework versions supported  criticality concept which allowed marking tests critical or non-critical. By default all tests were critical, but the --critical and --noncritical options could be used to configure that. The difference between critical and non-critical tests was that non-critical were not included when determining the final status for an executed suite or for the whole execution. In practice the Test status was two dimensional having PASS and FAIL in one axis and criticality on the other.

Non-critical failed tests were in many ways similar to the current skipped tests. Because these features are similar and having both SKIP and criticality would have created strange statuses such as a non-critical SKIP, the criticality concept was removed in Robot Framework 4.0 when the SKIP status was introduced. The problems with criticality are explained in more detail in the issue that proposed removing it.

The main use case for the criticality concept was being able to run tests which are not yet ready or that are executing a functionality that is not yet ready. This use case is nowadays covered by the skip-on-failure functionality discussed in the previous section.

To ease migrating from criticality to skipping, the old --noncritical option worked as an alias for the new --skiponfailure in Robot Framework 4.0 and also the old --critical option was preserved. Both old options were deprecated and they were removed in Robot Framework 5.0.

#### Suite status
Suite status is determined solely based on statuses of the tests it contains:

* If any Test has failed, suite status is FAIL.
* If there are no failures but at least one Test has passed, suite status is PASS.
* If all tests have been skipped or the are no tests at all, suite status is SKIP.

### Continuing on failure
Typically, test cases are stopped immediately when any of their keywords fail. This behavior shortens test execution time and prevents subsequent keywords hanging or otherwise causing problems if the system under test/RPA system is in unstable state. This has a drawback that often subsequent keywords would give more information about the state of the system, however, and in some cases those subsequent keywords would actually handle of the needed cleanup activities. Hence, Robot Framework offers several features to continue even if there are failures.

#### Execution continues on teardowns automatically
To ensure all the cleanup activities are handled, the continue-on-failure mode is automatically enabled in suite, Test and keyword teardowns. In practice this means that in teardowns all the keywords in all levels are always executed.

If this behavior is not desired, the special robot:stop-on-failure and robot:recursive-stop-on-failure tags can be used to disable it.

#### All top-level keywords are executed when tests have templates
When using Test templates, all the top-level keywords are executed to make it sure that all the different combinations are covered. In this usage continuing is limited to the top-level keywords and inside them the execution ends normally if there are non-continuable failures.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Continue with templates
       [Template]    Should be Equal
       this    fails
       this    is run
   ```
</details>  
<br />

If this behavior is not desired, the special robot:stop-on-failure and robot:recursive-stop-on-failure tags can be used to disable it.

#### Special failures from keywords
Library keywords report failures using exceptions and it is possible to use special exceptions to inform Robot Framework that execution can continue regardless the failure. How these exceptions can be created is explained in the Continuable failures section in the Creating Test libraries section.

When a Test ends and there have been continuable failures, the Test will be marked failed. If there is more than one failure, all of them will be enumerated in the final error message:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   Several failures occurred:
   
   1) First error message.
   
   2) Second error message.
   ```
</details>  
<br />

Test execution ends also if a normal failure occurs after a continuable failure. Also in that case all the failures will be listed in the final error message.

The return value from failed keywords, possibly assigned to a variable, is always the Python None.

#### Run Keyword And Continue On Failure keyword
BuiltIn keyword Run Keyword And Continue On Failure allows converting any failure into a continuable failure. These failures are handled by the framework exactly the same way as continuable failures originating from library keywords discussed above.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
       Run Keyword and Continue on Failure    Should be Equal    1    2
       Log    This is executed but test fails in the end

   ```
</details>  
<br />

#### Enabling continue-on-failure using tags
All keywords executed as part of test cases or user keywords which are tagged with the robot:continue-on-failure tag are considered continuable by default. For example, the following two tests behave identically:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Test 1
       Run Keyword and Continue on Failure    Should be Equal    1    2
       User Keyword 1
   
   Test 2
       [Tags]    robot:continue-on-failure
       Should be Equal    1    2
       User Keyword 2
   
   *** Keywords ***
   User Keyword 1
       Run Keyword and Continue on Failure    Should be Equal    3    4
       Log    This is executed
   
   User Keyword 2
       [Tags]    robot:continue-on-failure
       Should be Equal    3    4
       Log    This is executed
   ```
</details>  
<br />

These tags also affect the continue-on-failure mode with different control structures. For example, the below test case will execute the Do Something keyword ten times regardless whether each succeeds or not:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
       [Tags]    robot:continue-on-failure
       FOR    ${index}    IN RANGE    10
           Do Something
       END
   ```
</details>  
<br />

Setting robot:continue-on-failure within a test case or a user keyword will not propagate the continue-on-failure behavior into user keywords they call. If such recursive behavior is needed, the robot:recursive-continue-on-failure tag can be used. For example, all keywords in the following example are executed:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
       [Tags]    robot:recursive-continue-on-failure
       Should be Equal    1    2
       User Keyword 1
       Log    This is executed
   
   *** Keywords ***
   User Keyword 1
       Should be Equal    3    4
       User Keyword 2
       Log    This is executed
   
   User Keyword 2
       Should be Equal    5    6
       Log    This is executed
   ```
</details>  
<br />

Setting robot:continue-on-failure or robot:recursive-continue-on-failure in a test case does NOT alter the behaviour of a failure in the keyword(s) executed as part of the [Setup]: The test case is marked as failed and no test case keywords are executed.

> &#128226; _**NOTE:** The robot:continue-on-failure and robot:recursive-continue-on-failure tags are new in Robot Framework 4.1. They do not work properly with WHILE loops prior to Robot Framework 6.0.

#### Disabling continue-on-failure using tags
Special tags robot:stop-on-failure and robot:recursive-stop-on-failure can be used to disable the continue-on-failure mode if needed. They work when continue-on-failure has been enabled using tags and also with teardowns and templates:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Disable continue-in-failure set using tags
       [Tags]    robot:recursive-continue-on-failure
       Keyword
       Keyword    # This is executed
   
   Disable continue-in-failure in teardown
       No Operation
       [Teardown]    Keyword
   
   Disable continue-in-failure with templates
       [Tags]    robot:stop-on-failure
       [Template]    Should be Equal
       this    fails
       this    is not run
   
   *** Keywords ***
   Keyword
       [Tags]    robot:stop-on-failure
       Should be Equal    this    fails
       Should be Equal    this    is not run    
   ```
</details>  
<br />

The robot:stop-on-failure tag affects only test cases and user keywords where it is used and does not propagate to user keywords they call nor to their own teardowns. If recursive behavior affecting all called user keywords and teardowns is desired, the robot:recursive-stop-on-failure tag can be used instead. If there is a need, its effect can again be disabled in lower level keywords by using robot:continue-on-failure or robot:recursive-continue-on-failure tags.

The robot:stop-on-failure and robot:recursive-stop-on-failure tags do not alter the behavior of continuable failures caused by library keywords or by Run Keyword And Continue On Failure. For example, both keywords in this example are run even though robot:stop-on-failure is used:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
       [Tags]    robot:stop-on-failure
       Run Keyword and Continue on Failure    Should be Equal    1    2
       Log    This is executed regardless the tag    
   ```
</details>  
<br />

If robot:recursive-stop-on-failure and robot:continue-on-failure are used together in the same Test or keyword, execution is stopped in called keywords if there are failures, but continues in the Test or keyword using these tags. If robot:recursive-continue-on-failure and robot:stop-on-failure are used together in the same Test or keyword, execution is continued in called keywords if there are failures, but stopped in the Test or keyword using these tags.

> &#128226; _**NOTE:** The robot:stop-on-failure and robot:recursive-stop-on-failure tags are new in Robot Framework 6.0.

> &#128226; _**NOTE:** Using recursive and non-recursive tags together in same Test or keyword is new in Robot Framework 7.0.

#### TRY/EXCEPT
Robot Framework 5.0 introduced a native TRY/EXCEPT syntax which can be used for handling failures:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
       TRY
           Some Keyword
       EXCEPT    Expected error message
           Error Handler Keyword
       END    
   ```
</details>  
<br />

For more details see the separate TRY/EXCEPT syntax section.

#### BuiltIn keywords
There are several BuiltIn keywords that can be used to execute other keywords so that execution can continue after possible failures:

* Run Keyword And Expect Error executes a keyword and expects it to fail with the specified error message. The aforementioned TRY/EXCEPT syntax is nowadays generally recommended instead.
* Run Keyword And Ignore Error executes a keyword and silences possible error. It returns the status along with possible keyword return value or error message. The TRY/EXCEPT syntax generally works better in this case as well.
* Run Keyword And Warn On Failure is a wrapper for Run Keyword And Ignore Error that automatically logs a warning if the executed keyword fails.
* Run Keyword And Return Status executes a keyword and returns Boolean True or False depending on did it pass or fail.

### Stopping test execution gracefully
Sometimes there is a need to stop the execution before all the tests have finished, but still with logs and reports being created. Different ways of accomplishing this are explained below. In all these cases the remaining test cases are marked failed.

The tests which are automatically failed get robot:exit tag and the generated report will include NOT robot:exit combined tag pattern to easily see those tests which were not skipped. Note that the Test in which the exit happened does not get the robot:exit tag.

> &#128226; _**NOTE:** Prior to Robot Framework 3.1, the special tag was named robot-exit.

#### Pressing Ctrl-C
The execution is stopped when Ctrl-C is pressed in the console where the execution is occurring. The execution is stopped immediately, but reports and logs are still generated.

If Ctrl-C is pressed again, the execution ends immediately and reports and logs are not created.

#### Using signals
On UNIX-like machines it is possible to terminate execution using signals INT and TERM. These signals can be sent from the command line using a kill command and sending signals can also be easily automated.

#### Using keywords
The execution can be stopped also by the executed keywords. There is a separate Fatal Error BuiltIn keyword for this purpose, and custom keywords can use fatal exceptions when they fail.

#### Stopping when first test case fails
If option --exitonfailure (-X) is used, execution stops immediately if any Test fails. The remaining tests are marked as failed without actually executing them.

#### Stopping on parsing or execution error
Robot Framework separates failures caused by failing keywords from errors caused by, for example, invalid settings or failed library imports. By default these errors are reported as execution errors, but errors themselves do not fail tests or affect execution otherwise. If --exitonerror option is used, however, all such errors are considered fatal and execution stopped so that remaining tests are marked failed. With parsing errors encountered before execution even starts, this means that no tests are actually run.

#### Handling teardowns
By default teardowns of the tests and suites which have been started are executed even if the execution is stopped using one of the methods above. This allows clean-up activities to be run regardless how execution ends.

It is also possible to skip teardowns when execution is stopped by using --skipteardownonexit option. This can be useful if, for example, clean-up tasks take a lot of time.

## Task execution
Robot Framework can be used also for other automation purposes than test automation and starting from Robot Framework 3.1 it is possible to explicitly create and execute Robotic Process Automation  tasks. For the most parts task execution and test execution work the same way and this section explains the differences.

### Generic automation mode
When Robot Framework is used execute a file and it notices that the file has tasks, not tests, it automatically sets itself into the generic automation mode. This mode does not change the actual execution at all, but when logs and reports are created, they use term task, not test. They have, for example, headers like Task Log and Task Statistics instead of Test Log and Test Statistics.

The generic automation mode can also be enabled by using the --rpa option. In that case the executed files can have either tests or tasks. Alternatively --norpa can be used to force the test automation mode even if executed files contain tasks. If neither of these options are used, it is an error to execute multiple files so that some have tests and others have tasks.

The execution mode is stored in the generated output file and read by Rebot if outputs are post-processed. The mode can also be set when using Rebot if necessary.

>**TODO:** Below reads as though the user would have read the above test section 1st perhaps. Better a clone of test for those users coming only to this section?

#### Task related command line options
All normal command line options can be used when executing tasks. If there is a need to select only certain tasks for execution, --task can be used instead of --test. Additionally the aforementioned --rpa can be used to control the execution mode.

## Post-processing outputs
XML output files that are generated during the test execution can be post-processed afterwards by the Rebot tool, which is an integral part of Robot Framework. It is used automatically when test/task reports and logs are generated during the execution and using it separately allows creating custom reports and logs as well as combining and merging results.

### Using Rebot

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot [options] outputs
   python -m robot.rebot [options] outputs
   python path/to/robot/rebot.py [options] outputs
   
   ```
</details>  
<br />

The most common way to use Rebot is using the rebot command. Alternatively it is possible to execute the installed robot.rebot module or the robot/rebot.py file using the selected Python interpreter.

#### Specifying options and arguments
The basic syntax for using Rebot is exactly the same as when starting test execution and also most of the command line options are identical. The main difference is that arguments to Rebot are XML output files instead of input data files or directories.

#### Return codes with Rebot
Return codes from Rebot are exactly same as when running tests.

#### Controlling execution mode
Rebot notices whether tests or tasks been run and by default preserves the execution mode. The mode affects logs and reports so that in the former case they will use terminology of test, such as Test Log and Test Statistics, and in the latter case term task such as Task Log and Task Statistics.

Rebot also supports using --rpa or --norpa options to set the execution mode explicitly. This is necessary if multiple output files are processed and they have conflicting modes.

### Creating reports, logs and output files
You can use Rebot for creating the same reports and logs that are created automatically during the test execution. Of course, it is not sensible to create the exactly same files, but, for example, having one report with all test cases and another with only some subset of tests can be useful:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot output.xml
   rebot path/to/output_file.xml
   rebot --include smoke --name Smoke_Tests c:\results\output.xml
   ```
</details>  
<br />

Another common usage is creating only the output file when running tests (log and report generation can be disabled with --log NONE --report NONE) and generating logs and reports later. Tests can, for example, be executed on different environments, output files collected to a central place and reports and logs created there.

Rebot does not create XML output files by default, but it is possible to create them by using the --output (-o) option. Log and report are created by default, but they can be disabled by using value NONE (case-insensitive) if they are not needed:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot --include smoke --output smoke.xml --log none --report none original.xml
   ```
</details>  
<br />

### Combining outputs
An important feature in Rebot is its ability to combine outputs from different test execution rounds. This capability allows, for example, running the same test cases/RPA tasks on different environments and generating an overall report from all outputs. Combining outputs is extremely easy, all that needs to be done is giving several output files as arguments:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot output1.xml output2.xml
   rebot outputs/*.xml   
   ```
</details>  
<br />

When outputs are combined, a new top-level suite is created so that suites in the given output files are its child suites. This works the same way when multiple input data files or directories are executed, and also in this case the name of the top-level suite is created by joining child suite names with an ampersand (&) and spaces. These automatically generated names are not ideal, and it is often a good idea to use --name to give a more meaningful name:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot --name Browser_Compatibility firefox.xml opera.xml safari.xml ie.xml
   rebot --include smoke --name Smoke_Tests c:\results\*.xml
   ```
</details>  
<br />

### Merging outputs
If the same tests are re-executed or a single test suite executed in pieces, combining results like discussed above creates an unnecessary top-level suite. In these cases it is typically better to merge results instead. Merging is acheived by using --merge (-R) option which changes the way how Rebot combines two or more output files. This option itself takes no arguments and all other command line options can be used with it normally:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot --merge original.xml merged.xml
   rebot --merge --name Example first.xml second.xml third.xml
   ```
</details>  
<br />

When suites are merged, documentation, suite setup and suite teardown are obtained from the last merged suite. Suite metadata from all merged suites is preserved so that values in latter suites have precedence.

How merging tests works, is explained in the following sections discussing the two main merge use cases.

> &#128226; _**NOTE:** Getting suite documentation and metadata from merged suites is new in Robot Framework 6.0.

#### Merging re-executed tests/tasks
There is often a need to re-execute a subset of tests/tasks, for example, after fixing a bug in the system under test/RPA system or in the tests/tasks themselves. This can be accomplished by selecting test cases/tasks by names (--test or --task and --suite options), tags (--include and --exclude), or by previous status (--rerunfailed or --rerunfailedsuites).

Combining re-execution results with the original results using the default combining outputs approach does not work too well. The main problem is that you get separate suites and possibly already fixed failures are also shown. In this situation it is better to use the --merge (-R) option to tell Rebot to merge the results instead. In practice this means that tests/tasks from the latter test/task runs replace those in the original. An exception to this rule is that skipped tests/tasks  in latter runs are ignored and the original are preserved.

This usage is best illustrated by a practical example using --rerunfailed and --merge together:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --output original.xml tests                          # first execute all tests
   robot --rerunfailed original.xml --output rerun.xml tests  # then re-execute failing
   rebot --merge original.xml rerun.xml                       # finally merge results
   ```
</details>  
<br />

The message of the merged tests/tasks contains a note that results have been replaced. The message also shows the old status and message of the test/task.

Merged results must always have same top-level suite. Tests/tasks and suites in merged outputs that are not found from the original output, are added into the resulting output. How this works in practice is discussed in the next section.

> &#128226; _**NOTE:** Ignoring skipped tests in latter runs is new in Robot Framework 4.1.

#### Merging suites executed in pieces
Another important use case for the --merge option is merging results got when running a suite in pieces using, for example, --include and --exclude options:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --include smoke --output smoke.xml tests   # first run some tests
   robot --exclude smoke --output others.xml tests  # then run others
   rebot --merge smoke.xml others.xml               # finally merge results
   ```
</details>  
<br />

When merging outputs like this, the resulting output contains all tests/tasks and suites found from all given output files. If some test/task is found from multiple outputs, latest results replace the earlier ones as explained in the previous section. Also this merging strategy requires the top-level suites to be same in all outputs.

### JSON output files
Rebot can create and process output files also in the JSON format. Creating JSON output files is done using the typical --output option so that the specified file has a .json extension:


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot --output output.json output.xml   
   ```
</details>  
<br />

When reading output files, JSON files are automatically recognized by the extension:


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot output.json
   rebot output1.json output2.json
   ```
</details>  
<br />

When combining or merging results, it is possible to mix JSON and XML files:


***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot output1.xml output2.json
   rebot --merge original.xml rerun.json
   ```
</details>  
<br />

The JSON output file structure is documented in the result.json schema file.

> &#128226; _**NOTE:** Support for JSON output files is new in Robot Framework 7.0.

## Configuring execution
This section explains different command line options that can be used for configuring the execution or post-processing outputs. Options related to generated output files are discussed in the next section.

### Selecting files to parse
#### Executing individual files
When executing individual files, Robot Framework tries to parse and run them regardless the name or the file extension. Which parser to use depends on the extension:

* .robot files and files that are not recognized are parsed using the normal Robot Framework parser.
* .rst and .rest files are parsed using the reStructuredText parser.
* .rbt and .json files are parsed using the JSON parser.

Files supported by custom parsers are parsed by a matching parser.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   robot example.robot    # Standard Robot Framework parser.
   robot example.tsv      # Must be compatible with the standard parser.
   robot example.rst      # reStructuredText parser.
   robot x.robot y.rst    # Parse both files using an appropriate parser.
   ```
</details>  
<br />

#### Included and excluded files
When executing a directory, files and directories are parsed using the following rules:

* All files and directories starting with a dot (.) or an underscore (_) are ignored.
* .robot files are parsed using the normal Robot Framework parser.
* .robot.rst files are parsed using the reStructuredText parser.
* .rbt files are parsed using the JSON parser.
* Files supported by custom parsers are parsed by a matching parser.
* Other files are ignored unless parsing them has been enabled by using the --parseinclude or --extension options discussed in the subsequent sections.

#### Selecting files by name or path
When executing a directory, it is possible to parse only certain files based on their name or path by using the --parseinclude (-I) option. This option has slightly different semantics depending on the value it is used with:

If the value is just a file name like example.robot, files matching the name in all directories will be parsed.
To match only a certain file in a certain directory, files can be given as relative or absolute paths like path/to/tests.robot.
If the value is a path to a directory, all files inside that directory are parsed, recursively.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   robot --parseinclude example.robot tests       # Parse `example.robot` files anywhere under `tests`.
   robot -I example_*.robot -I ???.robot tests    # Parse files matching `example_*.robot` or `???.robot` under `tests`.
   robot -I tests/example.robot tests             # Parse only `tests/example.robot`.
   robot --parseinclude tests/example tests       # Parse files under `tests/example` directory, recursively.
   ```
</details>  
<br />

Values used with --parseinclude are case-insensitive and support glob patterns like example_*.robot. There are, however, two small differences compared to how patterns typically work with Robot Framework:

* \* matches only a single path segment. For example, path/*/tests.robot matches path/to/tests.robot but not path/to/nested/tests.robot.
* \** can be used to enable recursive matching. For example, path/**/tests.robot matches both path/to/tests.robot and path/to/nested/tests.robot.

If the pattern contains a file extension, files with that extension are parsed even if they by default would not be. Which parser to use depends on the used extension:

* .rst and .rest files are parsed using the reStructuredText parser.
* .json files are parsed using the JSON parser.
* Other files are parsed using the normal Robot Framework parser.

Notice that when you use a pattern such as *.robot and a file exists which that matches the pattern in the execution directory, the shell may resolve the pattern before Robot Framework is called and the value passed to it is the file name, not the original pattern. In such cases you need to quote or escape the pattern like '*.robot' or \*.robot.

> &#128226; _**NOTE:** --parseinclude is new in Robot Framework 6.1.

#### Selecting files by extension
In addition to using the --parseinclude option discussed in the previous section, it is also possible to enable parsing files that are not parsed by default by using the --extension (-F) option. Matching extensions is case insensitive and the preceeding dot can be omitted. If there is a need to parse more than one kind of file, it is possible to use a colon : to separate extensions:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --extension rst path/to/tests    # Parse only *.rst files.
   robot -F robot:rst path/to/tests       # Parse *.robot and *.rst files.
   ```
</details>  
<br />

The above is equivalent to the following --parseinclude usage:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --parseinclude *.rst path/to/tests
   robot -I *.robot -I *.rst path/to/tests
   ```
</details>  
<br />

Because the --parseinclude option is more powerful and covers all same use cases as the --extension option, the latter is likely to be deprecated in the future. Users are recommended to use --parseinclude already now.

#### Using custom parsers
External parsers can parse files that Robot Framework does not recognize otherwise. For more information about creating and using such parsers see the Parser interface section.

### Selecting test cases/RPA tasks
Robot Framework offers several command line options for selecting which test cases to execute. The same options work also when executing tasks and when post-processing outputs with Rebot.

#### By test names
The easiest way to select only some tests/tasks to be run is using the --test (-t) option. As the name implies, it can be used for selecting tests/tasks by their names. Given names are case, space and underscore insensitive and they also support simple patterns. The option can be used multiple times to match multiple tests/tasks:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```   
   --test Example                   # Match only tests with name 'Example'.
   --test example*                  # Match tests starting with 'example'.
   --test first --test second       # Match tests with name 'first' or 'second'.
   ```
</details>  
<br />

To pinpoint a test more precisely, it is possible to prefix the test/task name with a suite name:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   
   --test mysuite.mytest            # Match test 'mytest' in suite 'mysuite'.
   --test root.sub.test             # Match test 'test' in suite 'sub' in suite 'root'.
   --test *.sub.test                # Match test 'test' in suite 'sub' anywhere.
   ```
</details>  
<br />

Notice that when the given name includes a suite name, it must match the whole suite name starting from the root suite. Using a wildcard as in the last example above allows matching tests/tasks with a parent suite anywhere.

Using the --test option is convenient when only a few tests needs to be selected. A common use case is running just the test/task that is currently being worked on. If a bigger number of tests needs to be selected, it is typically easier to select them by suite names or by tag names.

When executing tasks, it is possible to use the --task option as an alias for --test.

#### By suite names
Tests/tasks can be selected also by suite names with the --suite (-s) option that selects all tests/tasks in matching suites. Similarly as with --test or --task, given names are case, space and underscore insensitive and support simple patterns. To pinpoint a suite more precisely, it is possible to prefix the name with the parent suite name:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```   
   --suite Example                  # Match only suites with name 'Example'.
   --suite example*                 # Match suites starting with 'example'.
   --suite first --suite second     # Match suites with name 'first' or 'second'.
   --suite root.child               # Match suite 'child' in root suite 'root'.
   --suite *.parent.child           # Match suite 'child' with parent 'parent' anywhere.
   ```
</details>  
<br />

If the name contains a parent suite name, it must match the whole suite name the same way as with --test or --task. Using a wildcard as in the last example above allows matching suites with a parent suite anywhere.

> &#128226; _**NOTE:** Prior to Robot Framework 7.0, --suite with a parent suite did not need to match the whole suite name. For example, parent.child would match suite child with parent parent anywhere. The name must be prefixed with a wildcard if this behavior is desired nowadays.

If both --suite and --test options are used, only the specified tests in specified suites are selected:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --suite mysuite --test mytest    # Match test 'mytest' if its inside suite 'mysuite'.
   ```
</details>  
<br />

Using the --suite option is more or less the same as executing the appropriate suite file or directory directly. The main difference is that if a file or directory is run directly, possible suite setups and teardowns on higher level are not executed:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   # Root suite is 'Tests' and its possible setup and teardown are run.
   robot --suite example path/to/tests
   
   # Root suite is 'Example' and possible higher level setups and teardowns are ignored.
   robot path/to/tests/example.robot
   ```
</details>  
<br />

Prior to Robot Framework 6.1, files not matching the --suite option were not parsed at all for performance reasons. This optimization was not possible anymore after suites got a new Name setting that can override the default suite name that is got from the file or directory name. New --parseinclude option has been added to explicitly select which files are parsed if this kind of parsing optimization is needed.

#### By tag names
It is possible to include and exclude test cases by tag names with the --include (-i) and --exclude (-e) options, respectively. If the --include option is used, only test cases/RPA tasks having a matching tag are selected, and with the --exclude option those having a matching tag are not. If both are used, only tests/tasks with a tag matching the former option, and not with a tag matching the latter, are selected:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include example
   --exclude not_ready
   --include regression --exclude long_lasting
   ```
</details>  
<br />

Both --include and --exclude can be used several times to match multiple tags. In that case a test/task is selected if it has a tag that matches any included tags, and also has no tag that matches any excluded tags.

In addition to specifying a tag to match fully, it is possible to use tag patterns where * and ? are wildcards and AND, OR, and NOT operators can be used for combining individual tags or patterns together:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --include feature-4?
   --exclude bug*
   --include fooANDbar
   --exclude xxORyyORzz
   --include fooNOTbar
   ```
</details>  
<br />

Starting from RF 5.0, it is also possible to use the reserved tag robot:exclude to achieve the same effect as with using the --exclude option:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   *** Test Cases ***
   Example
      [Tags]    robot:exclude
      Fail      This is not executed
   ```
</details>  
<br />

Selecting test cases/RPA tasks by tags is a very flexible mechanism and allows many interesting possibilities:

* A subset of tests to be executed before other tests, often called smoke tests, can be tagged with smoke and executed with --include smoke.
* Unfinished tests/tasks can be committed to version control with a tag such as not_ready and excluded from the execution with --exclude not_ready.
* Tests/tasks can be tagged with sprint-<num>, where <num> specifies the number of the current sprint, and after executing all test cases/RPA tasks, a separate report containing only the tests/tasks for a certain sprint can be generated (for example, rebot --include sprint-42 output.xml).

Options --include and --exclude can be used in combination with --suite and --test or --task discussed in the previous section. In that case tests/task which are selected must match all selection criteria:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --suite example --include tag    # Match test if it is in suite 'example' and has tag 'tag'.
   --suite example --exclude tag    # Match test if it is in suite 'example' and does not have tag 'tag'.
   --test ex* --include tag         # Match test if its name starts with 'ex' and it has tag 'tag'.
   --test ex* --exclude tag         # Match test if its name starts with 'ex' and it does not have tag 'tag'.
   ```
</details>  
<br />

> &#128226; _**NOTE:** In Robot Framework 7.0 --include and --test were cumulative and selected tests/tasks needed to match only either of these options. That behavior caused backwards incompatibility problems and it was changed back to the original already in Robot Framework 7.0.1.

#### Re-executing failed test cases/RPA tasks
Command line option --rerunfailed (-R) can be used to select all failed tests/tasks from an earlier output file for re-execution. This option is useful, for example, if running all tests/tasks takes a lot of time and one wants to iteratively fix failing test cases/RPA tasks.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot tests                             # first execute all tests
   robot --rerunfailed output.xml tests    # then re-execute failing
   ```
</details>  
<br />

Behind the scenes this option selects the failed tests/tasks as they would have been selected individually using the --test or --task option. It is possible to further fine-tune the list of selected tests by using --test, --task, --suite, --include and --exclude options.

It is an error if the output contains no failed tests/tasks, but this behavior can be changed by using the --runemptysuite option discussed below. Using an output not originating from executing the same tests/tasks which are run now causes undefined results. Using a special value NONE as the output is same as not specifying this option at all.

> &#128226; _**TIP:** Re-execution results and original results can be merged together using the --merge command line option.

#### Re-executing failed test suites
Command line option --rerunfailedsuites (-S) can be used to select all failed suites from an earlier output file for re-execution. Like --rerunfailed (-R), this option is useful when full test execution takes a lot of time. Note that all tests/tasks from a failed suite will be re-executed, even passing ones. This option is useful when the tests/tasks in a suite depend on each other.

Behind the scenes this option selects the failed suites as they would have been selected individually with the --suite option. It is possible to further fine-tune the list of selected tests/tasks by using --test, --task, --suite, --include and --exclude options.

#### When no tests match selection
By default when no tests match the selection criteria test execution fails with an error such as:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   [ ERROR ] Suite 'Example' contains no tests matching tag 'xxx'.
   ```
</details>  
<br />

Because no outputs are generated, this behavior can be problematic if tests/tasks are executed and results processed automatically. Luckily a command line option --RunEmptySuite (case-insensitive) can be used to force the suite to be executed also in this case. As a result normal outputs are created but show zero executed tests/tasks. The same option can be used also to alter the behavior when an empty directory or a test case/RPA task file containing no tests/tasks is executed.

A similar situation can occur also when processing output files with Rebot. It is possible that no tests/tasks match the used filtering criteria or that the output file contained no tests/tasks to begin with. By default executing Rebot fails in these cases, but it has a separate --ProcessEmptySuite option that can be used to alter the behavior. In practice this option works the same way as --RunEmptySuite when running tests.

> &#128226; _**NOTE:** Using --RunEmptySuite with --ReRunFailed or --ReRunFailedSuites requires Robot Framework 5.0.1 or newer.

### Setting metadata
#### Setting suite name
When Robot Framework parses input data, suite names are created from file and directory names. The name of the top-level suite can, however, be overridden with the command line option --name (-N):

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --name "Custom name" tests.robot
   ```
</details>  
<br />

#### Setting suite documentation
In addition to defining documentation in the input data, documentation of the top-level suite can be given from the command line with the option --doc (-D). The value can contain simple HTML formatting and must be quoted if it contains spaces.

If the given documentation is a relative or absolute path pointing to an existing file, the actual documentation will be read from that file. This is especially convenient if the externally specified documentation is long or contains multiple lines.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```  
   robot --doc "Example documentation" tests.robot
   robot --doc doc.txt tests.robot    # Documentation read from doc.txt if it exits.
   ```
</details>  
<br />

> &#128226; _**NOTE:** Reading documentation from an external file is new in Robot Framework 4.1.
> &#128226; _**NOTE:** Prior to Robot Framework 3.1, underscores in documentation were converted to spaces same way as with the --name option.

#### Setting free suite metadata
Free suite metadata may also be given from the command line with the option --metadata (-M). The argument must be in the format name:value, where name the name of the metadata to set and value is its value. The value can contain simple HTML formatting and the whole argument must be quoted if it contains spaces. This option may be used several times to set multiple metadata values.

If the given value is a relative or absolute path pointing to an existing file, the actual value will be read from that file. This is especially convenient if the value is long or contains multiple lines. If the value should be a path to an existing file, not read from that file, the value must be separated with a space from the name: part.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   robot --metadata Name:Value tests.robot
   robot --metadata "Another Name:Another value, now with spaces" tests.robot
   robot --metadata "Read From File:meta.txt" tests.robot    # Value read from meta.txt if it exists.
   robot --metadata "Path As Value: meta.txt" tests.robot    # Value always used as-is.
   ```
</details>  
<br />

> &#128226; _**NOTE:** Reading metadata value from an external file is new in Robot Framework 4.1.
> &#128226; _**NOTE:** Prior to Robot Framework 3.1, underscores in the value were converted to spaces same way as with the --name option.

#### Setting test/task tags
The command line option --settag (-G) can be used to set the given tag to all executed test cases/RPA tasks. This option may be used several times to set multiple tags.

### Configuring where to search libraries and other extensions
When Robot Framework imports a library, listener, or some other Python based extension, it uses the Python interpreter to import the module containing the extension from the system. The list of locations where modules are looked for is called the module search path, and its contents can be configured using different approaches explained in this section.

Robot Framework uses Python's module search path also when importing resource and variable files if the specified path does not match any file directly.

The module search path being set correctly so that libraries and other extensions are found is a requirement for successful execution. If you need to customize it using approaches explained below, it is often a good idea to create a custom start-up script.

#### Locations automatically in module search path
Python interpreters have their own standard library as well as a directory where third party modules are installed automatically in the module search path. This means that libraries packaged using Python's own packaging system are automatically installed so that they can be imported without any additional configuration.

##### PYTHONPATH
Python reads additional locations to be added to the module search path from PYTHONPATH environment variables. If you want to specify more than one location in any of them, you need to separate the locations with a colon on UNIX-like machines (e.g. /opt/libs:$HOME/testlibs) and with a semicolon on Windows (e.g. D:\libs;%HOMEPATH%\testlibs).

Environment variables can be configured permanently system wide or so that they affect only a certain user. Alternatively they can be set temporarily before running a command, something which works extremely well in custom start-up scripts.

##### Using --pythonpath option
Robot Framework has a separate command line option --pythonpath (-P) for adding locations to the module search path.

Multiple locations can be given by separating them with a colon (:) or a semicolon (;) or by using this option multiple times. If the value contains both colons and semicolons, it is split from semicolons. Paths can also be glob patterns matching multiple paths, but they typically need to be escaped when used on the console.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   --pythonpath libs
   --pythonpath /opt/testlibs:mylibs.zip:yourlibs
   --pythonpath /opt/testlibs --pythonpath mylibs.zip --pythonpath yourlibs
   --pythonpath c:\temp;d:\resources
   --pythonpath  lib/\*.zip    # '*' is escaped
   ```
</details>  
<br />

> &#128226; _**NOTE:** Both colon and semicolon work regardless the operating system. Using semicolon is new in Robot Framework 5.0.

#### Configuring sys.path programmatically
Python interpreters store the module search path they use as a list of strings in sys.path attribute. This list can be updated dynamically during execution and changes are taken into account the next time when something is imported.

### Setting variables
Variables can be set from the command line either individually using the --variable (-v) option or through variable files with the --variablefile (-V) option. Variables and variable files are explained in separate chapters, but the following examples illustrate how to use these options:

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   --variable name:value
   --variable OS:Linux --variable IP:10.0.0.42
   --variablefile path/to/variables.py
   --variablefile myvars.py:possible:arguments:here
   --variable ENVIRONMENT:Windows --variablefile c:\resources\windows.py
   ```
</details>  
<br />

### Dry run
Robot Framework supports a so-called dry run mode where the tests/tasks are run normally otherwise, but the keywords coming from the libraries are not executed at all. The dry run mode can be used to validate the input data; if the dry run passes, the data should be syntactically correct. This mode is triggered using option --dryrun.

The dry run execution may fail for following reasons:

* Using keywords that are not found.
* Using keywords with wrong number of arguments.
* Using user keywords that have invalid syntax.

In addition to these failures, normal execution errors are shown, for example, when test library or resource file imports cannot be resolved.

It is possible to disable dry run validation of specific user keywords by adding a special robot:no-dry-run keyword tag to them. This is useful if a keyword fails in the dry run mode for some reason, but work fine when executed normally.

> &#128226; _**NOTE:** The dry run mode does not validate variables.

### Randomizing execution order
The execution order can be randomized using option --randomize <what>[:<seed>], where <what> is one of the following:

* `tests`
Test cases inside each test suite are executed in random order.
* `tasks`
RPA tasks inside each suite are executed in random order.
* `suites`
All suites are executed in a random order, but test cases/RPA tasks inside suites are run in the order they are defined.
* `all`
Both test cases/RPA tasks and suites are executed in a random order.
* `none`
Neither execution order of test/task nor suites is randomized. This value can be used to override the earlier value set with --randomize.
It is possible to give a custom seed to initialize the random generator. This is useful if you want to re-run tests/tasks using the same order as earlier. The seed is given as part of the value for --randomize in format <what>:<seed> and it must be an integer. If no seed is given, it is generated randomly. The executed top level suite automatically gets metadata named Randomized that tells both what was randomized and what seed was used.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --randomize tests my_test.robot
   robot --randomize all:12345 path/to/tests
   ```
</details>  
<br />

### Programmatic modification of input data
If the provided built-in features to modify input data before execution are not enough, Robot Framework makes it possible to perform  custom modifications programmatically. This is accomplished by creating a so called pre-run modifier and activating it using the --prerunmodifier option.

Pre-run modifiers should be implemented as visitors that can traverse through the executable suite structure and modify it as needed. The visitor interface is explained as part of the Robot Framework API documentation and it is possible to modify executed suites, test cases/RPA tasks and keywords using it. The examples below are provided to give an idea of how pre-run modifiers can be used and how powerful this functionality is.

When a pre-run modifier is taken into use on the command line using the --prerunmodifier option, it can be specified either as a name of the modifier class or a path to the modifier file. If the modifier is given as a class name, the module containing the class must be in the module search path, and if the module name is different than the class name, the given name must include both like module.ModifierClass. If the modifier is given as a path, the class name must be same as the file name. For most parts this works the same as  when importing a library.

If a modifier requires arguments, as the examples below do, they can be specified after the modifier name or path using either a colon (:) or a semicolon (;) as a separator. If both are used in the value, the one used first is considered to be the actual separator. Starting from Robot Framework 4.0, arguments also support the named argument syntax as well as argument conversion based on type hints and default values the same way as keywords do.

If more than one pre-run modifier is needed, they can be specified by using the --prerunmodifier option multiple times. If similar modifying is needed before creating logs and reports, programmatic modification of results can be enabled using the --prerebotmodifier option.

Pre-run modifiers are executed before other configuration affecting the executed suite and test cases/RPA tasks. Most importantly, options related to selecting test cases are processed after modifiers, making it possible to use options such as --include also with possible dynamically added tests.

> &#128226; _**TIP:** Modifiers are taken into use from the command line exactly the same way as listeners. See the Registering listeners from command line section for more information and examples.

The first example below shows how a pre-run modifier can remove tests from the executed test suite structure. In this example only every Xth tests is preserved, and the X is given from the command line along with an optional start index.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE: Select every Xth test</i></b></summary>

   ```
   """Pre-run modifier that selects only every Xth test for execution.
   
   Starts from the first test by default. Tests are selected per suite.
   """
   
   from robot.api import SuiteVisitor
   
   
   class SelectEveryXthTest(SuiteVisitor):
   
       def __init__(self, x: int, start: int = 0):
           self.x = x
           self.start = start
   
       def start_suite(self, suite):
           """Modify suite's tests to contain only every Xth."""
           suite.tests = suite.tests[self.start::self.x]
   
       def end_suite(self, suite):
           """Remove suites that are empty after removing tests."""
           suite.suites = [s for s in suite.suites if s.test_count > 0]
   
       def visit_test(self, test):
           """Avoid visiting tests and their keywords to save a little time."""
           pass
   ```
</details>  
<br />

If the above pre-run modifier is in a file SelectEveryXthTest.py and the file is in the module search path, it could be used like this:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   # Specify the modifier as a path. Run every second test.
   robot --prerunmodifier path/to/SelectEveryXthTest.py:2 tests.robot
   
   # Specify the modifier as a name. Run every third test, starting from the second.
   robot --prerunmodifier SelectEveryXthTest:3:1 tests.robot
   ```
</details>  
<br />

> &#128226; _**NOTE:** Argument conversion based on type hints such as x: int in the above example is new in Robot Framework 4.0 and requires Python 3.

This second example removes tests, this time based on a given name pattern. In practice it works as a negative version of the built-in --test option.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE: Exclude tests by name</i></b></summary>

   ```
   """Pre-run modifier that excludes tests by their name.
   
   Tests to exclude are specified by using a pattern that is both case and space
   insensitive and supports '*' (match anything) and '?' (match single character)
   as wildcards.
   """
   
   from robot.api import SuiteVisitor
   from robot.utils import Matcher
   
   
   class ExcludeTests(SuiteVisitor):
      
       def __init__(self, pattern):
           self.matcher = Matcher(pattern)
   
       def start_suite(self, suite):
           """Remove tests that match the given pattern."""
           suite.tests = [t for t in suite.tests if not self._is_excluded(t)]
   
       def _is_excluded(self, test):
           return self.matcher.match(test.name) or self.matcher.match(test.longname)
   
       def end_suite(self, suite):
           """Remove suites that are empty after removing tests."""
           suite.suites = [s for s in suite.suites if s.test_count > 0]
      
       def visit_test(self, test):
           """Avoid visiting tests and their keywords to save a little time."""
           pass
   ```
</details>  
<br />

Assuming the above modifier is in a file named ExcludeTests.py, it could be used like this:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   # Exclude test named 'Example'.
   robot --prerunmodifier path/to/ExcludeTests.py:Example tests.robot
   
   # Exclude all tests ending with 'something'.
   robot --prerunmodifier path/to/ExcludeTests.py:*something tests.robot
   ```
</details>  
<br />

Sometimes when debugging, it can be useful to disable setups or teardowns. This can be accomplished by editing the input data, but pre-run modifiers make it easy to do that temporarily for a single run:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE: Disable setups and teardowns</i></b></summary>

   ```
   """Pre-run modifiers for disabling suite and test setups and teardowns."""
   
   from robot.api import SuiteVisitor
   
   
   class SuiteSetup(SuiteVisitor):
   
       def start_suite(self, suite):
           suite.setup = None
   
   
   class SuiteTeardown(SuiteVisitor):
   
       def start_suite(self, suite):
           suite.teardown = None
   
   
   class TestSetup(SuiteVisitor):
   
       def start_test(self, test):
           test.setup = None

   
   class TestTeardown(SuiteVisitor):
   
       def start_test(self, test):
           test.teardown = None
   ```
</details>  
<br />

Assuming that the above modifiers are all in a file named disable.py and this file is in the module search path, setups and teardowns could be disabled, for example, as follows:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   # Disable suite teardowns.
   robot --prerunmodifier disable.SuiteTeardown tests.robot
   
   # Disable both test setups and teardowns by using '--prerunmodifier' twice.
   robot --prerunmodifier disable.TestSetup --prerunmodifier disable.TestTeardown tests.robot
   ```
</details>  
<br />

> &#128226; _**NOTE:** Prior to Robot Framework 4.0 setup and teardown were accessed via the intermediate keywords attribute and, for example, suite setup was disabled like suite.keywords.setup = None.

### Controlling console output
There are various command line options to control how execution is reported on the console.

#### Console output type
The overall console output type is set with the --console option. It supports the following case-insensitive values:

* `verbose`
Every suite and test case/RPA task is reported individually. This is the default.
* `dotted`
Only show . for passed test/tasks, F for failed, s for skipped and x for those which are skipped because of  execution exit. Failed tests/tasks are listed separately after execution. This output type makes it easy to see if there were any failures during execution even if there would be a lot of tests/tasks.
* `quiet`
No output except for errors and warnings.
* `none`
No output whatsoever. Useful when creating a custom output using, for example, listeners.
Separate convenience options --dotted (-.) and --quiet are shortcuts for --console dotted and --console quiet, respectively.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   robot --console quiet tests.robot
   robot --dotted tests.robot
   ```
</details>  
<br />

#### Console width
The width of the test execution output in the console can be set using the option --consolewidth (-W). The default width is 78 characters.

> &#128226; _**TIP:** On many UNIX-like machines you can use handy $COLUMNS environment variable like --consolewidth $COLUMNS.

#### Console colors
The --consolecolors (-C) option is used to control whether colors should be used in the console output. Colors are implemented using ANSI colors except on Windows where, by default, Windows APIs are used instead.

This option supports the following case-insensitive values:

* `auto`
Colors are enabled when outputs are written into the console, but not when they are redirected into a file or elsewhere. This is the default.
* `on`
Colors are used also when outputs are redirected. Does not work on Windows.
* `ansi`
Same as on but uses ANSI colors also on Windows. Useful, for example, when redirecting output to a program that understands ANSI colors.
* `off`
Colors are disabled.

#### Console markers
Special markers . (success) and F (failure) are shown on the console when using the verbose output and top level keywords in test cases/RPA tasks end. The markers allow following the execution in high level, and they are erased when test cases/RPA tasks end.

It is possible to configure when markers are used with --consolemarkers (-K) option. It supports the following case-insensitive values:

* `auto`
Markers are enabled when the standard output is written into the console, but not when it is redirected into a file or elsewhere. This is the default.
* `on`
Markers are always used.
* `off`
Markers are disabled.

### Setting listeners
Listeners can be used to monitor the test execution. When they are taken into use from the command line, they are specified using the --listener command line option. The value can either be a path to a listener or a listener name. See the Listener interface section for more details about importing listeners and using them in general.

## Output files
Several output files are created when tests/tasks are executed and all of them are somehow related to test/task results. This section discusses what outputs are created, how to configure where they are created, and how to fine-tune their contents.

### Different output files
This section explains which different output files can be created and how to configure where they are created. Output files are configured using command line options, which get the path to the output file in question as an argument. A special value NONE (case-insensitive) can be used to disable creating a certain output file.

#### Output directory
All output files can be set using an absolute path, in which case they are created to the specified place, but in other cases, the path is considered relative to the output directory. The default output directory is the directory where the execution is started from, but it can be altered with the --outputdir (-d) option. The path set with this option is, again, relative to the execution directory, but can naturally be given also as an absolute path. Regardless of how a path to an individual output file is obtained, its parent directory is created automatically, if it does not exist already.

#### Output file
Output files contain all the test/task execution results in machine readable XML format. Log, report and xUnit files are typically generated based on them, and they can also be combined and otherwise post-processed with Rebot.

> &#128226; _**TIP:** Generating report and xUnit files as part of execution does not require processing output files after execution. Disabling log generation when running tests can thus save memory.

The command line option --output (-o) determines the path where the output file is created relative to the output directory. The default name for the output file, when tests are run, is output.xml.

When post-processing outputs with Rebot, new output files are not created unless the --output option is explicitly used.

It is possible to disable creation of the output file when running tests/tasks by giving a special value NONE to the --output option. If no outputs are needed, they should all be explicitly disabled using --output NONE --report NONE --log NONE.

The XML output file structure is documented in the robot.xsd schema file.

> &#128226; _**NOTE:** Starting from Robot Framework 7.0, Rebot can read and write JSON output files. The plan is to enhance the support for JSON output files in the future so that they could be created already during execution. For more details see issue #3423.

#### Legacy output file format
There were some backwards incompatible changes to the output file format in Robot Framework 7.0. To make it possible to use new Robot Framework versions with external tools that are not yet updated to support the new format, there is a --legacyoutput option that produces output files that are compatible with Robot Framework 6.x and earlier. Robot Framework itself can process output files both in the old and in the new formats.

We hope that external tools are updated soon, but we plan to support this option at least until Robot Framework 8.0. If you encounter tools that are not compatible, please inform the tool developers about changes.

#### Log file
Log files contain details about the executed test cases/RPA tasks in HTML format. They have a hierarchical structure showing suite, test case/RPA task and keyword details. Log files are needed nearly every time when test/task results are to be investigated in detail. Even though log files also have statistics, reports are better for getting an higher-level overview.

The command line option --log (-l) determines where log files are created. Unless the special value NONE is used, log files are always created and their default name is log.html.

>**TODO:** src/ExecutingTestCases/log_passed.png
An example of beginning of a log file

>**TODO:** src/ExecutingTestCases/log_failed.png
An example of a log file with keyword details visible

>**TODO:** src/ExecutingTestCases/log_skipped.png
An example of a log file with skipped and passed tests

#### Report file
Report files contain an overview of the execution results in HTML format. They have statistics based on tags and executed suites, as well as a list of all executed test cases/RPA tasks. When both reports and logs are generated, the report has links to the log file for easy navigation to more detailed information. It is easy to see the overall execution status from report, because its background color is green, if all tests pass and bright red if any test fails. The background can also be yellow, which means that all tests were skipped.

The command line option --report (-r) determines where report files are created. Similarly as log files, reports are always created unless NONE is used as a value, and their default name is report.html.

>**TODO:** src/ExecutingTestCases/report_passed.png
An example report file of successful test execution

>**TODO:** src/ExecutingTestCases/report_failed.png
An example report file of failed test execution

>**TODO:** Yellow file example?

#### XUnit compatible result file
XUnit result files contain the execution summary in xUnit-compatible XML format. These files can thus be used as an input for external tools that understand xUnit reports. For example, Jenkins continuous integration server supports generating statistics based on xUnit compatible results.

> &#128226; _**TIP:** Jenkins also has a separate Robot Framework plugin.

XUnit output files are not created unless the command line option --xunit (-x) is used explicitly. This option requires a path to the generated xUnit file, relatively to the output directory, as a value.

>**TODO:** Include RPA below - <testsuite> version?

XUnit output files were changed pretty heavily in Robot Framework 5.0. They nowadays contain separate <testsuite> elements for each suite, <testsuite> elements have timestamp attribute, and suite documentation and metadata is stored as <property> elements.

#### Debug file
Debug files are plain text files which are written during the execution. All messages obtained from libraries are written to them, as well as information about started and ended suites, test cases/RPA tasks and keywords. Debug files can be used for monitoring the test execution. This can be done using, for example, a separate fileviewer.py tool, or in UNIX-like systems, simply with the tail -f command.

Debug files are not created unless the command line option --debugfile (-b) is used explicitly.

#### Timestamping output files
All output files generated by Robot Framework itself can be automatically timestamped with the option --timestampoutputs (-T). When this option is used, a timestamp in the format YYYYMMDD-hhmmss is placed between the extension and the base name of each file. The example below would, for example, create output files such as output-20080604-163225.xml and mylog-20080604-163225.html:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --timestampoutputs --log mylog.html --report NONE tests.robot
   ```
</details>  
<br />

#### Setting titles
The default titles for logs and reports are generated by prefixing the name of the top-level suite with Test/Task Log or Test/Task Report. Custom titles can be given from the command line using the options --logtitle and --reporttitle, respectively.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   robot --logtitle "Smoke Test Log" --reporttitle "Smoke Test Report" --include smoke my_tests/
   ```
</details>  
<br />

> &#128226; _**NOTE:** Prior to Robot Framework 3.1, underscores in the given titles were converted to spaces. Nowadays spaces need to be escaped or quoted as in the example above.

#### Setting background colors
By default the report file has a red background if there are failures, a green background if there are passed tests and possibly some skipped ones, and a yellow background if all tests/tasks are skipped or no tests/tasks have been run. These colors can be customized by using the --reportbackground command line option, which takes two or three colors separated with a colon as an argument:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --reportbackground blue:red
   --reportbackground blue:red:orange
   --reportbackground #00E:#E00
   ```
</details>  
<br />

If you specify two colors, the first one will be used instead of the default green (pass) color and the second instead of the default red (fail). This allows, for example, using blue instead of green to make backgrounds easier to separate for color blind people.

If you specify three colors, the first two have same semantics as earlier and the last one replaces the default yellow (skip) color.

The specified colors are used as a value for the body element's background CSS property. The value is used as-is and can be a HTML color name (e.g. red), a hexadecimal value (e.g. #f00 or #ff0000), or an RGB value (e.g. rgb(255,0,0)). The default green, red and yellow colors are specified using hexadecimal values #9e9, #f66 and #fed84f, respectively.

### Log levels
#### Available log levels
Messages in log files can have different log levels. Some of the messages are written by Robot Framework itself, but also executed keywords can log information using different levels. The available log levels are:

* `FAIL`
Used when a keyword fails. Can be used only by Robot Framework itself.
* `WARN`
Used to display warnings. They shown also in the console and in the Test/Task Execution Errors section in log files, but they do not affect the test case/RPA task status.
* `INFO`
The default level for normal messages. By default, messages below this level are not shown in the log file.
* `DEBUG`
Used for debugging purposes. Useful, for example, for logging what libraries are doing internally. When a keyword fails, a traceback showing where in the code the failure occurred is logged using this level automatically.
* `TRACE`
More detailed debugging level. The keyword arguments and return values are automatically logged using this level.

#### Setting log level
By default, log messages below the INFO level are not logged, but this threshold can be changed from the command line using the --loglevel (-L) option. This option takes any of the available log levels as an argument, and that level becomes the new threshold level. A special value NONE can also be used to disable logging altogether.

It is possible to use the --loglevel option also when post-processing outputs with Rebot. This allows, for example, running tests/tasks initially with the TRACE level, and generating smaller log files for normal viewing later with the INFO level. By default all the messages included during execution will be included also with Rebot. Messages ignored during the execution cannot be recovered.

Another possibility to change the log level is using the BuiltIn keyword Set Log Level in the input data. It takes the same arguments as the --loglevel option, and it also returns the old level so that it can be restored later, for example, in a test teardown.

#### Visible log level
If the log file contains messages at DEBUG or TRACE levels, a visible log level drop down is shown in the upper right corner. This allows users to remove messages below chosen level from the view. This can be useful especially when running test at TRACE level.

>**TODO:** src/ExecutingTestCases/visible_log_level.png
An example log showing the visible log level drop down

By default the drop down will be set at the lowest level in the log file, so that all messages are shown. The default visible log level can be changed using --loglevel option by giving the default after the normal log level separated by a colon:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --loglevel DEBUG:INFO
   ```
</details>  
<br />

In the above example, tests/tasks are run using level DEBUG, but the default visible level in the log file is INFO.

### Splitting logs
Normally the log file is just a single HTML file. When the amount of the test cases/RPA tasks increases, the size of the file can grow so large that opening it into a browser is inconvenient or even impossible. Hence, it is possible to use the --splitlog option to split parts of the log into external files that are loaded transparently into the browser when needed.

The main benefit of splitting logs is that individual log parts are so small that opening and browsing the log file is possible even if the amount of the input data is very large. A small drawback is that the overall size taken by the log file increases.

Technically the input data related to each test case/RPA task is saved into a JavaScript file in the same folder as the main log file. These files have names such as log-42.js where log is the base name of the main log file and 42 is an incremented index.

> &#128226; _**NOTE:** When copying the log files, you need to copy also all the log-*.js files or some information will be missing.

### Configuring statistics
There are several command line options that can be used to configure and adjust the contents of the Statistics by Tag, Statistics by Suite and Test/Task Details by Tag tables in different output files. All these options work both when executing test cases/RPA tasks and when post-processing outputs.

#### Configuring displayed suite statistics
When a deeper suite structure is executed, showing all the suite levels in the Statistics by Suite table may make the table somewhat difficult to read. By default all suites are shown, but you can control this with the command line option --suitestatlevel which takes the level of suites to show as an argument:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --suitestatlevel 3
   ```
</details>  
<br />

#### Including and excluding tag statistics
When many tags are used, the Statistics by Tag table can become quite congested. If this happens, the command line options --tagstatinclude and --tagstatexclude can be used to select which tags to display, similarly as --include and --exclude are used to select test cases/RPA tasks:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --tagstatinclude some-tag --tagstatinclude another-tag
   --tagstatexclude owner-*
   --tagstatinclude prefix-* --tagstatexclude prefix-13
   ```
</details>  
<br />

### Generating combined tag statistics
The command line option --tagstatcombine can be used to generate aggregate tags that combine statistics from multiple tags. The combined tags are specified using tag patterns where * and ? are supported as wildcards and AND, OR and NOT operators can be used for combining individual tags or patterns together.

The following examples illustrate creating combined tag statistics using different patterns, and the figure below shows a snippet of the resulting Statistics by Tag table:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --tagstatcombine owner-*
   --tagstatcombine smokeANDmytag
   --tagstatcombine smokeNOTowner-janne*
   ```
</details>  
<br />

>**TODO:** src/ExecutingTestCases/tagstatcombine.png
Examples of combined tag statistics

As the above example illustrates, the name of the added combined statistic is, by default, just the given pattern. If this is not good enough, it is possible to give a custom name after the pattern by separating them with a colon (:):

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --tagstatcombine "prio1ORprio2:High priority tests"   
   ```
</details>  
<br />

> &#128226; _**NOTE:** Prior to Robot Framework 3.1, underscores in the custom name were converted to spaces. Nowadays spaces need to be escaped or quoted as in the example above.

#### Creating links from tag names
You can add external links to the Statistics by Tag table by using the command line option --tagstatlink. Arguments to this option are given in the format tag:link:name, where tag specifies the tags to assign the link to, link is the link to be created, and name is the name to give to the link.

tag may be a single tag, but more commonly a simple pattern where * matches anything and ? matches any single character. When tag is a pattern, the matches to wildcards may be used in link and title with the syntax %N, where "N" is the index of the match starting from 1.

The following examples illustrate the usage of this option, and the figure below shows a snippet of the resulting Statistics by Tag table when example input data is executed with these options:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   --tagstatlink mytag:http://www.google.com:Google
   --tagstatlink example-bug-*:http://example.com
   --tagstatlink owner-*:mailto:%1@domain.com?subject=Acceptance_Tests:Send_Mail
   ```
</details>  
<br />

>**TODO:** src/ExecutingTestCases/tagstatlink.png
Examples of links from tag names

#### Adding documentation to tags
Tags can be given a documentation with the command line option --tagdoc, which takes an argument in the format tag:doc. tag is the name of the tag to assign the documentation to and it can also be a simple pattern matching multiple tags. doc is the assigned documentation. It can contain simple HTML formatting.

The given documentation is shown with matching tags in the Test/Task Details by Tag table, and as a tool tip for these tags in the Statistics by Tag table. If one tag gets multiple documentations, they are combined together and separated with an ampersand.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   --tagdoc mytag:Example
   --tagdoc "regression:*See* http://info.html"
   --tagdoc "owner-*:Original author"
   ```
</details>  
<br />

> &#128226; _**NOTE:** Prior to Robot Framework 3.1, underscores in the documentation were converted to spaces. Nowadays spaces need to be escaped or quoted as in the examples above.

### Removing and flattening keywords
Most of the content of output files comes from keywords and their log messages. When creating higher level reports, log files are not necessarily needed at all and in that case keywords and their messages just take space unnecessarily. Log files themselves can also grow overly large, especially if they contain FOR loops or other constructs that repeat certain keywords multiple times.

In these situations, command line options --removekeywords and --flattenkeywords can be used to dispose or flatten unnecessary keywords. They can be used both when executing test cases/RPA tasks and when post-processing outputs. When used during execution, they only affect the log file, not the XML output file. With rebot they affect both logs and possibly generated new output XML files.

#### Removing keywords
The --removekeywords option removes keywords and their messages altogether. It has the following modes of operation, and it can be used multiple times to enable multiple modes. Keywords that contain errors or warnings are not removed except when using the ALL mode.

* `ALL`
Remove data from all keywords unconditionally.
* `PASSED`
Remove keyword data from passed test cases/RPA tasks. In most cases, log files created using this option contain enough information to investigate possible failures.
* `FOR`
Remove all passed iterations from FOR loops except the last one.
* `WHILE`
Remove all passed iterations from WHILE loops except the last one.
* `WUKS`
Remove all failing keywords inside BuiltIn keyword Wait Until Keyword Succeeds except the last one.
* `NAME:<pattern>`
Remove data from all keywords matching the given pattern regardless the keyword status. The pattern is matched against the full name of the keyword, prefixed with the possible library or resource file name such as MyLibrary.Keyword Name. The pattern is case, space, and underscore insensitive and it supports simple patterns with *, ? and [] as wildcards.
* `TAG:<pattern>`
Remove data from keywords with tags that match the given pattern. Tags are case and space insensitive and they can be specified using tag patterns where *, ? and [] are supported as wildcards and AND, OR and NOT operators can be used for combining individual tags or patterns together. Can be used both with library keyword tags and user keyword tags.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   rebot --removekeywords all --output removed.xml output.xml
   robot --removekeywords passed --removekeywords for tests.robot
   robot --removekeywords name:HugeKeyword --removekeywords name:resource.* tests.robot
   robot --removekeywords tag:huge tests.robot
   ```
</details>  
<br />

Removing keywords is performed after parsing the output file and generating an internal model based on it. Thus it does not reduce memory usage as much as flattening keywords.

Flattening keywords
The --flattenkeywords option flattens matching keywords. In practice this means that matching keywords get all log messages from their child keywords, recursively, and child keywords are discarded otherwise. Flattening supports the following modes:

* `FOR`
Flatten FOR loops fully.
* `WHILE`
Flatten WHILE loops fully.
* `ITERATION`
Flatten individual FOR and WHILE loop iterations.
* `FORITEM`
Deprecated alias for ITERATION.
* `NAME:<pattern>`
Flatten keywords matching the given pattern. Pattern matching rules are same as when removing keywords using the NAME:<pattern> mode.
* `TAG:<pattern>`
Flatten keywords with tags matching the given pattern. Pattern matching rules are same as when removing keywords using the TAG:<pattern> mode.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   robot --flattenkeywords name:HugeKeyword --flattenkeywords name:resource.* tests.robot
   rebot --flattenkeywords foritem --output flattened.xml original.xml
   ```
</details>  
<br />

Flattening keywords is performed already when the output file is parsed initially. This can save a significant amount of memory especially with deeply nested keyword structures.

#### Flattening keyword during execution time
Starting from Robot Framework 6.1, it is possible to enable the keyword flattening during the execution time. This can be done only on an user keyword level by defining the reserved tag robot:flatten as a keyword tag. Using this tag will work similarly as the command line option described in the previous chapter, e.g. all content except for log messages is removed from under the keyword having the tag. One important difference is that in this case, the removed content is not written to the output file at all, and thus cannot be accessed at a later time.

***
<details>
  <summary>&#129302; <b><i>SOME EXAMPLES:</i></b></summary>

   ```
   *** Keywords ***
   Flattening affects this keyword and all it's children
       [Tags]    robot:flatten
       Log    something
       FOR     ${i}     IN RANGE     2
            Log    The message is preserved but for loop iteration is not
       END
   
   *** Settings ***
   # Flatten content of all uer keywords
   Keyword Tags    robot:flatten
   ```
</details>  
<br />

### Automatically expanding keywords
Keywords which have passed are closed in the log file by default. Thus information they contain is not visible unless you expand them. If certain keywords have important information that should be visible when the log file is opened, you can use the --expandkeywords option to set keywords automatically expanded in log file similar to failed keywords. Expanding supports the following modes:

* `NAME:<pattern>`
Expand keywords matching the given pattern. Pattern matching rules are same as when removing keywords using the NAME:<pattern> mode.
* `TAG:<pattern>`
Expand keywords with tags matching the given pattern. Pattern matching rules are same as when removing keywords using the TAG:<pattern> mode.
If you need to expand keywords matching different names or patterns, you can use the --expandkeywords multiple times.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   robot --expandkeywords name:SeleniumLibrary.CapturePageScreenshot tests.robot
   rebot --expandkeywords tag:example --expandkeywords tag:another output.xml
   ```
</details>  
<br />

> &#128226; _**NOTE:** The --expandkeywords option is new in Robot Framework 3.2.

### Setting start and end time of execution
When combining outputs using Rebot, it is possible to set the start and end time of the combined test suite/RPA task using the options --starttime and --endtime, respectively. This is convenient, because by default, combined suites do not have these values. When both the start and end time are given, the elapsed time is also calculated based on them. Otherwise the elapsed time is obtained by adding the elapsed times of the child test suites together.

It is also possible to use the above-mentioned options to set start and end times for a single suite when using Rebot. Using these options with a single output always affects the elapsed time of the suite.

Times must be given as timestamps in the format YYYY-MM-DD hh:mm:ss.mil, where all separators are optional and the parts from milliseconds to hours can be omitted. For example, 2008-06-11 17:59:20.495 is equivalent both to 20080611-175920.495 and 20080611175920495, and also mere 20080611 would work.

***
<details>
  <summary>&#129302; <b><i>EXAMPLES:</i></b></summary>

   ```
   rebot --starttime 20080611-17:59:20.495 output1.xml output2.xml
   rebot --starttime 20080611-175920 --endtime 20080611-180242 *.xml
   rebot --starttime 20110302-1317 --endtime 20110302-11418 myoutput.xml
   ```
</details>  
<br />

### Limiting error message length in reports
If a test case/RPA task fails and has a long error message, the message shown within reports is automatically cut from the middle to keep reports easier to read. By default messages longer than 40 lines are cut, but that can be configured by using the --maxerrorlines command line option. The minimum value for this option is 10, and it is also possible to use a special value NONE to show the full message.

Full error messages are always visible in log files as messages of the failed keywords.

> &#128226; _**NOTE:** The --maxerrorlines option is new in Robot Framework 3.1.

### Programmatic modification of results
If the provided built-in features to modify results are not enough, Robot Framework makes it possible to perform custom modifications programmatically. This is accomplished by creating a model modifier and activating it using the --prerebotmodifier option.

This functionality works nearly the same as programmatic modification of input data which can be enabled with the --prerunmodifier option. The obvious difference is that this time modifiers operate with the result model, not the running model. For example, the following modifier marks all passed tests that have taken more time than allowed as failed:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
    from robot.api import SuiteVisitor
    
    
    class ExecutionTimeChecker(SuiteVisitor):
    
        def __init__(self, max_seconds: float):
            self.max_milliseconds = max_seconds * 1000
    
        def visit_test(self, test):
            if test.status == 'PASS' and test.elapsedtime > self.max_milliseconds:
                test.status = 'FAIL'
                test.message = 'Test execution took too long.'
   ```
</details>  
<br />

If the above modifier would be in file ExecutionTimeChecker.py, it could be used, for example, similar to this:

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   # Specify modifier as a path when running tests. Maximum time is 42 seconds.
   robot --prerebotmodifier path/to/ExecutionTimeChecker.py:42 tests.robot
   
   # Specify modifier as a name when using Rebot. Maximum time is 3.14 seconds.
   # ExecutionTimeChecker.py must be in the module search path.
   rebot --prerebotmodifier ExecutionTimeChecker:3.14 output.xml
   ```
</details>  
<br />

If more than one model modifier is needed, they can be specified by using the --prerebotmodifier option multiple times. When executing tests, it is possible to use --prerunmodifier and --prerebotmodifier options together.

> &#128226; _**NOTE:** Argument conversion based on type hints like max_seconds: float in the above example is new in Robot Framework 4.0 and requires Python 3.

### System log
Robot Framework has its own plain-text system log where it writes information about

* Processed and skipped input data files
* Imported test libraries, resource files and variable files
* Executed test suites and test cases
* Created outputs

Normally users never need this information, but it can be useful when investigating problems with test libraries or Robot Framework itself. A system log is not created by default, but it can be enabled by setting the environment variable ROBOT_SYSLOG_FILE so that it contains a path to the selected file.

A system log has the same log levels as a normal log file, with the exception that instead of FAIL it has the ERROR level. The threshold level to use can be altered using the ROBOT_SYSLOG_LEVEL environment variable like shown in the example below. Possible unexpected errors and warnings are written into the system log in addition to the console and the normal log file.

***
<details>
  <summary>&#129302; <b><i>EXAMPLE:</i></b></summary>

   ```
   #!/bin/bash
   
   export ROBOT_SYSLOG_FILE=/tmp/syslog.txt
   export ROBOT_SYSLOG_LEVEL=DEBUG
   
   robot --name Syslog_example path/to/tests
   ```
</details>  
<br />
