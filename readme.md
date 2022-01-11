# Welcome to Mesimä

This is the source of Mesimä (pronounced Mesi-mah). It is a RESTful HTTP application for task managment, written in Python.

Mesimä was created with ❤️ using [Django Rest Framework](https://www.django-rest-framework.org/) and [PostgreSQL](https://www.postgresql.org/).

# Development Instructions

## Prerequisites

Running the app requires having tilt, k3d and their dependencies (Docker, kubectl...).

This project was developed using tilt `v0.23.4` and k3d `v5.2.2`.
Newer version *should* be fine.

## Running the Application

Create a k3d cluster:

```s
$ k3d cluster create --config k3d.yaml
```

Install Kubegres (a Kuberntes operator for delpoying PostgreSQL clustres):

```s
$ kubectl apply -f https://raw.githubusercontent.com/reactive-tech/kubegres/v1.15/kubegres.yaml
```

Start the development setup:

```s
$ tilt up
```

Open a web broswer and navigate to `https://localhost:3080/api`. You should see DRF's browseable api client.

To delete the cluster:

```s
$ k3d cluster delete amit-mini-project
```

## Running the Tests

It is recommended to run the tests using sqlite, without k3d. 
This requires having `poetry` installed.

Use the following sequence of commands to run the unit-tests:

```s
$ cd backend
$ poetry install                       # Install Python dependencies
$ poetry shell                         # Spawn a shell inside the virtual environemnt
$ cd manager
$ DB="sqlite" python manage.py test    # Run the test suite while using sqlite
```

## Documentation

The Django app and project were generated using `django create project` and `django create app` commands.

Consequentially, a basic understanding of Django's [getting started tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/) should be enough to understand the role of each source file.

To gain understanding of specific aspects of the app (e.g, routing), it is recommended to read the respective source files.
DRF abstractions are heavily used, which allows most code to be self-documenting.

Usage of less common Django/DRF funcitonality is documented inline in each source file, with comments linking to Django documentation. 
