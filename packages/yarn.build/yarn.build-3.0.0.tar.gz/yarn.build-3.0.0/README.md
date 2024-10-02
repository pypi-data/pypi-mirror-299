# Introduction

This package builds JavaScript projects any JS tooling you might happen to use.
It contains a [`zest.releaser`](http://pypi.org/project/zest.releaser)
entry point and a stand-alone command line tool.

## Goal

You want to release a package that has a `packages.json` on it
and to build the final assets you only have two commands:

- install (dependencies)
- build (the assets)

Usually one does not want to keep the generated files on VCS,
but you want them when releasing with `zest.releaser`.

## Configuration

For that to work you need to add a `yarn.build` section on `setup.cfg`
with the following configuration options:

```ini
[yarn.build]
folder = src/my/package/frontend
install = pnpm install --frozen-lockfile
build = pnpm build
```

- `folder`: is a path to where the `package.json` is located
- `install`: is the command to install the dependencies that your frontend code needs
- `build`: is the command that generates your assets

## Credits

This package is a direct inspiration from
[`zest.pocompile`](https://pypi.org/project/zest.pocompile) from Maurits van Rees.

Thanks!

## To Do

Add tests
