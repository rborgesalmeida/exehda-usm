GeoIP Update Change Log
=======================

2.2.1 (2015-02-25)
------------------

* Bump version number to correct PPA release issue. No other changes to the
  source distribution.


2.2.0 (2015-02-25)
------------------

* `geoipupdate` now verifies the MD5 of the new database before deploying it.
  If the database MD5 does not match the expected MD5, `geoipupdate` will
  exit with an error.
* The copy of `base64.c` and `base64.h` was switched to a version under GPL 2+
  to prevent a license conflict.
* The `LICENSE` file was added to the distribution.
* Several issues in the documentation were fixed.

2.1.0 (2014-11-06)
------------------

* Previously `geoipupdate` did not check the status code of an HTTP response.
  It will now check for an unexpected status code and exit with a warning if
  such a status is received.
* The client now checks the return value of gz_close to ensure that the gzip
  stream was correctly decoded. GitHub PR #18.
* The client now checks that the file was correctly opened. Previous versions
  used an incorrect check.

2.0.2 (2014-07-22)
------------------

* The client now uses a single TCP connection when possible. Previously the
  public IP address of a host could change across requests, causing the
  authentication to fail. Reported by Aman Gupta. GitHub issue #12 and #13.
* ` geoipupdate-pureperl.pl` was updated to work with GeoIP2.

2.0.1 (2014-05-02)
------------------

* Error handling was generally improved. `geoipupdate` will now return a 1
  whenever an update fails.
* Previously if one database failed to be updated, `geoipupdate` would not
  attempt to download the remaining databases. It now continues to the next
  database when a download fails.
* Support for Mac OS X 10.6, which is missing the `getline` function, was
  added.
* Unknown directives in the configuration file will now be logged.
* The debugging output was improved and made more readable.
* Several documentation errors and typos were fixed.

2.0.0 (2013-10-31)
------------------

* First stand-alone release.
