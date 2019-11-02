# Boardwatch

## Concept

A bot to scour postings on secondhand market sites so I don't have to.

## Features

### Search

Scourable platforms:
- [x] [Craigslist](https://seattle.craigslist.org/)
- [ ] [eBay](https://www.ebay.com/)
- [ ] [LetGo](https://us.letgo.com/en)
- [ ] [OfferUp](https://offerup.com/)

### Notifications

Modes of sending findings:
- [x] e-mail
- [ ] on-site messages (combined with tweets?)
- [ ] in-house app

## Structure

### Overview


### Database

#### Overview

MongoDB database.

Tables List:
* consoles/platforms
* console name groups
* console variations
* console colors
* companies
* games
* peripherals/accessories
* users
* watches (who wants what)
* item types

#### Document Schema

##### `consoles` (platforms)

data					|type	|rules
---						|---	|---
id						|int	|PK, NOT NULL
name					|text	|NOT NULL
generation				|int	|NULL
year					|int	|NULL
abbreviation_official	|text	|NULL
developer				|id		|company_id NOT NULL
name_group				|id		|name_group_id NOT NULL
name_prefix				|text	|NULL
name_suffix				|text	|NULL
name_alternatives		|id[]	|name_alt_id
variations				|id[]	|variation_id

##### `variations`

data					|type		|rules
---						|---		|---
id						|int		|PK, NOT NULL
name					|text		|NULL
model_no				|text		|NULL
storage					|embed[]	|(see table: embedded_A)
editions				|embed		|(see table: embedded_B)

##### `storage` (embedded_A)

data					|type		|rules
---						|---		|---
capacity				|int		|NULL
unit					|text		|NULL
type					|text		|NULL

##### `editions` (embedded_B)

data					|type		|rules
---						|---		|---
name					|text		|NULL
colors					|id[]		|color_id

##### `colors`

data					|type		|rules
---						|---		|---
id						|int		|PK, NOT NULL
name					|text		|NULL
similar_colors			|id[]		|color_id

##### `games`

data					|type		|rules
---						|---		|---
id						|int		|PK, NOT NULL
name					|text		|NULL
platforms				|id[]		|console_id
date_first_release		|int		|NULL
is_bootleg				|boolean	|NOT NULL

##### `peripherals` (accessories)

data					|type		|rules
---						|---		|---
id						|int		|PK, NOT NULL
TBD

##### `users`

data					|type		|rules
---						|---		|---
id						|int		|PK, NOT NULL
TBD

##### `watches` (who wants what)

data					|type		|rules
---						|---		|---
id						|int		|PK, NOT NULL
TBD

##### `item_types`

data					|type		|rules
---						|---		|---
id						|int		|PK, NOT NULL
TBD
