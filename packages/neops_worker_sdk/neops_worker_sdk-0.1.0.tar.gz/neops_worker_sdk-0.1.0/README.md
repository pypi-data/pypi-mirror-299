# Neops Task Runner for Python

This repository provides the base infrastructure and SDK to create workers for your own function blocks. 


## Run nepos Worker

To run th neops worker, simply execute

```
poetry run neops_worker
```

## Code Style

We enforce typing for all python files. You can check if typing is correct by running the following command

```shell
poetry run mypy ./neops_worker_sdk examples/
```

Formatting is enforced by black

```shell
poetry run black ./neops_worker_sdk examples/
```