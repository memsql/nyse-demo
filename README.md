# Simple NYSE Simulator

## Dependencies

Before running the code, make sure we have all of the dependencies
needed for this example by running:

```
sudo apt-get install gfortran libopenblas-dev liblapack-dev libmysqlclient-dev python-numpy python-scipy python-matplotlib ipython
python-imaging-tk ipython-notebook python-pandas python-sympy python-nose libfreetype6-dev;
make deps;
```

## Setup the database

To run the nyse-demo you need to have a running MemSQL cluster (or single
node), and the included schema.  To quickly create the "stocks" database this
demo needs run the following command against your MemSQL master aggregator:

```
mysql ...connection arguments... < schema.sql
```

## Usage from Docker

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

### Run regression analysis on data
