Release Notes
-------------

**1.6.0 (2024-09-27)**

* Use the official release of PyFxA 0.7.9 instead of a forked release.

**1.5.2 (2024-09-25)**

* Add maintainer and project URL.

**1.5.1 (2024-09-25)**

* Bump PyFxA (now pyfxa-mte) package so that we can remove the test account during test teardown.

**1.4.0 (2018-08-28)**

* Match session when verifying account and cleanup when verification fails.

**1.3.0 (2018-06-26)**

* Allow environment(s) to be specified using a custom ``fxa_env`` marker.

**1.2.0 (2018-06-15)**

* Catch the exception in teardown when the account has already been destroyed.

**1.1.0 (2018-05-21)**

* Provide a ``fxa_email`` fixture for accessing the email address.

* Allow users to specify the email address by passing ``--fxa-email`` command
line option or setting the ``FXA_EMAIL`` environment variable.

**1.0.0 (2018-04-12)**

* Initial release
