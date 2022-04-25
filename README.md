# Products Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Build Status](https://github.com/NYU-DevOps-Class-Product-Squad/products/actions/workflows/main.yml/badge.svg)](https://github.com/NYU-DevOps-Class-Product-Squad/products/actions)

[![codecov](https://codecov.io/gh/NYU-DevOps-Class-Product-Squad/products/branch/main/graph/badge.svg?token=XAFTPW0V0T)](https://codecov.io/gh/NYU-DevOps-Class-Product-Squad/products)



## Overview

This is the products service, which is used to list, create, read, update, and delete products in the products database.

## Contents

The project contains the following:

```text
.coveragerc         - settings file for code coverage options
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/      - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                - service python package
├── __init__.py         - package initializer
├── error_handlers.py   - HTTP error handling code
├── models.py           - module with business models
├── routes.py           - module with service routes
└── status.py           - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for busines models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
