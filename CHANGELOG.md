## [v2.0.1] - 2026-04-02

### Added
- **Option to choose where to put the file** to be able to put your files in global/ and that everyone can access.

### Changed
- **We fixed the annoying bug that does not include global in the list of available files** so you can access all the files that others put there.

### Technical
- we added a new protocol with the `USERS` key, which allows us to list the available users to be able to put a file.
- We fixed the error that the `GUI.py` windows were bugged when we logged in

### Breaking Changes
- **Protocol update required:** Now with the new `USERS` protocol it is necessary for both client and server to be updated