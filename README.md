# Koncepts

[![Build Status](https://travis-ci.org/smrowley/koncepts.svg?branch=master)](https://travis-ci.org/smrowley/koncepts)
[![](https://images.microbadger.com/badges/commit/srowley/koncepts.svg)](https://microbadger.com/images/srowley/koncepts "Get your own commit badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/srowley/koncepts.svg)](https://microbadger.com/images/srowley/koncepts "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/srowley/koncepts.svg)](https://microbadger.com/images/srowley/koncepts "Get your own version badge on microbadger.com")

Image is hosted on [Docker Hub](https://hub.docker.com/r/srowley/koncepts)

Koncepts is an application for exercising Kubernetes concepts to newer Kubernetes users, as well as testing various configurations.

A Python Flask application that displays `/etc/hostname` and other info about the host as an html page. When the application is deployed in k8s, this will be the pod name and other pod info.

The app may be helpful for demos of pod deployments, scaling, deletions, etc.

The service is a Flask Python app running on gunicorn. It is using a Jinja template for the index.html. Please forgive the messy html with inline styles and such.

## Deploying the app

You can quickly deploy the app in k8s with the following after cloning the repo:

```
kubectl apply -k kube/base
```

### Example: Deploy with config files mounted as volume

```
kubectl apply -k kube/overlays/with-config-files
```

### Example: Deploy with LoadBalancer service ingress

```
kubectl apply -k kube/overlays/expose-lb
```

### Example: Deploy with Ingress configured for Traefik

```
kubectl apply -k kube/overlays/expose-traefik
```

## Index page

The index URL returns an html page that provides information about the container.

## Command line inspection

The app will also handle requests to any path, log the request, and provide a response.

### Query Parameters

There are also two query parameters that you can specify:

* `d` parameter looks for a positive integer value, and represents the number of seconds after the python app has started before it will return `200` responses. Until that time, it will return `503` response codes.
  * eg. `http://<route url>/test?d=10` will return `503` responses for 10 seconds
  * Default value is `0`
* `f` parameter works similar to `d`, but will return `500` status codes after the integer value in seconds beyond the python app starting.
  * eg. `http://<route url>/test?f=10` will return `500` responses after the first 10 seconds of the app being started.
  * Default value is `0`
  * Note: this parameter is absolute, and has no effect from the value set by `d`.
    * Example: `http://<route url>/test?d=10&f=10` will never return a `200` response. Only `503` prior to 10 seconds, and `500` after 10 seconds has lapsed.

### Curl loop for testing

The following is an example script that will curl the app at one second intervals and return the pod name. This can be used to demonstrate the effects of pod scaling with `ReplicaSets` or `Deployment` rollouts.

```sh
while [ true ]
do
  curl http://<route url>/test?d=10
  sleep 1
done
```
