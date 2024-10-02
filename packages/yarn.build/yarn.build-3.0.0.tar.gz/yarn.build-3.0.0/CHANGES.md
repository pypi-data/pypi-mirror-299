# Changelog

## 3.0.0 (2024-10-01)

### Breaking changes

- configuration options are mandatory,
  autodiscovery of `packages.json` has been removed
- it is no longer tied to `yarn`, nor to `yarn build` to generate the assets,
  you can use whichever tooling you want, please refer to the `README`

## 2.0.0 (2024-03-01)

- Nothing changed since the alpha release.

## 2.0.0a1 (2024-02-22)

- Add linting with `pre-commit` / `tox` / GitHub Actions

- Rename the main module to something else than `build` as it clashes with the distribution https://pypi.org/project/build/

- Update the syntax to python 3.11 and use `pathlib`

## 1.0.0 (2019-02-11)

- No changes since last release

## 1.0b3 (2018-11-09)

- Fix logic, to not try to build a project if no package.json could be found

- Be more quiet if no `yarn.build` section is found on `setup.cfg`

## 1.0b2 (2018-11-09)

- Change option to `folder` as package.json is expected to be there, i.e.

```ini
[yarn.build]
folder = path/to/folder/
```

## 1.0b1.post0 (2018-11-09)

- Fix (hopefully), pypi rendering

## 1.0b1 (2018-11-09)

- Allow to configure where package.json is located via a setup.cfg section

```ini
[yarn.build]
file = path-to/package.json
```

## 1.0a6 (2017-01-06)

- Create universal wheels again

## 1.0a5 (2017-01-06)

- Pass the parent folder where package.json is

## 1.0a4 (2017-01-06)

- Typos are fun...

## 1.0a3 (2017-01-06)

- Ditch wheels by now, only source releases

## 1.0a2 (2017-01-06)

- Be more verbose

## 1.0a1 (2017-01-05)

- Initial release
