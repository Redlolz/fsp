# FSP

File Server with Password

## Usage

Use setup.sh to setup the virtual environment

```bash
$ ./setup.sh
```

Edit the config.json

```json
{
    "webhost":"0.0.0.0",
    "webport":8080,
    "password":"1234",
    "path":"/home/user/Documents"
}
```

Start the server

```
$ ./fsp.sh
```