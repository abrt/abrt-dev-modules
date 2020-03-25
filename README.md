<p align="center">
<a href="https://retrace.fedoraproject.org/">
    <img alt="ABRT" src="https://github.com/abrt/abrt/blob/master/icons/hicolor_apps_scalable_abrt.svg" width="128">
</a>  
</p>
<h1 align=center>sABRTooth Python</h1>
<h6 align=center>Developer module for error and exception tracking in Python applications</h6>

***

**sABRTooth** automatically captures errors and exceptions in your applications and collects important data for easier debugging.
Captured errors and exceptions are reported to [ABRT Analytics](https://retrace.fedoraproject.org/faf) without any user interation.

Features
---
**Automatic error monitoring and reporting** - Exceptions and errors in Python are automatically captured and reported.  


Using sABRTooth
---
1) Install `sABRTooth`.  
On Fedora:
``` bash
$ dnf install python3-sabrtooth
```
2) Generate a key for your project on [retrace.fedoraproject.org/faf/projects](https://retrace.fedoraproject.org/faf).  
3) Import `sABRTooth` into your project and initialize it with your project's key.
``` python3
import sabrtooth

sabrtooth.init($your_projects_key)
```

Contributing to sABRTooth
---
Please read the [contribution guide](https://github.com/abrt/sABRTooth-python/blob/master/CONTRIBUTION.md) before contribution to `sABRTooth-python`.
  
  
Related projects
---
[abrt](https://github/abrt/abrt)  
[libreport](https://github/abrt/abrt)  
[satyr](https://github/abrt/abrt)  
[ABRT Analytics](https://github.com/abrt/faf)
