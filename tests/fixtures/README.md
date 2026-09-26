# Formula regression fixture

`excel_saved_formulas.xlsx` contains only invented test data. It was created,
recalculated with CalculateFullRebuild, and saved by Microsoft Excel 16.0 on
Windows on 2026-09-26 using `../create_excel_fixture.ps1`.

The first row uses formulas for text IDs, descriptive fields, and numeric
frequency. The reader must use their saved results without evaluating formulas.
Unit tests separately cover unavailable results, Excel errors, and reader-exposed
empty strings. A formula exposed as None is unavailable, even when Excel shows
it as blank; use a literal blank in an optional field in that case. The generator
does not inspect XLSX XML to distinguish these states.

Excel is needed only to regenerate this development fixture, not to run tests
against the saved fixture or to run the generator.
