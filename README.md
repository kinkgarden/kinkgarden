# [kink.garden](https://kink.garden)

[![Travis build status](https://img.shields.io/travis/com/kinkgarden/kinkgarden?style=flat-square)][travis] [![Code Climate coverage](https://img.shields.io/codeclimate/coverage/kinkgarden/kinkgarden?style=flat-square)][codeclimate] [![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/kinkgarden/kinkgarden?style=flat-square)][codeclimate] ![GitHub license](https://img.shields.io/github/license/kinkgarden/kinkgarden?style=flat-square) [![Twitter Follow](https://img.shields.io/twitter/follow/kinkgarden?style=social)][twitter]

[travis]: https://travis-ci.com/github/kinkgarden/kinkgarden
[codeclimate]: https://codeclimate.com/github/kinkgarden/kinkgarden
[twitter]: https://twitter.com/kinkgarden

kink.garden is a project that aims to create a website where you can make a **list of your kinks** that you can share with friends, the world, or no one but yourself!

this project was started and conceptualized **by queer people, for queer people**. it is being built from the ground up to be queer-inclusive, always with respectfulness in mind. you won't have to worry about bigotry, objectifying slurs, or tastelessly fetishizing marginalized people.

## developing

1. install [python](https://www.python.org) and [node.js](https://nodejs.org/en/)
2. clone this repository
3. install dependencies:
   ```shell script
   pip install -r requirements.txt
   npm install
   ```
4. copy `kinkgarden/ci_settings.py` to `kinkgarden/local_settings.py` and delete the first line (`from .settings import *`)
5. build the editor:
   ```shell script
   npm run build -- --mode=development
   ```
   (if you're going to be editing it, use `watch` instead of `build` and open a new terminal for the next steps)
6. set up the database and give yourself an admin account to make local test data:
   ```shell script
   python manage.py migrate
   python manage.py createsuperuser
   ```
7. run the server:
   ```shell script
   python manage.py runserver
   ```

in theory, that should get you going.
