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

This app runs a scraper that interacts with a database.

Scraper gathers list of posts on first search page, compares list of post IDs to the post IDs of listings which were already scraped.

For listings with new post IDs, it scrapes the page of the individual post. The idea is to go over the post body text with just enough of a fine-toothed comb that it identifies what further combing needs to be done.

Game titles are usually not identifiable from single words unless they involve unique and recognizable character names like Banjo Kazooie or non-words like "robobot". The program will compile a list of keywords to search for in the first once-over (perhaps already narrowed based on post title), then, because each keyword in the list will be mapped to specific games programmatically, a small-ish number of superfine-toothed combs can run over the post text to determine matches with specific titles.

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

#### Document Schema (normalized view)

##### `consoles` (platforms)

data						|type	|rules
---							|---	|---
id							|int	|PK
name						|text	|NOT NULL
generation					|int	|NULL
abbreviation_official		|text	|NULL
developer					|id		|company_id NOT NULL
name_group					|id		|name_group_id NOT NULL
name_prefix					|text	|NULL
name_suffix					|text	|NULL
name_alternatives			|id[]	|name_alt_id
variations					|id[]	|variation_id

##### `variations`

data				|type			|rules
---					|---			|---
id					|int			|PK
name				|text			|NULL
model_no			|text			|NULL
storage				|embed[]		|(see table: embedded_A)
editions			|embed			|(see table: embedded_B)

##### `storage` (embedded_A)

data					|type		|rules
---						|---		|---
capacity				|int		|NULL
unit					|text		|NULL
type					|text		|NULL

##### `editions` (embedded_B)

data				|type		|rules
---					|---		|---
name				|text		|NULL
colors				|id[]		|color_id

##### `colors`

data				|type		|rules
---					|---		|---
id					|int		|PK
name				|text		|NULL
similar_colors		|id[]		|color_id

##### `games`

data				|type		|rules
---					|---		|---
id					|int		|PK
name				|text		|NULL
platforms			|id[]		|console_id
date_first_release	|int		|NULL
is_bootleg			|boolean	|NOT NULL

##### `peripherals` (accessories)

TBD

##### `users`

data					|type		|rules
---						|---		|---
id						|int		|PK
e-mail					|text		|NOT NULL, UNIQUE
username				|text		|NOT NULL, UNIQUE
password				|text		|NOT NULL, HASH
watch_list				|embed		|(see table: embedded_C)

##### `watch_list` (embedded_C)

data				|type			|rules
---					|---			|---
consoles			|embed[]		|(see table: embedded_D)
games				|embed[]		|(see table: embedded_E)
peripherals			|embed[]		|(see table: embedded_F)

#### Document Schema (non-normalized view)

##### `consoles` (platforms)

template:
```
{
	id: id,
	type: item_type_id,
	name: text,
	name_group: text | null,
	name_prefix: text | null,
	name_suffix: text | null,
	abbreviation_official: text | null,
	developer: company_id | null,
	generation: int | null,
	names_other: text[],
	variations: variation_id[]
}
```

example (collapsed):
```
{
	"id": "584d947dea542a13e9ec7ae7",
	"type": "console",
	"name": "Wii",
	"name_group": "Wii",
	"name_prefix": null,
	"name_suffix": null,
	"abbreviation": null,
	"developer": "Nintendo",
	"generation": 7,
	"names_other": [
		"Revolution"
	],
	"variations": variation_id[]
}
```

##### `variations`

template:
```
{
	id: id,
	name: text | null,
	model_no: text | null,
	storage: [
		{
			capacity: int,
			unit: text | null,
			type: text | null
		},
		...
	],
	editions: [
		{
			name: text,
			colors: color_id[]
		},
		...
	]
}
```

example (collapsed):
```
{
	"id": "584d947dea542a13e9ec7ae7",
	"name": null,
	"model_no": "RVL-001",
	"storage_capacity": embed,
	"editions": embed[]
}
```

##### `storage` (embedded_A)

template:
```
{
	capacity: int,
	unit: text,
	type: text
}
```

example:
```
{
	capacity: 512,
	unit: "MB",
	type: disk
}
```

##### `editions` (embedded_B)

template:
```
{
	name: text,
	colors: color_id[]
}
```

example (collapsed):
```
{
	"name": "25th Anniversary Edition",
	"colors": color_id[]
}
```

##### `colors`

template:
```
{
	id: id,
	name: text,
	similar_colors: similar_color_id[]
}
```

example (collapsed):
```
{
	id: id,
	name: text,
	similar_colors: similar_color_id[]
}
```

##### `colors_common`

template:
```
{
	id: id,
	name: text
}
```

example:
```
{
	id: id,
	name: text
}
```

##### `games`

template:
```
{
	id: id,
	name: text,
	first_release_date: int,
	platforms: console_id[]
}
```

example:
```
{
	"id": "584d947dea542a13e9ec7ae7",
	"name": "Captain Toad: Treasure Tracker",
	"first_release_date": 1415836800,
	"platforms": console_id[]
}
```

##### `peripherals` (accessories)

TBD

##### `users`

template:
```
{
	id: id,
	email: text,
	username: text,
	password: text,
	watch_list: embedded_C
}
```

example (collapsed):
```
{
	id: id,
	email: address@domain.tld,
	username: ya_boi,
	password: 14$ya_bois_pw_hashed,
	watch_list: embedded_C
}
```

##### `watch_list` (embedded_C)

template:
```
{
	consoles: embed[],
	games: embed[],
	peripherals: embed[]
}
```

example (collapsed):
```
{
	consoles: embedded_CA[],
	games: embedded_CB[],
	peripherals: embedded_CC[]
}
```
##### `console_watch` (embedded_CA)

template:
```
{
	console_id: id,
	desired_variations: variation_id[],
	desired_price: int
}
```

example (collapsed):
```
{
	console_id: id,
	desired_variations: variation_id[],
	desired_price: 60
}
```

##### `game_watch` (embedded_CB)

TBD

template:
```
{
	console_id: id,
	desired_compatible_consoles: console_id[],
	desired_price: int
}
```

example (collapsed):
```
{
	console_id: id,
	desired_compatible_consoles: console_id[],
	desired_price: 20
}
```

##### `peripheral_watch` (embedded_CC)

TBD
