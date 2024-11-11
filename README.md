Requires : python3.12

# Active environment
```sh
python3.12 -m venv venv
source venv/bin/activate
```

# Start databases dev
```sh
make start_docker_compose
```

# Install dependencies
```sh
make install_dev
```

# Apply migration
```sh
make migrate
```

# Run tests
```sh
make test
```

# Run server
```sh
make run_dev
```
