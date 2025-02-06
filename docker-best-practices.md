# Container best practices and hard rules to follow

- [Container best practices and hard rules to follow](#container-best-practices-and-hard-rules-to-follow)
  - [Introduction](#introduction)
  - [Best practices](#best-practices)
    - [Each container should have only one responsibility.​](#each-container-should-have-only-one-responsibility)
    - [Containers should be immutable, lightweight, and fast.​](#containers-should-be-immutable-lightweight-and-fast)
      - [Recommended softwares, practices](#recommended-softwares-practices)
      - [Note on the stateless part](#note-on-the-stateless-part)
    - [Don’t store data in your containers. Use a shared data store instead.​](#dont-store-data-in-your-containers-use-a-shared-data-store-instead)
    - [Containers should be easy to destroy and rebuild.​](#containers-should-be-easy-to-destroy-and-rebuild)
      - [Note](#note)
    - [Avoid installing unnecessary packages. This keeps the image clean and safe.​](#avoid-installing-unnecessary-packages-this-keeps-the-image-clean-and-safe)
    - [Avoid cache hits when building.​](#avoid-cache-hits-when-building)
    - [Orchestrator: configure resource quotas (memory / CPU) and resource limits​.](#orchestrator-configure-resource-quotas-memory--cpu-and-resource-limits)
  - [Enforced rules](#enforced-rules)
    - [Never use `latest` tag](#never-use-latest-tag)
    - [Add linter, static analysis, and tests](#add-linter-static-analysis-and-tests)
      - [Linting](#linting)
        - [Recommended linter](#recommended-linter)
      - [Static analysis](#static-analysis)
        - [Recommended static analysis software](#recommended-static-analysis-software)
      - [Structure tests](#structure-tests)
        - [Recommended structure tests software](#recommended-structure-tests-software)
    - [Run containers as a non-root user​.](#run-containers-as-a-non-root-user)
    - [Regularly update Docker and host​.](#regularly-update-docker-and-host)
    - [Produce a Software Bill Of Materials (SBOM) and a CVE report](#produce-a-software-bill-of-materials-sbom-and-a-cve-report)
      - [Recommended softwares](#recommended-softwares)
    - [Reduce the capabilities of your container](#reduce-the-capabilities-of-your-container)
  - [Nice to have](#nice-to-have)
  - [To go further](#to-go-further)

## Introduction

The following document outlines the various guidelines you will need to follow when working with containers at Roquette. These guidelines have been written in collaboration with :

This document is divided into three sections:

1. Best practices, i.e. the practices you should follow when working with containers, whether you work at Roquette or not. Every software engineer in the world follow these practices and so should you. Note that this is not an exhaustive list, we're just presenting the most important ones here.
2. The strict rules, i.e. those that we apply and that everyone must follow. There may be particular cases where you should deviate from one of these rules, but you will need to document this.
3. The nice-to-have rules, we don't enforce them and it's up to you and your department's capabilities to follow them or not.

When applicable, we will try to give you a list of recommended softwares, practices.

## Best practices

### Each container should have only one responsibility.​

We try as far as possible to follow a microservices architecture when we deploy our applications.

Let's recall here what a microservice is. The microservices architecture is described [as follows](https://fr.wikipedia.org/wiki/Microservices):

* Services are small and designed to perform a single function.
* The organisation of the project must take account of automation, deployment and testing.
* Each service is elastic, resilient, composable, minimal and complete.

For example, a container hosting a REST service should also not host the database with which it can communicate or anything else. Moreover, you shouldn't need a connection to the database to test your REST service.

### Containers should be immutable, lightweight, and fast.​

A container should be as stateless as possible. Your container output shouldn't depend on anything except its input, ie it contains no state. Each input is self-descriptive, meaning that each request contains enough context to be processed. Especially when you're developping a REST API.

Concerning the "lightweight and fast" practices, it will depend of the programmation language you use. If you use compiled programming language like Go or Rust, your container can weight only a few mb. For language like Python you will be closer of the hundreds of mb.

This does not means you shouldn't optimize the size of your containers. Many softwares allow to do that.

#### Recommended softwares, practices

Note that you don't have to use all of them at once.

* Try as much as possible to perform [multi-stage builds](https://docs.docker.com/build/building/multi-stage/) when writing your Dockerfile,
* Use [distroless](https://github.com/GoogleContainerTools/distroless) images if you can,
* Use [slimtoolkit](https://slimtoolkit.org/) if you can to make your images smaller,
* If you're building Go applications, then the recommended way to build container is to use [ko](https://ko.build/).

#### Note on the stateless part

There are cases where you will have to hold a state on the container, for example with OAuth2 (so it is not officially/technically RESTful).

### Don’t store data in your containers. Use a shared data store instead.​

Apart from database containers, container are not made to store data. You should rely on whether:

* a mounted, named volume,
* a database, storage account hosted on Azure,
* a database container,

to store your data.

### Containers should be easy to destroy and rebuild.​

Easy to build and easy to rebuild is at the core philosophy of containers.

What we mean here is that there should be as least as possible human interaction, you should automate build, push, and destroy as much as possible through CICD pipelines.

Concerning CICD pipelines, we enforce the use of Azure DevOps pipelines as our entreprise solution.

#### Note

Although this won't be enforced, a best practice in software engineering is that your CICD pipelines should be able to run whether you are running them locally on your laptop, or through Azure DevOps. That way your are able to test them and the artifacts they should produce before pushing them to Azure DevOps.

The recommended way to do that is to use softwares like [dagger.io](https://dagger.io/) that rely on isolated containers to run each step of the pipeline.


### Avoid installing unnecessary packages. This keeps the image clean and safe.​

That should be obvious.

### Avoid cache hits when building.​

When building Docker images, caching lets you speed up rebuilding images. But this has a downside: it can keep you from installing security updates from your base Linux distribution. If you cache the image layer that includes the security update... you’re not getting new security updates.

See [here](https://pythonspeed.com/articles/disabling-docker-caching/) as to why it is a best practice.

Note that if you are using CICD pipelines this problem might never happen since there are cleaning, maintenance protocols that wipe pipelines cache, memory after use.


### Orchestrator: configure resource quotas (memory / CPU) and resource limits​.

When you deploy containers on Kubernetes or Azure Container Apps Environment (Microsoft managed Kubernetes solution), be sure to configure resource quotas and resource limits, like the maximum number of pods in a replicaset.

Although you can configure resource quotas on your container during the `docker run ...` command, it is a best practice to delegate this task to the orchestrator.

## Enforced rules

The following rules are the one we will enforce when you aim to deploy container to production. We will try to follow the zero trust principles as much as possible by reducing all rights of the container to the bare minimum.

There are cases where you might deviate from these rules, this should be fine as long as you document why you had to deviate, just remember this should be the exception.

### Never use `latest` tag

The syntax of an image is the following one: `repository:tag`. For example:

* `ubuntu:20.04`, the image hosting the ubuntu OS in its 20.04 version, ubuntu is the name of the repository and 20.04 the tag.
* `daa/iac:20231112.1`, the image used by the Data and Advanced Analyics (daa) team containing Infrastructure as Code (iac) softwares. `daa/iac` is the repository name and the tag `20231112.1` refers to the id of the Azure DevOps pipeline building it: it was the first pipeline that ran the 12th of November 2023.

By default, when you use the `docker build ...` command docker tags your image with the `latest` tag. This means that any previous image that has the same name and tag, ie `repository:latest`, will be overridden if you push you new one in the container registry.

Whether you use semantic versioning tags (eg `1.0.1`), date tags (eg `20231112.1`), or any other type of tags is up to you and your team as long as:

* They are explicit,
* You stick to one type.

### Add linter, static analysis, and tests

#### Linting

The dirty little secret regarding containers is that it’s not always as easy as you might expect to to be. Case in point, have you ever crafted a Dockerfile by hand, only to have it fail to run? It can be very frustrating. From YAML indentation, using an inappropriate image, improperly using tags, and wrong volume mapping... there are so many issues that can cause Dockerfiles to fail.

That’s why you need linting.

Linting is the automated checking of your source code for programmatic and stylistic errors. This is done by using a lint tool (otherwise known as linter). A lint tool is a basic static code analyzer. Linting is important to reduce errors and improve the overall quality of your code. Using lint tools can help you accelerate development and reduce costs by finding errors earlier.

##### Recommended linter

We recommend the use of hadolint, which can be use either [online](https://hadolint.github.io/hadolint/) or via a container you can find on [its github page](https://github.com/hadolint/hadolint).

#### Static analysis

Container images are derived from base images, and there is a lot of stuff within the base images that might be vulnerable. Therefore, a need arises to scan the images because a huge chunk is not in control of developers.

That does not mean that we don’t need to scan the developer configuration as well.

We need to scan the Dockerfiles, the Kubernetes manifests, and other IaC configurations, discover any vulnerabilities that might have crept in, and enforce the security best practices.

You should at least have one static analysis software in your CICD pipeline when building your images. Moreover the report of this analysis is an artifact that should be stored for audit or furthe analysis purpose.

##### Recommended static analysis software

We recommend the use of one of the two folowing softwares.

* [Checkov](https://www.checkov.io/), it uses a common command line interface to manage and analyze infrastructure as code (IaC) scan results across platforms such as Terraform, CloudFormation, Kubernetes, Helm, ARM Templates and Serverless framework. It also performs static on [Dockerfiles](https://www.checkov.io/5.Policy%20Index/dockerfile.html). It can easily be used in a CICD pipeline via the use of the provided [docker image](https://www.checkov.io/4.Integrations/Docker.html).
* [Trivy](https://aquasecurity.github.io/trivy/v0.47/) is a comprehensive and versatile security scanner. It can look into [container images](https://aquasecurity.github.io/trivy/v0.47/docs/target/container_image/#files-inside-container-images) for vulnerabilities, misconfigurations, secrets, and licenses.

Although these two softwares are be complementary, it is mandatory to have **at least one of them** in your CICD pipeline building your image.

#### Structure tests

It’s common practice to validate built container images before deploying them to our cluster. To do this, you can integrate a testing phase between the build and deploy phases of the pipeline. A structure test validates the structural integrity of container images.

Structure tests are defined per image. Every time an image is rebuilt, the associated structure tests on that image must be run. If the tests fail, it will not continue on to the deploy stage.

##### Recommended structure tests software

We recommend the use of [Container Structure Tests](https://github.com/GoogleContainerTools/container-structure-test) which proposes an easy way to write structure tests in yaml format. Again, this tool can be integrated in your CICD pipeline, and the generated report can be saved.

### Run containers as a non-root user​.

Most of the time, when a container is runnning the user inside is by default the `root` user, with a large number of rights, permissions. This can be a major security concern and as such a container running in production shouldn't run as a `root` user.

Changing the user, the user id, and the group id can be done directly in the Dockerfile.

### Regularly update Docker and host​.

As any other piece of software, you should regularly update your containers.

This update mechanism should be done automatically via scans in your Azure DevOps repository.

As a best practice, youy should check for updates at least once a month.

### Produce a Software Bill Of Materials (SBOM) and a CVE report

Ideally, each container should provide at least the following two artifacts:

* A Software Bill Of Materials (SBOM), which writes down all the software components used in an image. SBOMs aim to reduce risk and improve transparency and security around the applications produced by the company. This should be generated in a CI.
* A list of vulnerabilities attached to the SBOM should also be generated in a CI.

These two artifacts can then be pushed into the container registry at the same time as the image.

#### Recommended softwares

* Concerning the Software Bill Of Materials (SBOM), it can be done with a tool such as [Syft](https://github.com/anchore/syft)
* Concerning the list of vulnerabilities attached to the SBOM, it can be done with a tool such as [Grype](https://github.com/anchore/grype).

### Reduce the capabilities of your container

To check permissions, traditional UNIX implementations distinguish between two categories of process: privileged processes (whose effective UID is 0, known as superuser or root), and non-privileged processes (whose effective UID is non-zero). Privileged processes bypass kernel permission checks, while non-privileged processes are subject to a full check based on process identification (usually: effective UID, effective GID, and list of groups).

From kernel 2.2 onwards, Linux offers a (still incomplete) capabilities mechanism, which splits the privileges traditionally associated with the superuser into separate units that can be activated or inhibited individually.  Capabilities are individual attributes of each thread.

Out of the 35 available "sensitive" capabilities, the following 19 are equivalent to the rights of the root user (UID=0) (full root).

* `CAP_AUDIT_CONTROL`
* `CAP_CHOWN`
* `CAP_DAC_OVERRIDE`
* `CAP_DAC_READ_SEARCH`
* `CAP_FOWNER`
* `CAP_FSETID`
* `CAP_IPC_OWNER`
* `CAP_MKNOD`
* `CAP_SETFCAP`
* `CAP_SETGID`
* `CAP_SETPCAP`
* `CAP_SETUID`
* `CAP_SYS_ADMIN`
* `CAP_SYS_CHROOT`
* `CAP_SYS_BOOT`
* `CAP_SYS_MODULE`
* `CAP_SYS_PTRACE`
* `CAP_SYS_RAWIO`
* `CAP_SYS_TTY_CONFIG`

By default, and to follow the zero trust principles and the [ANSSI recommendations](https://cyber.gouv.fr/publications/recommandations-de-securite-relatives-au-deploiement-de-conteneurs-docker), each container must be started without any capability using the option `--cap-drop=ALL`.

If your container really need one or more capabilities, you can still add them. A container can be started with the strictly necessary capabilities with the `--cap-drop=ALL` and `--cap-add={"capability A"}` options. But then you should provide a documentation as to why you had to add this capability.

(maybe provide a reproducible example of your container failure without this capability ?)

## Nice to have

If you want to go further, you can use tools such as [cosign](https://github.com/sigstore/cosign), which enables images to be electronically signed to validate that the software they use is exactly what you expect. This validation is carried out using coded digital signatures and transparency log technologies.

Other methods are also available on the Azure container registry:

* [Docker Content Trust](https://learn.microsoft.com/en-us/azure/devops/pipelines/ecosystems/containers/content-trust?view=azure-devops)
* [Docker Content Trust on ACR with Azure Pipelines](https://dev.to/smapiot/docker-content-trust-on-acr-with-azure-pipelines-1p0k)

In order to benefit from these tools, the container registries deployed on Azure must be deployed with premium sku.

## To go further

The CNCF (Cloud Native Computing Foundation), part of the Linux Foundation, has published 2 white papers on the "Secure Software Factory" and the "Supply Chain Security". Although they take a very macro viewpoint, they provide a good starting point.

* https://github.com/cncf/tag-security/blob/main/supply-chain-security/secure-software-factory/Secure_Software_Factory_Whitepaper.pdf
* https://github.com/cncf/tag-security/blob/main/supply-chain-security/supply-chain-security-paper/CNCF_SSCP_v1.pdf

