---
marp: true
theme: gaia
markdown.marp.enableHtml: true
paginate: true
footer: ISEN
---

<style>

section {
  background-color: #fefefe;
  color: #333;
}

img[alt~="center"] {
  display: block;
  margin: 0 auto;
}
blockquote {
  background: #ffedcc;
  border-left: 10px solid #d1bf9d;
  margin: 1.5em 10px;
  padding: 0.5em 10px;
}
blockquote:before{
  content: unset;
}
blockquote:after{
  content: unset;
}
</style>

<!-- _class: lead -->


# Containers

---

# What  is a docker container ?

A Docker container is a lightweight, standalone, executable package of software that includes everything needed to run an application: code, runtime, system tools, system libraries and settings.

---

### Think of it like a shipping container

* Standardized: Just like shipping containers are standardized in size and shape, Docker containers are standardized to run consistently across different environments.
* Isolated: Each shipping container is isolated from others, preventing any interference. Similarly, Docker containers are isolated from each other and the host system, ensuring that applications don't conflict.
* Portable: Shipping containers can be easily transported between ships, trains, and trucks. Docker containers can be easily moved between different machines running Docker, whether it's your laptop, a server in your data center, or a cloud provider.

---

## Benefits of using Docker containers

* Consistency: Applications run the same way across different environments, from development to production.
* Portability: Easily move applications between different machines and cloud providers.
* Efficiency: Containers are lightweight and use fewer resources than VMs.
* Speed: Containers start up quickly, making it easier to deploy and scale applications.
* Isolation: Applications are isolated from each other, preventing conflicts and improving security.

---

# How do we write a dockerfile ?

A Dockerfile is a text file that contains all the instructions Docker needs to build an image. It's essentially a recipe for creating a container.

**Basic Structure**:

A Dockerfile starts with a `FROM` instruction, specifying the base image to build upon. This could be an operating system like Ubuntu or a pre-configured image with tools you need, like Python or Node.js. Subsequent instructions add layers to this base image, installing software, copying files, and setting up the environment.

---

`FROM <image>`: Specifies the base image.
```docker
FROM ubuntu:latest
```

`WORKDIR <path>`: Sets the working directory inside the container.
```docker
WORKDIR /app
```

`COPY <source> <destination>`: Copies files from your host machine to the container.
```docker
COPY . /app
```
---

`RUN <command>`: Executes commands inside the container, often to install software. .
```docker
RUN apt-get update && apt-get install -y python3
```

`CMD ["executable", "parameters"]`: Specifies the command to run when the container starts. There can be only one CMD instruction.
```docker
CMD ["python", "app.py"]
```

---

`EXPOSE <port>`: Exposes a port to allow communication with the container.
```docker
EXPOSE 8080
```

`ENV <variable> <value>`: Sets environment variables inside the container.
```docker
ENV FLASK_APP app.py
```
---

```docker
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run"]
```

---

# Building and Running

Once you have a Dockerfile, you can build an image using the docker build command:

* `docker build -f Dockerfile -t my-app-image .`
* `docker build -f Dockerfile -t my-app-image frontend`

And then run a container from that image:

* `docker run -p 5000:5000 my-app-image`

---

### Differences between a dockerfile, a container and an image

1. Dockerfile:

  * What it is: A text file containing instructions on how to build a Docker image. Think of it like a recipe or a blueprint.
  * Purpose: To define the steps needed to create a consistent and reproducible environment for your application.
  * Analogy: A recipe in a cookbook.

---

2. Docker Image:

  * What it is: A read-only template or snapshot that includes everything needed to run an application: code, runtime, system tools, libraries, and settings. It's built from a Dockerfile.
  * Purpose: To serve as a base for creating containers. You can have multiple containers running from the same image.
  * Analogy: The cake you baked using the recipe.

---

3. Docker Container:

  * What it is: A running instance of a Docker image. It's a lightweight and portable environment where your application actually executes.
  * Purpose: To provide an isolated and consistent environment for your application to run, regardless of the underlying infrastructure.
  * Analogy: A slice of the cake you baked.

---

|  Feature   |               Dockerfile                |                Docker Image                 |                 Docker Container                  |
| :--------: | :-------------------------------------: | :-----------------------------------------: | :-----------------------------------------------: |
|    Type    |                Text file                |             Read-only template              |                 Running instance                  |
|  Purpose   |      Defines how to build an image      |  Serves as a base for creating containers   | Provides an isolated environment for running apps |
| Mutability | Immutable (you don't change the recipe) | Immutable (you can't change the baked cake) |   Mutable (you can add frosting to your slice)    |

---

## Best Practices

* Use Official Images: Start with well-maintained base images from Docker Hub.
* Minimize Layers: Combine multiple commands into a single RUN instruction to reduce image size.
* Use `.dockerignore`: Create a `.dockerignore` file to exclude unnecessary files from being copied into the image.
* Multi-Stage Builds: Use multiple `FROM` instructions to create intermediate images for compilation or dependency installation, then copy only the necessary artifacts to the final image.
* Security: Run containers as a non-root user whenever possible.

---

## Multi-stage build

A multi-stage build in Docker is a technique that allows you to use multiple FROM instructions in your Dockerfile to create intermediate images during the build process.  This is useful for optimizing your final image size and improving build efficiency.

---

## The Problem with Single-Stage Builds

In a typical single-stage build, all the commands in your Dockerfile contribute to the final image size.  Often, you need tools and dependencies for building your application that aren't needed at runtime. For example:

