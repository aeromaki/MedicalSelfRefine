# What the STOP rules detect

The examples below are schematic format illustrations, not additional experimental prompt examples. Actual preserved responses are in the 171-case files and historical result JSONs.

The exact terminal rule accepts this at the end of the response (trailing whitespace is permitted):

````text
```STOP```
````

The whitespace/case-tolerant terminal rule additionally accepts formatting such as:

````text
```
STOP
```
````

````text
``` stop ```
````

The historical detector searches anywhere in a lowercased response for any of these strings:

````text
`stop`
'stop'
"stop"
````

It does not require that the match be at the end of the response. A difference in matching rules establishes a format/detection discrepancy; it does not by itself establish that a model intended to continue or that a clinically incorrect stop occurred.
