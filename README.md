# Flask RESearch NOTEbook

[![Documentation Status](https://readthedocs.org/projects/pip/badge/?version=stable)](https://pip.pypa.io/en/stable/?badge=stable) [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

**F**lask **res**earch **note**book (`fresnote`) is a browser-based note-taking application suitable for managing and organizing personal and research projects. It uses Flask as backend and Bootstrap as frontend.

![main figure](https://github.com/dkioroglou/fresnote/blob/main/docs/images/main_figure.png)

``fresnote`` is based on the following rationale:

* User creates **projects**.
* Each project has one or more **notebooks**.
* Each notebook has one or more **chapters**.
* Each chapter has one or more **sections**.

## Installation

`fresnote` has been developed with `python 3.8` and has Flask as the only dependency. Necessary HTML templates, CSS and JS files are included in the installation for offline use.

To install **fresnote** run:

```
pip install fresnote
```

Testing of `fresnote` has been done on a typical x86 64bit Linux-based machine running Ubuntu 16.04 and on an Android 9.0 device (via Termux). HTML rendering was similar on both Chrome and Firefox browsers. No issues are expected on macOS and Windows devices.

## Run fresnote

Create an empty `.ini` file. Example `fresnote.ini`.
Run:
```
fresnote -c fresnote.ini
```

Open your preferred browser and enter the following url:
```
http://127.0.0.1:5000/
```

If you want to specify different port:
```
fresnote -c fresnote.ini -p [PORT]
```


## Documentation

You can read the full documentation here: [https://fresnote.readthedocs.io](https://fresnote.readthedocs.io/en/latest/)


## License

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
