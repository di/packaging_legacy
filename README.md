# Legacy Packaging

This library provides support for "legacy" Python Packaging functionality
removed from https://github.com/pypa/packaging.


## Supported APIs

This library includes support for the following deprecated/removed APIs:

### `LegacyVersion`
Removed in https://github.com/pypa/packaging/pull/407, this includes a
`packaging_legacy.version.parse` function that handles legacy versions.

```diff
- from packaging.version import parse, LegacyVersion
+ from packaging_legacy.version import parse, LegacyVersion
```
