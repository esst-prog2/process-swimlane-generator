## ADDED Requirements

### Requirement: Optional paired viewer output
The CLI SHALL accept `--viewer` to create a self-contained HTML viewer alongside the SVG. Without this option the existing SVG command, naming and diagnostics SHALL remain compatible. With the option, both outputs SHALL use the same first available base or ascending numbered stem in `output/`, considering collisions in either format. Existing files SHALL never be overwritten, including competing publications. Rendering of both formats SHALL finish before publication. Handled publication failures SHALL roll back newly published members, clean staging files and report failure without claiming success; if cleanup itself fails the terminal SHALL explicitly identify the incomplete output and cleanup problem. Success SHALL print both paths and identify the HTML as the file to open for frozen labels.

#### Scenario: Viewer requested
- **WHEN** a valid workbook is processed with `--viewer`
- **THEN** matching SVG and HTML files are published and their paths and viewer opening guidance are printed

#### Scenario: Default command
- **WHEN** the same workbook is processed without `--viewer`
- **THEN** only an SVG is published using existing SVG-only numbering

#### Scenario: Either extension occupied
- **WHEN** the SVG or HTML filename exists or is claimed during publication
- **THEN** the pair uses the next jointly available suffix and all preexisting or competing files remain unchanged

#### Scenario: Render or second publication fails
- **WHEN** rendering, staging or publication of either member fails
- **THEN** the command returns nonzero, preserves previous files, removes newly published members and temporary files, and does not print success

#### Scenario: Cleanup denied
- **WHEN** the operating system also refuses removal during failure rollback
- **THEN** the command returns nonzero and identifies the incomplete output paths and cleanup error for manual recovery
