The directory `docs` contains all the files related to the ontology, its versions in time, and the related documentations. In particular, it includes:

* the `current` directory, where the files of the current version of the ontology are stored;
* one `yyyy-mm-dd` version directory for each of the versions of the ontology developed.

The `current` directory contains a `.owl` file named after the lowercase ontology acronym, which is the source of the ontology in a particular format between RDF/XML, Turtle, N-triples, or JSON-LD. In addition to this file, the directory includes five other files, named in the same way and with the following extensions specifying each of five different formats: `.xml` (RDF/XML), `.ttl` (Turtle), `.nt` (Ntriple), `.json` (JSON-LD), `.html` (HTML, i.e. the human readable documentation of the ontology). All the images used in the documentation should additionally be included in this `.html` directory.

The version directories (i.e. `yyyy-mm-dd`) contains the same kinds of files as those included in the `current` directory, but specific for that particular version. However, the `.owl` file should be present only in the `current` directory.
