
import unittest

import testutils
import sqlservertests

# TODO review
usage = """\
usage: %prog [options] connection_string

Unit tests for Actian Ingres, ActianX, Vector.  To use, pass a connection string as the parameter.
The tests will create and drop tables t1 and t2 as necessary.

These run using the version from the 'build' directory, not the version
installed into the Python directories.  You must run python setup.py build
before running the tests.

Easiest way to run is to specify connection string on command line, e.g.:

    ingres_tests.py "DRIVER={Ingres XT};SERVER=(local);DATABASE=db"

NOTE below not tested
You can also put the connection string into a setup.cfg file in the root of the project
(the same one setup.py would use) like so:

  [ingres_tests]
  connection-string=DRIVER={Ingres};SERVER=(local);DATABASE=db

The connection string above will use the default driver. Additional samples:

  connection-string=DRIVER={Ingres CR};SERVER=(local);DATABASE=db;UID=uid;PWD=pwd
  connection-string=DRIVER={Ingres XT};SERVER=(local);DATABASE=db;UID=uid;PWD=pwd
  connection-string=DRIVER={Ingres XT};SERVER=(local);DATABASE=demodb
"""

class IngresTestCase(sqlservertests.SqlServerTestCase):
    pass
    # todo override version func

# ingres_tests.py -v "DRIVER={Ingres XT};SERVER=(local);DATABASE=db"
def main():
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="count", help="Increment test verbosity (can be used multiple times)")
    parser.add_option("-d", "--debug", action="store_true", default=False, help="Print debugging items")
    parser.add_option("-t", "--test", help="Run only the named test")

    (options, args) = parser.parse_args()

    if len(args) > 1:
        parser.error('Only one argument is allowed.  Do you need quotes around the connection string?')

    if not args:
        connection_string = testutils.load_setup_connection_string('ingres_tests')  # TODO review/test

        if not connection_string:
            parser.print_help()
            raise SystemExit()
    else:
        connection_string = args[0]

    cnxn = pypyodbc.connect(connection_string)
    c = cnxn.cursor()
    c.execute("select dbmsinfo('_version')")
    print(c.fetchone())
    c.close()
    testutils.print_library_info(cnxn)
    cnxn.close()

    suite = testutils.load_tests(IngresTestCase, options.test, connection_string)
    print (suite)
    testRunner = unittest.TextTestRunner(verbosity=options.verbose)
    result = testRunner.run(suite)


if __name__ == '__main__':

    # Add the build directory to the path so we're testing the latest build, not the installed version.

    testutils.add_to_path()

    import pypyodbc
    main()
