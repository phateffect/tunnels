Tunnels
-------

## How to use
### Install Dependencies
```bash
pipenv install --deploy
```

### Setup your ssh config file
`vim ~/.ssh/config`
```
Host remote_machine
  User your_user_name
  HostName  your_hostname
  Port your_ssh_port
```

#### Testrun
tunnel your local 80 port to remote 8080 port (on `remote_machine`)
```
python tunnel.py name_your_machine 80 8080
```
