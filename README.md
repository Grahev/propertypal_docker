#Commands
***

## To build docker image:
```terminal
docker build -t test-enviroment .
```

```terminal
docker build -t [image-name] .
```

## To run container:
```terminal
docker run --name test-enviroment test-envviroment
```

```terminal
docker run --name [image-name] [container-name]
```
## To run vith assigned volume:
```terminal
docker run --name test-enviroment test-envviroment -v $(pwd):/code
```