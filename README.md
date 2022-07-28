# Website

## Installation

This project handles commands using [`just`](https://github.com/casey/just), and the project runs in Docker.

1. `just build`
2. Create [`.env` file](#env-file)
3. `just compose up -d`
4. `just compose run web just start`

### `.env` file

Local development secrets are stored in a `.env` file. This file is automatically loaded by `just`.
