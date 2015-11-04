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

## Pull and run the nyse-demo container:
```
docker pull memsql/nyse-demo
```

### Generate data:

```
docker run --link memsql nyse-demo gen.py
```

### Run the main container:

```
docker run -d --name nyse-demo -p 8888:8888 --link memsql nyse-demo
```

### Setting up Docker gateways

Run the Docker image:
```
docker run -d --name nyse-demo -p 8888:8888 nyse-demo
```

On Linux, you will now be able to connect to localhost:8888 from the browser, and run nyse_demo.ipynb.

Otherwise, find the Docker VM IP address, and from the browser open VM_IP:8888.

From there, open the IPython notebook nyse_demo.ipynb.
