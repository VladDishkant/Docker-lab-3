# Task 3. Generate more data

## Prerequisites

Done task 2.

## Description

* Use London addresses for simulations below.
* Simulate taxi orders and store in base (with custom intensity).
* Simulate taxi movement tracking and store in base (up to 10GB data).
* Taxi without order are moving at nearest area.
* Simulate taxi drive feedback and store in base.
* Test the result.

## Goals

* Become experience with mongo CRUD.

## Usage

```shell
$ docker-compose up -d
$ docker-compose exec mongoapp /bin/bash
$ python generate.py
```