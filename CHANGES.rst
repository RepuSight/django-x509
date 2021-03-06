Changelog
=========

Version 0.1.3 [2016-09-22]
--------------------------

* [model] avoid import error if any imported field is ``NULL``
* [admin] added ``serial_number`` to ``list_display`` in ``Cert`` admin
* [model] avoid exception if x509 subject attributes are empty

Version 0.1.2 [2016-09-08]
--------------------------

* improved general ``verbose_name`` of the app
* added official compatibility with django 1.10
* [admin] show link to CA in cert admin
* [admin] added ``key_length`` and ``digest`` to available filters

Version 0.1.1 [2016-08-03]
--------------------------

* fixed x509 certificate version
* renamed ``public_key`` field to more appropiate ``certificate``
* show x509 text dump in admin when editing objects

Version 0.1 [2016-07-18]
------------------------

* CA and end entity certificate generation
* import existing certificates
* x509 extensions
* revocation
* CRL
