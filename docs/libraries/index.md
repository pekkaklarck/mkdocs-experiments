# Standard libraries

Standard libraries are distributed with Robot Framework as part of a normal installation.
Some of them have external dependencies that need to be installed before they can
be used, though. See library documentations themselves for more details about possible
dependencies and libraries in general.

## Library documentation

The following table contains links to standard library documentation in external
files.

| Library                                                     | Description                                                                                |
|-------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [BuiltIn](BuiltIn.html)                                     | Contains generic often needed keywords. Imported automatically and thus always available.  |
| [Collections](Collections.html)                             | Contains keywords for handling lists and dictionaries.                                     |
| [DateTime](DateTime.html)                                   | Supports creating and verifying date and time values as well as calculations between them. |
| [Dialogs](Dialogs.html)                                     | Supports pausing the test execution and getting input from users.                          |
| [OperatingSystem](OperatingSystem.html)                     | Enables performing various operating system related tasks.                                 |
| [Process](Process.html)                                     | Supports executing processes in the system.                                                |
| [Remote](https://github.com/robotframework/RemoteInterface) | Part of the remote library interface. Does not have any keywords of its own.               |
| [Screenshot](Screenshot.html)                               | Provides keywords to capture and store screenshots of the desktop.                         |
| [String](String.html)                                       | Library for manipulating strings and verifying their contents.                             |
| [Telnet](Telnet.html)                                       | Supports connecting to Telnet servers and executing commands on the opened connections.    |
| [XML](XML.html)                                             | Library for verifying and modifying XML documents.                                         |

## Spec files

Standard library spec files are hosted here as well. They contain library information
in JSON format and can be used by external tools such as editors.

- [BuiltIn](BuiltIn.json)                
- [Collections](Collections.json)        
- [DateTime](DateTime.json)              
- [Dialogs](Dialogs.json)                
- [OperatingSystem](OperatingSystem.json)
- [Process](Process.json)                
- [Screenshot](Screenshot.json)          
- [String](String.json)                  
- [Telnet](Telnet.json)                  
- [XML](XML.json)                        
