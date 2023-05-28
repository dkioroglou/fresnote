# Flask RESearch NOTEbook

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

**F**lask **res**earch **note**book (`fresnote`) is a browser-based note-taking application suitable for managing and organizing personal and research projects. It uses Flask as backend and Bootstrap as frontend.

![main figure](https://github.com/dkioroglou/fresnote/blob/main/docs/images/main_figure.png)

``fresnote`` is based on the following rationale:

* User creates **projects**.
* Each project has one or more **notebooks**.
* Each notebook has one or more **chapters**.
* Each chapter has one or more **sections**.

## Installation

`fresnote` has been tested with python 3.8 and has Flask as the only dependency. Necessary HTML templates, CSS and JS files are automatically installed upon installation. 

To install **fresnote** run:

```
pip install fresnote
```

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

Coming soon.


## License

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
