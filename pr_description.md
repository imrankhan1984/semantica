## Description

Fixes two gaps that made Turtle/TTL export inaccessible:

1. `format="ttl"` raised a `ValidationError` because `"ttl"` was not accepted as an alias for `"turtle"` in `RDFExporter`, even though it is the standard file extension.
2. `RDFExporter` was never introduced in `cookbook/introduction/15_Export.ipynb`, so users following the default learning path had no way to discover TTL export.

## Type of Change

- [x] Bug fix (non-breaking change which fixes an issue)
- [x] Documentation update

## Related Issues

Closes #355

## Changes Made

- `semantica/export/rdf_exporter.py`: Added `_format_aliases` dict in `RDFExporter.__init__()` mapping common shorthands to canonical format names (`ttl→turtle`, `nt→ntriples`, `xml→rdfxml`, `rdf→rdfxml`, `json-ld→jsonld`). Added one-line alias resolution at the top of `export_to_rdf()` before format validation — all existing callers using canonical names are unaffected.
- `cookbook/introduction/15_Export.ipynb`: Added a code cell in Step 3 (RDF Export) demonstrating `format="ttl"` and `validate_rdf()`.
- `tests/export/test_rdf_exporter.py`: New test file with 8 tests covering alias parity, canonical formats, unsupported format error, and file export with `format="ttl"`.

## Testing

- [x] Tested locally
- [x] Added tests for new functionality
- [x] Package builds successfully (`python -m build`)

### Test Commands

```bash
# Run new RDF exporter tests
pytest tests/export/test_rdf_exporter.py -v

# Verify the original bug is fixed
python -c "
from semantica.export import RDFExporter
exporter = RDFExporter()
rdf_data = {
    'entities': [
        {'id': 'e1', 'text': 'Apple Inc.', 'type': 'ORG', 'confidence': 0.95},
        {'id': 'e2', 'text': 'Steve Jobs', 'type': 'PERSON', 'confidence': 0.97},
    ],
    'relationships': [
        {'source_id': 'e2', 'target_id': 'e1', 'type': 'founded_by', 'confidence': 0.91},
    ],
}
exporter.export(rdf_data, 'output.ttl', format='ttl')
print('format=ttl works correctly')
"

# Full test suite
pytest tests/
```

## Documentation

- [x] Updated relevant documentation
- [x] Added code examples if applicable
- [x] Updated cookbook if adding new examples

## Breaking Changes

**Breaking Changes**: No

All existing callers using canonical format names (`"turtle"`, `"rdfxml"`, `"jsonld"`, `"ntriples"`, `"n3"`) are completely unaffected. The alias map is purely additive.

## Checklist

- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my code
- [x] My changes generate no new warnings
- [x] Package builds successfully

## Additional Notes

The alias resolution uses `.lower()` on the input before lookup, so `"TTL"`, `"Ttl"`, etc. also work. No public API signatures were changed.
