# CHANGELOG

PyPI grscheller.untyped project.

#### Semantic versioning

* first digit
  * major event, epoch, or paradigm shift
* second digit
  * breaking API changes
  * major changes
* third digit
  * API additions
  * bug fixes
  * minor changes
  * significant documentation updates
* forth digit (development environment only)
  * commit count of "non-trivial" changes/regressions

## Releases and Important Milestones

### Version 0.3.0 - PyPI Release: 2024-10-02

* renamed untyped.nothing to untyped.nada
  * Nothing -> Nada
  * nothing -> nada

### Version 0.2.0 - PyPI Release: 2024-08-17

* typing improvements back-ported from grscheller.fp
* updated optional dependencies to use grscheller.circular-array 3.4.0
  * for tests/

### Version 0.1.1 - PyPI Release: 2024-08-12

* prototype of a module level inaccessible sentinel value
  * _nothing_nada: _Nothing_Nada
  * for use only within the grscheller.untyped module itself

### Version 0.1.0 - Initial PyPI Release: 2024-08-08

* moved module nothing from grscheller.fp
  * wanted everything in grscheller.fp strictly typed
  * felt class Nothing worked better untyped
    * at least marginally typed with Any
