# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-05-30
### Added
- Initial release
- - Supports SHORT_ANSWER, and MULTIPLE_CHOICE questions
- - Suports plusminus parsing of variable, answer, and alt_answer expressions
- - Supports optional question associated images
- -- Currently there is only one image for each question across all generated versions of the exam,
    so images should reference variable names in the question text rather than having hardcoded values.
- - Supports limited HTML with embedded python string formatting expressions for
- -- Front matter pages
- -- Back matter pages
- -- Section headers
- -- Question text
- -- Solution text

[Unreleased]: https://github.com/malcolm-3/ExamMaker/compare/0.1.0...master
[0.1.0]: https://github.com/malcolm-3/ExamMaker/tree/0.1.0

