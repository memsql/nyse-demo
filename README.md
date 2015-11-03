# Simple NYSE Simulator

This simple NYSE demo uses Jupyter notebooks.

## Setup the database

To run the nyse-demo you need to have a running MemSQL cluster (or single
node), and the included schema.  To quickly create the "stocks" database this
demo needs run the following command against your MemSQL master aggregator:

```
mysql ...connection arguments... < schema.sql
```

## Usage from Docker, with Jupyter notebooks

Optionally, rather than installing the dependencies on your base system (and
running the code on your system), you can build and run the included Dockerfile
which includes all dependencies:

```
docker build -t nyse-demo .
```

### Generate data:

```
docker run nyse-demo gen.py --host <MEMSQL HOST> --user <MEMSQL USER>
```

### Setting up Docker gateways

### Run regression analysis on data
