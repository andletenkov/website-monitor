## Website monitoring
Simple monitoring system that monitors websites and puts results to database through Kafka topic. Built on top of Aiven Kafka & PostgeSQL services.

## Prerequisites
* Python 3.9
* Aiven Kafka 2.7.1 running instance
* Aiven PostgreSQL 13 running instance

## Running via commandline
1. Clone project source code to your machine
```bash
git clone git@github.com:aiven-recruitment/swet-20212408-andletenkov.git
```
2. Install project dependencies
```bash
pip install poetry
poetry install
```
3. Put service credentials and monitoring configurations to `config/config.yml` according to `config/config.example.yml`
4. Run application as python module (assume you have poetry env already activated)
```bash
python -m monitor 
```
You also could run tests to check everything is OK:
```bash
pytest -v -s 
```