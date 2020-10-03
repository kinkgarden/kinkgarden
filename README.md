# [kink.garden](https://kink.garden)

[![Travis build status](https://img.shields.io/travis/com/kinkgarden/kinkgarden?style=flat-square)][travis]
[![Code Climate coverage](https://img.shields.io/codeclimate/coverage/kinkgarden/kinkgarden?style=flat-square)][codeclimate]
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/kinkgarden/kinkgarden?style=flat-square)][codeclimate]
![GitHub license](https://img.shields.io/github/license/kinkgarden/kinkgarden?style=flat-square)
[![Twitter Follow](https://img.shields.io/twitter/follow/kinkgarden?style=social)][twitter]

[travis]: https://travis-ci.com/github/kinkgarden/kinkgarden
[codeclimate]: https://codeclimate.com/github/kinkgarden/kinkgarden
[twitter]: https://twitter.com/kinkgarden

kink.garden is a project that aims to create a website where you can make a
**list of your kinks** that you can share with friends, the world, or no one but
yourself!

this project was started and conceptualized **by queer people, for queer
people**. it is being built from the ground up to be queer-inclusive, always
with respectfulness in mind. you won't have to worry about bigotry, objectifying
slurs, or tastelessly fetishizing marginalized people.

## developing

1. install [python](https://www.python.org) and
   [Docker Desktop](https://www.docker.com/get-started)
2. clone this repository
3. prepare secrets:
    ```shell script
    docker run --rm python:alpine python -c "import string,random;print(''.join(random.choices(string.ascii_letters,k=30)))" > ./secrets/secret-key
    ```
4. run the server:
    ```shell script
    docker-compose up --build
    ```
5. give yourself an admin account to make local test data:
    ```shell script
    docker-compose exec django python manage.py createsuperuser
    ```

in theory, that should get you going, with the server on http://localhost:8000/.

we use [black](https://github.com/psf/black) and
[prettier](https://prettier.io/) to manage code formatting. you can set up their
respective editor integrations if you like, or you can fix everything at once
after the fact:

```shell script
black .
npx prettier --write .
```
