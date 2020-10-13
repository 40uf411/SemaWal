# SemaWal Semantic network resolver
<div style="text-align:center">
<img src="logo.png" alt="SemaWal logo" style="width:250px;"/>
</div>
SemaWal is a semantic network resolver in python

<!--![arrand logo](doc/arrand_header.png  "arrand logo")-->
<!--![PyPI - Downloads](https://img.shields.io/pypi/dm/arrand)-->

  Developper:  Ali AOUF

Features |   value
---------|---------------------------------------------------------------------------------
Authors  | [Authors.md](https://github.com/40uf411/SemaWal/master/AUTHORS.md)
Release  | 0.2 (20.10)
License  |[GPL](https://github.com/40uf411/SemaWal/master/LICENSE)
Tracker  |[40uf411/arrand/Issues](https://github.com/40uf411/SemaWal/issues)
Source  |[Github](http://github.com/40uf411/SemaWal)
Feedbacks  |[Comments](https://github.com/40uf411/SemaWal/)
Accounts  |[@Twitter](https://twitter.com/40uf411)

## **Description**

SemaWal Is a semantic network resolver developed as a python library. 
It allows the creation of networks through manual coding or a JSON file. It supports a variety of connection types between nodes.
SemaWal provides useful network defining functions and knowledge extraction functions, these functions allows for network browsing, path finding, pattern checking and more.

###  Features:
* Support for multi-relations(connections between nodes).
* Support for extend relation(inheritance).
* Support for positive and negative relations.
* Support for JSON files.
* Support for node properties.
* Support for Sub-networks.
* Relations extraction.
* Pattern checking.
* Advanced filtered search.
* Path finding.
* Static graph generation.
---
### Changelog:
#### 0.2(20.10)
	- New code (Node and Net classes rewritten from scratch)
	- Allowing power value to be and integer between 0 and 10 (old: 0 or 1)
	- Adding JSON support
	- Adding a function to look for pattern (Beta)
	- Deprecating the CSV parser
	- Deprecating the tkinter based GUI
#### 0.1(20.08)
	- initial release
### In progress features
* A GUI interface
* A web interface
* An option to ignore certain relations

**Full documentation:** [https://40uf411.github.io/SemaWal/](https://40uf411.github.io/SemaWal/)