# sABRTooth-python
Developer module for error and exception tracking in Python applications

---

sABRTooth aims to automatically capture application errors and report them to
[ABRT Analytics](https://github.com/abrt/faf) for easier tracking and monitoring.

---

## Example usage

Warning: `allow-unpackaged = True` needs to be set in ABRT Analytics.

``` python3
import sabrtooth


NAME = "application"
VERSION = "1.0"
FAF_URI = "http://localhost:8080/faf/" # ABRT Analytics instance to use for reporting

sabrtooth.register(NAME, VERSION, FAF_URI)

0/0
```
