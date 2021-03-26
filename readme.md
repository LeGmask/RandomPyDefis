# RandomPyDefis

RandomPyDefis is a Python Discord Bot for random [PyDefis](https://pydefis.callicode.fr/) challenge.

### Config

For setting up the bot, you need :

-   A Discord bot
-   A Discord server
-   Some Users

In `config.json` you will find every common settings that are not private.

In `config_override.json` you will find settings that are private such as your Discord bot token... In this file you can overrite every setting you fin in config.json

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Usage

To run the server, run in your terminal :

```sh
poetry run python main.py
```

### Docker

You can easily setup this project using docker:

1. First download `docker-compose.yml` and `config.json` and default `config_override.json`;
2. Edit settings depending on your server (see [config](#config) part);
3. Run the docker using the following command :

-   run in foreground:

```sh
docker-compose up
```

-   run in background:

```sh
docker-compose up -d
```

_if you need more help see the docker documentation_

<!-- For updating the container:
```sh
docker-compose pull
``` -->

## Licence
See [license](license) for details.
