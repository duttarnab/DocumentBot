name: docbot
command: bash
volumes:
- /root/.cache/pip
sync:
- .:/app
forward:
- 5005:5005
reverse:
- 8080:8080