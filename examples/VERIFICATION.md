# Verification performed during preparation

- Python runtime: see `actual_outputs.json`.
- scikit-learn version: 1.8.0.
- Five unit tests passed: source-backed similarity answer, REALM training query, unsupported query, paper filtering, invalid input.
- HTTP checks passed: `/health`, page response, `/api/ask` answer/citation, HTTP 400 for an empty question.
- Six actual demo requests are recorded in `actual_outputs.json`.
- Automated visual browser verification could not run because the environment lacks an installed browser executable. No screenshot is bundled or claimed as verified.

Run the app on your machine, check the interface, and capture a screenshot of a supported answer with its source link before publishing on LinkedIn. These development checks are not a held-out accuracy evaluation.
