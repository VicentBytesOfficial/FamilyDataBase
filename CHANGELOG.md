## [v1.2.0] - 2026-04-02

### Added
- **Automatic login** option, allowing users to skip manual credential entry on startup.
- **File autocompletion** in `CTkEntry` fields, enabling users to browse and select available files directly from the input.
- New `FILES` key in the client-server communication protocol for file-related operations.

### Changed
- **Migrated the entire GUI** from `tkinter` to `customtkinter`, delivering a modern and visually consistent interface.

### Technical
- The client-server communication protocol uses a `;`-separated message structure: `content_type;content;more_content;etc`. The `FILES` key has been added to the existing `GET`, `PUT`, and `LOGIN` keys. A `FILES` response follows the format `FILES;file1;file2;...`. Both server and client components have been updated accordingly.

### Breaking Changes
- **Protocol update required:** The addition of the `FILES` key means older clients are not compatible with the updated server and vice versa. Both sides must be updated to `v1.2.0` simultaneously.
- **New dependency:** `customtkinter` is now required. Install it with:
```
  pip install customtkinter
```