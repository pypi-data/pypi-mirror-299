# Strig

[![GitHub releases](https://img.shields.io/github/v/release/w-kuipers/strig)](https://github.com/w-kuipers/strig/releases)
[![PyPI release](https://img.shields.io/pypi/v/strig.svg)](https://pypi.org/project/strig/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/github/last-commit/w-kuipers/strig?label=last%20modified)](https://github.com/w-kuipers/strig)


A utility package for Python to generate random strings and numbers.


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#install-using-pip">Install using PIP</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#support">Support</a></li>
    <li><a href="#maintainer">Maintainer</a></li>
    <li><a href="#contributing">Contibruting</a></li>
    <li><a href="#license">License</a></li>

  </ol>
</details>

## Installation

### Install using PIP

    pip install strig

Note that `pip` refers to the Python 3 package manager. In an environment where Python 2 is also present the correct command may be `pip3`.

## Usage

For a more detailed explaination, visit the [documentation](https://github.com/w-kuipers/strig/wiki).

Import strig:

    import strig

Create a random string:

    strig.alpha()

You can specify the string length and a prefix:

    strig.alpha(length=20, prefix='start')

#### Cursor
Currently only SQL cursor objects are supported. If you encounter issues with other cursor objects, please [create an issue](https://github.com/w-kuipers/strig/issues) on GitHub. 
The cursor argument should be a dictionairy structured like the example below:

    #### SQL example
    cursor = {
        "cursor": cursor,
        "table": "table_name",
        "column": "column_name"
    }

    #### MongoDB example
    cursor = {
        "cursor": mongo_client["db"],
        "column": "column_name",
        "type": "mongo"
    }

## Support

If you come across any issues, please [create an issue](https://github.com/w-kuipers/strig/issues) on GitHub.

## Contributing

Your contributions are highly appreciated. Please [create a pull request](https://github.com/w-kuipers/strig/pulls) on GitHub. Bigger changes need to be discussed with the development team via the [issues section at GitHub](https://github.com/w-kuipers/strig/issues) first.


## License

[MIT LICENSE](https://github.com/w-kuipers/strig/blob/master/LICENSE)
