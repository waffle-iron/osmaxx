# Deployment container for Docker


## Docker installation

See https://docs.docker.com/installation/ubuntulinux/

1. Be sure your kernel version is 3.10 or newer and wget is installed
2. Install docker:

    ```shell
    wget -qO- https://get.docker.com/ | sh
    ```
3. Create a docker group and add you

    ```shell
    sudo usermod -aG docker {yourUserName}
    ```


## Build & run container

1. Copy current source to docker data:

    ```shell
    # use a clean repo to tar the source
    cd /tmp
    git clone git@github.com:geometalab/osmaxx.git --branch master --single-branch && cd osmaxx
    git submodule init && git submodule update
    tar -cf deployment/source.tar source

    # git archive not working with submodules
    # git archive master --format tar --output deployment/source.tar

    # tar from not-empty repository:
    tar -cf deployment/source.tar --exclude='*.git' --exclude='*.od*' --exclude='*.gitignore' --exclude='*.gitmodules' --exclude='*developmentEnvironment/' --exclude='*data/' --exclude='*.idea' --exclude='*test_db.sqlite' --exclude='*__pycache__/' source

    ```
2. Build image:

    ```shell
    docker build --tag=osmaxx --no-cache=true deployment/
    ```
3. Run container:

    ```shell
    # map host port 8080 to port 80 of container
    docker run -d -p 8080:80 osmaxx
    ```
    **Note:** If you start the container with custom arguments (e.g. *docker run osmaxx /bin/bash*) you will override the CMD command to start the server.
     So you need to start the server by your self.


## Management

Run container interactive:
```shell
(sudo) docker run -i -t osmaxx /bin/bash
```

Show running containers:
```shell
docker ps
```

Stop running container:
```shell
docker stop {containerID}
```

Save docker image to file:
```shell
docker save osmaxx > /tmp/osmaxx-alpha1.docker-img.tar
```

Load docker image from file:
```shell
docker load < /tmp/osmaxx-alpha1.docker-img.tar
```