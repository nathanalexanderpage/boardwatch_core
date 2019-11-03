# Boardwatch

## Concept

In short: a bot to root through postings on secondhand market sites in search of things I want so I don't have to.

## Table of Contents

section		|subsections
---				|---
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
* item_watches (who wants what)

#### Document Schema (normalized view)

##### `consoles` (platforms)

data									|type	|rules
---										|---	|---
id										|int	|PK
name									|text	|NOT NULL
generation						|int	|NULL
abbreviation_official	|text	|NULL
developer							|id		|company_id NOT NULL
name_group						|id		|name_group_id NOT NULL
name_prefix						|text	|NULL
name_suffix						|text	|NULL
name_alternatives			|id[]	|name_alt_id
variations						|id[]	|variation_id

##### `variations`

data					|type			|rules
---						|---			|---
id						|int			|PK
name					|text			|NULL
model_no			|text			|NULL
storage				|embed[]	|(see table: embedded_A)
editions			|embed		|(see table: embedded_B)

##### `storage` (embedded_A)

data					|type		|rules
---						|---		|---
capacity			|int		|NULL
unit					|text		|NULL
type					|text		|NULL

##### `editions` (embedded_B)

data					|type		|rules
---						|---		|---
name					|text		|NULL
colors				|id[]		|color_id

##### `colors`

data						|type		|rules
---							|---		|---
id							|int		|PK
name						|text		|NULL
similar_colors	|id[]		|color_id

##### `games`

data								|type		|rules
---									|---		|---
id									|int		|PK
name								|text		|NULL
platforms						|id[]		|console_id
date_first_release	|int		|NULL
is_bootleg					|boolean	|NOT NULL

##### `peripherals` (accessories)

data					|type		|rules
---						|---		|---
id						|int		|PK
TBD

##### `users`

data						|type		|rules
---							|---		|---
id							|int		|PK
e-mail					|text		|NOT NULL, UNIQUE
username				|text		|NOT NULL, UNIQUE
password				|text		|NOT NULL, HASH
item_watches		|embed	|(see table: embedded_C)

##### `item_watches` (embedded_C)

data					|type			|rules
---						|---			|---
consoles			|embed[]	|(see table: embedded_D)
games					|embed[]	|(see table: embedded_E)
peripherals		|embed[]	|(see table: embedded_F)

#### Document Schema (non-normalized view)

##### `consoles` (platforms)

template:
```
{
	id: text,
	type: item_type_id,
	name: text,
	name_group: text | null,
	name_prefix: text | null,
	name_suffix: text | null,
	abbreviation_official: text | null,
	developer: company_id | null,
	generation: int | null,
	names_other: [
		text,
		...
	],
	variations: [
		{
			id: text,
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
					colors: [color_id, ...]
				},
				...
			]
		},
		...
	]
}
```

example:
```
{
	'id': '584d947dea542a13e9ec7ae7',
	'type': 'console',
	'name': 'Wii',
	'name_group': 'Wii',
	'name_prefix': null,
	'name_suffix': null,
	'abbreviation': null,
	'developer': 'Nintendo',
	'generation': 7,
	'names_other': [
		'Revolution'
	],
	'variations': [
		{
			'id': '584d947dea542a13e9ec7ae7',
			'name': null,
			'model_no': 'RVL-001',
			'storage_capacity': '512MB',
			'editions': [
				{
					'name': '25th Anniversary Edition',
					'colors': ['red']
				},
				...
			]
		},
		{
			'id': '584d947dea542a13e9ec7ae7',
			'name': 'Mini',
			'model_no': 'RVL-201',
			'storage_capacity': null,
			'editions': [
				{
					'name': null,
					'colors': ['red', 'black']
				}
			]
		}
	]
}
```

##### `variations`

template:
```
{
	id: text,
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
			colors: [color_id, ...]
		},
		...
	]
}
```

example:
```
{
	'id': '584d947dea542a13e9ec7ae7',
	'name': null,
	'model_no': 'RVL-001',
	'storage_capacity': '512MB',
	'editions': [
		{
			'name': '25th Anniversary Edition',
			'colors': ['red']
		},
		...
	]
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
	id: text,
}
```

example:
```
{
	'name': '25th Anniversary Edition',
	'colors': ['red']
}
```

##### `colors`

template:
```
{
	id: text,
}
```

example:
```
{}
```

##### `games`

template:
```
{
	id: text,
}
```

example:
```
{}
```

##### `peripherals` (accessories)

template:
```
{
	id: text,
}
```

example:
```
{}
```

##### `users`

template:
```
{
	id: text,
}
```

example:
```
{}
```

##### `item_watches` (embedded_C)

template:
```
{
	consoles: embed[],
	games: embed[],
	peripherals: embed[]
}
```

example:
```
{
	consoles: console_watch[],
	games: game_watch[],
	peripherals: peripheral_watch[]
}
```
##### `console_watch`

template:
```
{
	id: text,
}
```

example:
```
{}
```

##### `game_watch`
TBD
template:
```
{
	id: text,
}
```

example:
```
{}
```

##### `peripheral_watch`
TBD
template:
```
{
	id: text,
}
```

example:
```
{}
```