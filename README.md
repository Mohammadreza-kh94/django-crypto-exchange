# Cryptocurrency Exchange App

This is a Django Rest Framework (DRF) app that allows users to buy and sell cryptocurrencies on an online exchange.
The app is built using the DRF framework and leverages Django's built-in user authentication system for managing user accounts and login sessions. It uses PostgreSQL as its database backend to store user and transaction data.

## key features:

- User authentication and registration
- Wallet management for storing and tracking cryptocurrency balances
- Order a cryptocurrency
- Purchase history tracking for viewing past transactions

## Requirements:

| Requirement | Specification          |
| ----------- | ---------------------- |
| OS          | Ubuntu 18.04 or higher |
| Language    | Python                 |
| Interpreter | Python 3.8+            |

## Local Development QuickStart:

### - Using docker-compose:

Dependencies:

- `docker` and `docker-compose`

  ```bash
  # install
  $ git clone https://github.com/Mohammadreza-kh94/django-crypto-exchange.git
  $ cd django-crypto-exchange

  # configure (the defaults are fine for development)
  $ edit `.env.sample` and save as `.env`

  # run it
  $ docker-compose up --build
  ```

  Once it's done building and everything has booted up:

  - Access the app at: [http://localhost:8000](http://localhost:8000)

### - Running locally

- Dependencies:

  - Linux system
  - Python 3.8+
  - virtualenv
  - PostgreSQL

- Installation

  ```bash
  # install
  $ git clone https://github.com/Mohammadreza-kh94/django-crypto-exchange.git
  $ cd django-crypto-exchange
  $ virtualenv -p /path/to/python3 venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt

  # configure
  $ edit `.env.sample` and save as `.env`

  # run db migrations
  $ python manage.py migrate

  # backend dev server:
  $ python manage.py runserver
  ```
