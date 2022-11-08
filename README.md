# Koncepts

![example workflow](https://github.com/smrowley/koncepts/actions/workflows/image-build-publish.yaml/badge.svg)

Image is hosted on [quay.io](https://quay.io/srowley/koncepts)

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

There are also a few query parameters that you can specify to will cause various status codes and messages to be given in the reponse:

* `startup_delay` parameter looks for a positive integer value, and represents the number of seconds after the python app has started before it will return `200` responses. Until that time, it will return `503` response codes.
  * eg. `$HOSTNAME/test?startup_delay=10` will return `503` responses for 10 seconds.
  * Default value is `-1`, which will immediately return a `200` on startup.
* `failure_delay` parameter works similar to `startup_delay`, but will return `500` status codes after the integer value in seconds beyond the python app starting.
  * eg. `$HOSTNAME/test?failure_delay=10` will return `500` responses after the first 10 seconds of the app being started.
  * Default value is `-1`, which will never return a `500` failure.
  * Note: this parameter is absolute, and has no effect from the value set by `startup_delay`.
    * Example: `$HOSTNAME/test?startup_delay=10&failure_delay=10` will never return a `200` response. Only `503` prior to 10 seconds, and `500` after 10 seconds has lapsed.
* `readiness_period` and `readiness_duration` parameters can be used to set a consistent interval of readiness/unreadiness.
  * `readiness_period` expects a positive integer value, which sets the interval period.
  * `readiness_duration` also expects a positive integer, and is the amount of time at the beginning of each period the response will return a `200`.
  * eg. `$HOSTNAME/test?readiness_period=10&readiness_duration=5` will return a `200` for the first five seconds of every ten second interval, and a `503` for the other five seconds.
  * Note: the readiness parameters only come into effect after `startup_delay` and `failure_delay` success conditions are met. However, the start time of the intervals is absolute to the startup time of the app.

### Curl loop for testing

The following is an example script that will curl the app at one second intervals and return the pod name. This can be used to demonstrate the effects of pod scaling with `ReplicaSets` or `Deployment` rollouts.

```sh
while [ true ]
do
  curl '$HOSTNAME/test?startup_delay=8&failure_delay=45&readiness_period=10&readiness_duration=5'
  sleep 1
done
```