* Compilers: You might need a compiler like GCC to build your application, but the compiler itself isn't needed in the final image.
* Build Tools: Tools like Maven or npm are used for building Java or Node.js applications, but they aren't required to run the application.
* Intermediate Files: Temporary files created during the build.

---

## How Multi-Stage Builds Solve the Problem

Multi-stage builds let you use separate "stages" for different parts of your build process.  You can use one stage for building your application, including all the necessary build tools and dependencies.  Then, you can create a second, smaller stage that copies only the essential artifacts from the build stage into the final image.

---

```docker
# Stage 1: Build the application
FROM node:16 AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Create the final image
FROM nginx:alpine

COPY --from=build-stage /app/build /usr/share/nginx/html
```

---

## Benefits of Multi-Stage Builds:

* Smaller Image Sizes: The final image only contains the necessary runtime components, significantly reducing its size. Faster downloads, deployments, and reduced storage costs.
* Improved Build Caching: Docker can cache the intermediate stages, speeding up subsequent builds if the build steps haven't changed.
* Simplified Dockerfiles: You can keep the build logic separate from the final image configuration, making your Dockerfiles easier to understand and maintain.
* Security: By not including build tools and dependencies in the final image, you reduce the potential attack surface.

---

# Docker capabilities

Docker capabilities are a security feature that allows you to fine-tune the privileges granted to a container. They're based on the Linux kernel's capability system, which breaks down the traditional all-or-nothing root privilege model into smaller, more granular permissions.

**How do Docker capabilities work?**
Linux capabilities divide the privileges traditionally associated with the root user into distinct units. For example, instead of giving a container full root access, you can grant it only the `CAP_NET_BIND_SERVICE` capability, which allows it to bind to privileged ports (those below 1024).

---

# Common Docker capabilities

* `CAP_NET_ADMIN`: Allows network administration tasks, like configuring interfaces or firewall rules.
* `CAP_SYS_ADMIN`: Grants a wide range of system administration capabilities, including mounting file systems and managing devices. (Use with caution!)
* `CAP_FOWNER`: Allows the container to act as the file owner, even if it doesn't actually own the file.
* `CAP_CHOWN`: Allows the container to change the ownership of files.

---

# Managing Docker capabilities

* Adding capabilities: Use the `--cap-add` flag when running a container to grant specific capabilities.
```sh
docker run --cap-add=NET_ADMIN <image>
```

* Removing capabilities: Use the `--cap-drop` flag to revoke capabilities.
```sh
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE <image>
```
`—-cap-add=all`

---

# Linux Container vs Windows Container

**The Core Difference: The Kernel**

The most fundamental difference lies in the kernel.

* Linux containers share the kernel of the Linux host operating system. This is the core of how containers achieve efficiency.
* Windows containers also share a kernel, but it's a Windows kernel. This means they can only run on Windows hosts.

---

This kernel difference has significant implications:

* Operating System Compatibility:
    * Linux containers can only run on Linux hosts.
    * Windows containers can only run on Windows hosts.
* Application Compatibility:
    * Linux containers are primarily used for applications designed for Linux environments.
    * Windows containers are designed for applications that rely on the Windows operating system, libraries, and APIs.

---

In practice

* **Linux Containers on Linux**: This is the "classic" container scenario. Containers share the host's Linux kernel directly, making them very lightweight and efficient.
* **Linux Containers on Windows**: This is possible, but it requires a Linux virtual machine (VM) running on the Windows host. Docker Desktop for Windows, for example, uses a lightweight Linux VM to run Linux containers.
* **Windows Containers on Windows**: Windows containers run directly on the Windows host, sharing its kernel.

---

# Containers vs Virtual Machines


|    Feature     | Virtual Machines (VMs) |      Containers       |
| :------------: | :--------------------: | :-------------------: |
|       OS       |  Separate OS for each  | Shares host OS kernel |
|   Isolation    |         Strong         |     Process-level     |
| Resource Usage |          High          |          Low          |
|  Startup Time  |          Slow          |         Fast          |
|      Size      |         Large          |         Small         |

---

# Docker compose files

A Docker Compose file is a YAML file that defines a multi-container Docker application.  It's a way to manage and orchestrate multiple Docker containers as a single unit.  Think of it as a blueprint for your entire application stack, specifying all the services (containers) that make up your application, their dependencies, and how they interact.

---

# What it does

* **Defines Services**: Each service in the Compose file represents a container. You specify the image to use, ports to expose, volumes to mount, environment variables, and other configuration options for each container.
* **Manages Dependencies**: You can define dependencies between services. For example, you can specify that a web application service depends on a database service, ensuring that the database starts before the web application.

---

# What it does

* **Simplifies Multi-Container Management**: Instead of running multiple docker run commands to start each container individually, you can use a single docker-compose up command to start all the services defined in the Compose file.
* **Configuration as Code**: The Compose file serves as a configuration file for your application stack, making it easy to share, version control, and reproduce your application environment.

---

# Why it's useful

* **Local Development**: Docker Compose is excellent for setting up and managing complex development environments. You can easily define all the services your application needs (database, web server, cache, etc.) and run them together locally.
* **Testing**: You can use Docker Compose to create consistent testing environments that mirror your production setup.
* **Simple Deployments**: While not typically used for large-scale production deployments (Kubernetes is better for that), Docker Compose can be useful for simpler deployments or for deploying to single server instances.