KiCad-GetLibs
=============

This is a rudimentary python script to help maintain a local copy of the official
KiCad footprint libraries from GitHub.

New style KiCad footprint libraries are folders named \*.pretty and are stored
as separate repos at <https://github.com/kicad>.  You can use them directly from
GitHub using the GitHub library type, but if you haven't got an internet connection
or want them local for some reason there are over 70 to clone individually.

This script uses the GitHub API to:
1. Clone a repository if it is one of the \*.pretty libraries and you don't have it
2. Pull the repository if you already have it locally (does an update).
3. Optionally update your fp-lib-table marking the auto-maintained repositories

Usage
-----

`python kicad-getlibs.py [options] [<local folder>]`

The optional local folder is the folder you want all your local git repositories
put in.  If you don't provide it the script will try and read the `KISYSMOD` 
environment variable and use that folder as the destination.  Note that if you
do specify the folder and don't use absolute URIs when updating fp-lib-table
the script will assume `KISYSMOD` is set to \<local folder\>.

Options are:

-h, --help  Shows a help screen on the command line

-v, --verbose  Shows the git progress for each repository

-q, --quiet  Don't show the repository names as they are tried

-t, --table  Update the fp-lib-table (not done by default)

-a, --absolute  Use the absolute path to each local repository, otherwise a path
relative to ${KISYSMOD} is used.

The first run will probably copy your existing fp-lib-table to fp-lib-table-old
and create a new one.  From that point on a special `auto=true` option added to
each of the automatically added libraries will mark only them for update and
any additional custom libraries will be kept.

**Example Usage**

Using KISYSMOD environment variable:

    python kicad-getlibs.py -tv

Specifying a local path manually:

    python kicad-getlibs.py -avt kicad-libs

**Dependencies**

It should just run with a standard distribution of python 2.x, there are no
special libraries used.  You'll need to have git installed and I've only tested
on Kubuntu 12.04.

Bugs/Feauture Requests
----------------------

Let me know either at <nathan@nathandumont.com> or via [@hairymnstr](https://twitter.com/hairymnstr) on twitter.

