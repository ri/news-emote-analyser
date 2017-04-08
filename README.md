# News Emote Analyser

News source headline scraper and analyser for, viewable with
[news-emote](https://github.com/ri/news-emote)

## Development

First time on new computer/clone:

```
$ git clone https://github.com/ri/news-emote-analyser analyser
$ cd analyser
$ virtualenv .
$ source bin/activate  # enters the project's virtualenv
(analyser) $ pip install -r requirements.txt
```

Then every time after:

```
$ source bin/activate  # enters the project's virtualenv
(analyser) $ ...
```

After installing new dependencies with `pip`:

```
(analyser) $ pip install "new-dependency"
(analyser) $ pip freeze > requirements.txt
(analyser) $ git add requirements.txt
```

Running the scraper:

```
(analyser) $ python newsemote.py [au|us|all]
```

You may have to put S3 credentials in `~/.boto` [as described here](http://boto.cloudhackers.com/en/latest/boto_config_tut.html).

## Deployment

Analyser is deployed on Heroku using the Python and PhantomJS buildpacks.

S3 credentials for storing the resulting data files are in Heroku environment variables and can be viewed with `heroku config` and changed with `heroku config:set`.

The Scheduler add-on runs the scraper for each region daily. To run them manually on Heroku, run:

```
$ heroku run -a news-emote-analyser python newsemote.py [au|us|all]
```
