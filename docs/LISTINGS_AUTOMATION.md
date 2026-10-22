# Controlled listings monitoring

## What is automated
- GitHub Actions runs a daily source-health check (06:23 UTC, approximate).
- Existing `data/properties.json` is validated for structural errors.
- The monitor tests whether source URLs respond and flags records older than 7 days.
- Changed reports are proposed in a pull request, **never pushed to the published branch**.

## What is NOT automated yet
- Price extraction, booking availability, incentives and academic-year classification.
- HTTP 200 does not establish that a price is correct.
- No automated modification of public listings. This is intentional until provider-specific parsers are independently tested.

## Review and publication
1. Inspect `reports/listings-monitor.json` in the generated PR.
2. Check flagged operator pages manually. A 403/429 is not evidence of sold-out accommodation.
3. Confirm academic year, room grade, weekly rent, contract length and promotion terms.
4. Update `data/properties.json` in a separate reviewed PR; retain source and checked date.
5. Merge only after validating changes. GitHub Pages then deploys from the default branch.

## One-time repository setting
In Settings > Actions > General, allow GitHub Actions to create and approve pull requests if your repository policy permits it. The workflow requires `contents: write` and `pull-requests: write` for the review PR. If restricted, the monitor still runs but PR creation may fail.

## Next milestone
Build source-specific parsers with fixture tests, explicit academic-year mapping, validation thresholds and a human approval gate before allowing verified routine fields to be updated automatically.
