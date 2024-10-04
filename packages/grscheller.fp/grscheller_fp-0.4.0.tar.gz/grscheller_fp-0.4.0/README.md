# Python Functional Programming (FP)

Functional programming tools which endeavor to be Pythonic.

* **Repositories**
  * [grscheller.fp][1] project on *PyPI*
  * [Source code][2] on *GitHub*
* Detailed documentation for grscheller.datastructures
  * [Detailed API documentation][3] on *GH-Pages*

### Modules

* grscheller.fp.iterables
  * iteration tools implemented in Python
* grscheller.fp.nothingness
  * singleton `noValue` representing a missing value.
    * similar to `None` but while
      * `None` represent "returned no values"
      * `noValue: _NoValue = _NoValue()` represents the absence of a value
* grscheller.fp.woException
  * tools for handling "exceptional" events without exceptions

### Benefits of FP

* improved composability
* avoid exception driven code paths
* data sharing becomes trivial due to immutability

---

[1]: https://pypi.org/project/grscheller.fp/
[2]: https://github.com/grscheller/fp/
[3]: https://grscheller.github.io/fp/
