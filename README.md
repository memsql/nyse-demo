# Simple NYSE Simulator

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

Run the Docker image:
```
docker run -d --name nyse-demo -p 8888:8888 nyse-demo
```

On Linux, you will now be able to connect to localhost:8888 from the browser, and run nyse_demo.ipynb.

Otherwise, find the Docker VM IP address, and from the browser open VM_IP:8888.

From there, open the IPython notebook nyse_demo.ipynb.
