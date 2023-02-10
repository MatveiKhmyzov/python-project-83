### Hexlet tests and linter status:
[![Actions Status](https://github.com/MatveiKhmyzov/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/MatveiKhmyzov/python-project-83/actions)
[![page-analyzer](https://github.com/MatveiKhmyzov/python-project-83/actions/workflows/page-analyzer.yml/badge.svg)](https://github.com/MatveiKhmyzov/python-project-83/actions/workflows/page-analyzer.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/6d63fcc571935912a0ce/maintainability)](https://codeclimate.com/github/MatveiKhmyzov/python-project-83/maintainability)

### About project
Website that mimics the basic functionality of analyzing the specified page for SEO suitability 
(checking the availability of the site, the presence of some tags). It based on Flask framework and contain
basic principles of building modern sites on the MVC-architecture.
### Installation
Versions of Python and Poetry are 3.10 and 1.1.13 respectively.
It also needs in PostgreSQL as database and for work with database is psycopg2-binary with 2.9.5-version
For correct work of application, it is necessary to create .env file in root directory of project with
variables: DATABASE_URL (database connection string) and SECRET_KEY (session secret key).
### Link to domain
https://python-project-83-production-b978.up.railway.app/