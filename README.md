# Python Reverse Debugger

[![Build Status](https://travis-ci.org/game-of-things/game-room-service.svg?branch=master)](https://travis-ci.org/game-of-things/game-room-service)
[![](https://images.microbadger.com/badges/commit/srowley/python-reverse-debugger.svg)](https://microbadger.com/images/srowley/python-reverse-debugger "Get your own commit badge on microbadger.com")
[![](https://images.microbadger.com/badges/image/srowley/python-reverse-debugger.svg)](https://microbadger.com/images/srowley/python-reverse-debugger "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/srowley/python-reverse-debugger.svg)](https://microbadger.com/images/srowley/python-reverse-debugger "Get your own version badge on microbadger.com")

Image is hosted on [Docker Hub](https://hub.docker.com/r/srowley/python-reverse-debugger)

A Python Flask application that displays `/etc/hostname` and other info about the host as an html page. When the application is deployed in k8s, this will be the pod name and other pod info.

The app may be helpful for demos of pod deployments, scaling, deletions, etc.

The service is a Flask Python app running on gunicorn. It is using a Jinja template for the index.html. Please forgive the messy html with inline styles and such.

## Deploying the app

You can quickly deploy the app in k8s with the following:

```
kubectl apply -f kube/deploy.yaml
```

## Command line inspection

The service also provides the `/plain` endpoint, which can be useful for curl commands.

The following is an example script that will curl the app at one second intervals and return the pod name. This can be used to demonstrate the effects of pod scaling with `ReplicaSets` or `Deployment` rollouts.

```sh
while [ true ]
do
  curl http://<route url>/plain
  sleep 1
done
```