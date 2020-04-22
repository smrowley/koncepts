# Python Reverse Debugger

[![Build Status](https://travis-ci.org/game-of-things/game-room-service.svg?branch=master)](https://travis-ci.org/game-of-things/game-room-service)

A Python Flask application that displays `/etc/hostname` as an html page. When the application is deployed in k8s, this will be the pod name.

The app may be helpful for demos of pod deployments, scaling, deletions, etc.


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