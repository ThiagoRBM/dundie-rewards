# How to use


## Load data

Having a file `people.csv` with the following format:

```csv
fulano, sales, salesman, fulano@dunder.com
ciclano, sales, manager, ciclano@dunder.com
beltrano, directory, manager, beltrano@dunder.com
```

Run `dundie load` command

```py
dundie load people.csv
```

## Viewing data

### Viewing all information

```bash
$ dundie show
                                    Dunder Mifflin Report
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
┃ Email               ┃ Balance ┃ Last_Movement              ┃ Name     ┃ Dept    ┃ Role     ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
│ fulano@dunder.com   │ 500     │ 2022-09-08T14:53:51.893904 │ fulano   │ sales   │ salesman │
│ ciclano@dunder.com  │ 100     │ 2022-09-08T14:53:51.895931 │ ciclano  │ sales   │ manager  │
│ beltrano@dunder.com │ 500     │ 2022-09-08T14:53:51.898356 │ beltrano │ C-Level │ CEO      │
└─────────────────────┴─────────┴────────────────────────────┴──────────┴─────────┴──────────┘
```

### Filtering

Available filters are `--dept` and `--email`

```bash
dundie show --dept=Sales
                                        Dunder Mifflin Report
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Email              ┃ Balance ┃ Last_Movement              ┃ Name    ┃ Dept  ┃ Role     ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ fulano@dunder.com  │ 500     │ 2022-09-08T14:53:51.893904 │ fulano  │ sales │ salesman │
│ ciclano@dunder.com │ 100     │ 2022-09-08T14:53:51.895931 │ ciclano │ sales │ manager  │
└────────────────────┴─────────┴────────────────────────────┴─────────┴───────┴──────────┘
```

> **NOTE** passing `--output=file.json` will save a json file with the results.


## Adding points

An admin user can easily add points to any user or dept.

```bash
dundie add 100 --email=fulano@dunder.com
                                 Dunder Mifflin Report
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Email             ┃ Balance ┃ Last_Movement              ┃ Name   ┃ Dept  ┃ Role     ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ fulano@dunder.com │ 600     │ 2022-09-11T12:27:35.454454 │ fulano │ sales │ salesman │
└───────────────────┴─────────┴────────────────────────────┴────────┴───────┴──────────┘

```

Available selectors are `--email` and `--dept`
