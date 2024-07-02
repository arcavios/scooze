# Deploying a new release

- Create a release PR off `dev`
  - Move `Development` section of changelog into section with new release number
  - Update `pyproject.toml` with new release number
  - Run `poetry update` to update dependencies
  - Verify CI
  - Merge PR (after review/verification)
- Create GitHub release with tag `vX.Y.Z`; copy changelog from PR
- You're done! `pypi` will auto-update from the newly tagged release


# New set release checklist

If any of the below could cause breaking changes, a new patch or minor release
should follow the fix PR.

## Issues expected to be caught by bulkdata validation

- New symbols on cards (e.g. mana symbols, energy)
- New frame effects
- New layouts (e.g. Case, Saga)
- Other [cataloged fields](src/scooze/catalogs.py)


## Potential issues that need manual checks

- New fields in card objects (e.g. moving `foil`/`nonfoil` to `finishes`)
- New card face combinations (e.g. reversible cards with different faces)
- New promo types
- New "relentless" cards or other specific deck limits


## Channels to monitor for changes

- Scryfall Discord's `#api-announcements` and `#announcements`
- Scryfall's [api changelog](https://scryfall.com/blog/category/api)
(seems to be deprecated since 9/2022)
