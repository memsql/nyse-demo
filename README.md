# Simple NYSE Simulator

## Setup the database

To run the nyse-demo you need to have a running MemSQL cluster (or single
node), and the included schema. The easiest way to get it is to pull the memsql-docker-quickstart image:

```
docker pull memsql/quickstart
docker run -d -p 3306:3306 -p 9000:9000 --name=memsql memsql/quickstart
```

Then create the database schema:

```
cat schema.sql | docker run -i --link=memsql:memsql memsql/quickstart memsql-shell
```

## Getting started with the nyse-demo container:
```
docker pull memsql/nyse-demo
```

### Generate data:

```
docker run --link memsql nyse-demo gen.py
```
This will generate around 500000 new records each time it's run.

### Run the main container:

```
docker run -d --name nyse-demo -p 8888:8888 --link memsql nyse-demo
```

On Linux, you'll now be able to open localhost:8888 in your browser. On Windows and OS X,
find the Docker VM IP address, and open VM_IP:8888. Then open the nyse_demo.ipynb notebook.
