|travis|_ |codecov|_

Revision Scoring
================
A generic, machine learning-based revision scoring system designed to be used
to automatically differentiate damage from productive contributory behavior on
Wikipedia.

Example
========

Using a scorer_model to score a revision::

  >>> import mwapi
  >>> from revscoring import ScorerModel
  >>> from revscoring.extractors.api.extractor import Extractor
  >>>
  >>> with open("models/enwiki.damaging.linear_svc.model") as f:
  ...     scorer_model = ScorerModel.load(f)
  ...
  >>> extractor = Extractor(mwapi.Session(host="https://en.wikipedia.org",
  ...                                        user_agent="revscoring demo"))
  >>>
  >>> feature_values = list(extractor.extract(123456789, scorer_model.features))
  >>>
  >>> print(scorer_model.score(feature_values))
  {'prediction': True, 'probability': {False: 0.4694409344514984, True: 0.5305590655485017}}


Installation
============
The easiest way to install `revscoring` is via the Python package installer
(pip).

``pip install revscoring``

You may find that some of `revscorings` dependencies fail to compile (namely
`scipy`, `numpy` and `sklearn`).  In that case, you'll need to install some
dependencies in your operating system.

Ubuntu & Debian:
  Run ``sudo apt-get install python3-dev g++ gfortran liblapack-dev libopenblas-dev``
Windows:
  'TODO'
MacOS:
  Using Homebrew and pip, installing `revscoring` and `enchant` can be accomplished
  as follows::

      brew install aspell --with-all-languages
      brew install enchant
      pip install --no-binary pyenchant revscoring
  Languages can be added to `aspell`::

      cd /tmp
      wget http://ftp.gnu.org/gnu/aspell/dict/pt/aspell-pt-0.50-2.tar.bz2
      bzip2 -dc aspell-pt-0.50-2.tar.bz2 | tar xvf -
      cd aspell-pt-0.50-2
      ./configure
      make
      sudo make install
  Caveats:
    * The differences between the `aspell` and `myspell` dictionaries can cause
      some of the tests to fail


Finally, in order to make use of language features, you'll need to download
some NLTK data.  The following command will get the necessary corpus.

``python -m nltk.downloader stopwords``

You'll also need to install `enchant <https://enchant.org>`_ compatible
dictionaries of the languages you'd like to use.  We recommend the following:

* ``languages.arabic``: aspell-ar
* ``languages.czech``: myspell-cs
* ``languages.dutch``: myspell-nl
* ``languages.english``: myspell-en-us myspell-en-gb myspell-en-au
* ``languages.estonian``: myspell-et
* ``languages.french``: myspell-fr
* ``languages.german``: myspell-de-at myspell-de-ch myspell-de-de
* ``languages.hebrew``: myspell-he
* ``languages.hungarian``: myspell-hu
* ``languages.indonesian``: aspell-id
* ``languages.italian``: myspell-it
* ``languages.norwegian``: myspell-nb
* ``languages.persian``: myspell-fa
* ``languages.polish``: aspell-pl
* ``languages.portuguese``: myspell-pt
* ``languages.spanish``: myspell-es
* ``languages.swedish``: aspell-sv
* ``languages.tamil``: aspell-ta
* ``languages.russian``: myspell-ru
* ``languages.ukrainian``: myspell-uk
* ``languages.vietnamese``: hunspell-vi

Authors
=======
    Aaron Halfaker:
        * `http://halfaker.info`
    Helder:
        * `https://github.com/he7d3r`
    Adam Roses Wight:
        * `https://mediawiki.org/wiki/User:Adamw`
    Amir Sarabadani:
	* `https://github.com/Ladsgroup`

.. |travis| image:: https://api.travis-ci.org/wiki-ai/revscoring.png
.. _travis: https://travis-ci.org/wiki-ai/revscoring
.. |codecov| image:: https://codecov.io/github/wiki-ai/revscoring/revscoring.svg
.. _codecov: https://codecov.io/github/wiki-ai/revscoring
