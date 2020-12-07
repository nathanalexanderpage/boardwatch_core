# Boardwatch

## Concept

In short: a bot to root through postings on secondhand market sites in search of things I want so I don't have to.

## Table of Contents

section		|subsections
---			|---
Features	|Search, Notifications
Structure	|Overview, Database

## Features

### Search

Scourable platforms:
- [x] [Craigslist](https://seattle.craigslist.org/)
- [ ] [eBay](https://www.ebay.com/) ([API](https://developer.ebay.com/Devzone/finding/Concepts/FindingAPIGuide.html))
- [ ] [OfferUp](https://offerup.com/)

### Notifications

Modes of sending findings:
- [x] e-mail
- [ ] on-site messages (combined with tweets?)
- [ ] in-house app

## Setup

__Note:__ Instructional code snippets given here are for Ubuntu.

### PostgreSQL

Install PostgreSQL

```
sudo apt-get install postgresql
```

Create a new user without superuser permissions to avoid unintended consequences as you run many SQL commands.

```
# shell
sudo psql -U postgres

# within psql
CREATE USER your-username-here CREATEDB LOGIN PASSWORD 'your-password-here';
```

In your `.env` file, include the following:

```
POSTGRESQL_USERNAME = "your-username-here"
POSTGRESQL_PASSWORD = "your-password-here"
POSTGRESQL_PORT = 5432
POSTGRESQL_HOST = "localhost"
POSTGRESQL_DBNAME = "boardwatch"
```

Edit the `pg_hba.conf` if necessary to make non-superuser localhost user connections use `md5` authentication method.
You will likely find `pg_hba.conf` in dir `/etc/postgresql/<version>/main/pg_hba.conf`

```
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

Any changes made to `pg_hba.conf` will not take effect until the machine's `postgresql` service has been restarted.

```
sudo service postgresql restart
```

### Required packages
(`requirements.txt` to come)

#### Troubleshooting `psycopg2` Installation Errors
If there are errors installing `psycopg2`, a couple troubleshooting steps:

1. Make sure you have already installed `postgresql`
2. A few resources are required from `libpq-dev`

```
sudo apt-get update
sudo apt-get install libpq-dev
```

## Structure

### Overview

This app runs a scraper that interacts with a database.

Scraper gathers list of posts on first search page, compares list of post IDs to the post IDs of listings which were already scraped.

For listings with new post IDs, it scrapes the page of the individual post. The idea is to go over the post body text with just enough of a fine-toothed comb that it identifies what further combing needs to be done.

Game titles are usually not identifiable from single words unless they involve unique and recognizable character names like Banjo Kazooie or non-words like "robobot". The program will compile a list of keywords to search for in the first once-over (perhaps already narrowed based on post title), then, because each keyword in the list will be mapped to specific games programmatically, a small-ish number of superfine-toothed combs can run over the post text to determine matches with specific titles.

### Database

#### Overview

PostgreSQL, accessed using [psycopg2](https://pypi.org/project/psycopg2/) Python module.
