# Plover Steno Engine Hooks Logger

[![Build Status][Build Status image]][Build Status url] [![PyPI - Version][PyPI version image]][PyPI url] [![PyPI - Downloads][PyPI downloads image]][PyPI url] [![linting: pylint][linting image]][linting url]

[Plover][] uses [Engine Hooks][] to allow [plugins][] to listen to its
[steno engine][] events. This hybrid [extension][]/[GUI Tool][] plugin simply
connects into all the known Engine Hooks, and logs out the given parameters to
the [Plover log][], which can be handy during Plover plugin development.

## Install

1. In the Plover application, open the Plugins Manager (either click the Plugins
   Manager icon, or from the `Tools` menu, select `Plugins Manager`).
2. From the list of plugins, find `plover-steno-engine-hooks`
3. Click "Install/Update"
4. When it finishes installing, restart Plover

### Extension Logging

1. After re-opening Plover, open the Configuration screen (either click the
   Configuration icon, or from the main Plover application menu, select
   `Preferences...`)
2. Open the Plugins tab
3. Check the box next to `plover_steno_engine_hooks` to activate the extension

### GUI Tool Logging

1. After re-opening Plover, click the Steno Engine Hooks Logger button on the
   Plover application to enable GUI-related logging.

## Usage

Since both the Extension and GUI Tool logging cover the same ground, you will
likely only want to use one at a single time (the extension, or the GUI Tool,
depending on what kind of plugin you are developing), otherwise the logs will
get very noisy.

To view the logs, open up `plover.log`, located under your [Plover configuration
directory][]:

- Windows: `C:\Users\<your username>\AppData\Local\plover`
- macOS: `~/Library/Application Support/plover`
- Linux: `~/.config/plover`

There, you should see entries there prefixed with `[STENO ENGINE HOOK
(EXTENSION)]` or `[STENO ENGINE HOOK (GUI)]`.

If you ever find the logs getting too noisy, then comment out any of the hooks
you don't need to listen to in the `_HOOKS` list under the `Logger` class.

## Development

Clone from GitHub with [git][] and install test-related dependencies with
[pip][]:

```console
git clone git@github.com:paulfioravanti/plover-steno-engine-hooks-logger.git
cd plover-steno-engine-hooks-logger
python -m pip install --editable ".[test]"
```

If you are a [Tmuxinator][] user, you may find my
[plover_steno_engine_hooks_logger project file][] of reference.

### Python Version

Plover's Python environment currently uses version 3.9 (see Plover's
[`workflow_context.yml`][] to confirm the current version).

So, in order to avoid unexpected issues, use your runtime version manager to
make sure your local development environment also uses Python 3.9.x.

### Type Checking and Linting

Since the only parts of the plugin able to be tested are ones that do not rely
directly on Plover, automated testing has not been possible. But, at least there
are some code quality checks performed:

- [Pylint][] is used for code quality
- [Mypy][] is used for static type checking

Run type checking and linting with the following commands:

```console
pylint plover_steno_engine_hooks_logger
mypy plover_steno_engine_hooks_logger
```

If you are a [`just`][] user, you may find the [`justfile`][] useful during
development in running multiple test commands. You can run the following command
from the project root directory:

```console
just
```

### Deploying Changes

After making any code changes, install the plugin into Plover with the following
command:

```console
plover --script plover_plugins install --editable .
```

When necessary, the plugin can be uninstalled via the command line with the
following command:

```console
plover --script plover_plugins uninstall plover-steno-engine-hooks-logger
```

[Build Status image]: https://github.com/paulfioravanti/plover-steno-engine-hooks-logger/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-steno-engine-hooks-logger/actions/workflows/ci.yml
[Engine Hooks]: https://plover.readthedocs.io/en/latest/api/engine.html#engine-hooks
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[git]: https://git-scm.com/
[GUI Tool]: https://plover.readthedocs.io/en/latest/plugin-dev/gui_tools.html
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[`just`]: https://github.com/casey/just
[`justfile`]: ./justfile
[linting image]: https://img.shields.io/badge/linting-pylint-yellowgreen
[linting url]: https://github.com/pylint-dev/pylint
[Mypy]: https://github.com/python/mypy
[pip]: https://pip.pypa.io/en/stable/
[Plover]: https://www.openstenoproject.org/
[Plover log]: https://plover.readthedocs.io/en/latest/api/log.html
[Plover Plugins Registry]: https://github.com/openstenoproject/plover_plugins_registry
[Plover configuration directory]: https://plover.readthedocs.io/en/latest/api/oslayer_config.html#plover.oslayer.config.CONFIG_DIR
[plover_steno_engine_hooks_logger project file]: https://github.com/paulfioravanti/dotfiles/blob/master/tmuxinator/plover_steno_engine_hooks_logger.yml
[plugins]: https://plover.readthedocs.io/en/latest/plugins.html
[Pylint]: https://github.com/pylint-dev/pylint
[PyPI]: https://pypi.org/
[PyPI downloads image]: https://img.shields.io/pypi/dm/plover-steno-engine-hooks-logger
[PyPI version image]: https://img.shields.io/pypi/v/plover-steno-engine-hooks-logger
[PyPI url]: https://pypi.org/project/plover-steno-engine-hooks-logger/
[steno engine]: https://plover.readthedocs.io/en/latest/api/engine.html
[Tmuxinator]: https://github.com/tmuxinator/tmuxinator
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
