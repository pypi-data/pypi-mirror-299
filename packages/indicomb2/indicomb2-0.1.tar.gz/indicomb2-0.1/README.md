Faster indicomb with mkdocs markdown support.
An alternative to the original [indicomb](https://gitlab.cern.ch/indicomb/indicomb).

This is fast enough to run in the CI as your docs get built (say goodby to your cron jobs!), and comes with mkdocs markdown support.


## Quick Start

```bash
pip install indicomb2
```

Set up a config, see the [example](https://gitlab.cern.ch/indicomb/indicomb2/-/blob/main/example.yaml)

Run:

```bash
indicomb2 -c my_config.yaml
```


## More details

1. Set up a CERN docs site: https://how-to.docs.cern.ch/
2. Add an environment variable `INDICO_API_TOKEN` with the token from https://indico.cern.ch/user/tokens/
3. Setup a config, see the [example](https://gitlab.cern.ch/indicomb/indicomb2/-/blob/main/example.yaml)
4. Run `indicomb2 -c my_config.yaml`
