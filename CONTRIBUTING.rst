Contributing to Respawn
########################

Bug fixes, feature additions, tests, documentation and more can be contributed via [issues](https://github.com/dowjones/respawn/issues) and/or [pull requests](https://github.com/dowjones/respawn/pulls). All contributions are welcome.

Bug fixes, feature additions, etc.
###################################

Please send a pull request to the master branch. Please include [documentation](https://readthedocs.org) and [tests](respawn/test/README.rst) for new features. Tests or documentation without bug fixes or feature additions are welcome
 too. Feel free to ask questions [via issues](https://github.com/dowjones/respawn/issues/new) or irc://irc.freenode
 .net#respawn

- Fork the respawn repository.
- Create a branch from master.
- Develop bug fixes, features, tests, etc.
- Run the test suite on both Python 2.7. You can enable [Travis CI on your repo](https://travis-ci.org/profile/) to catch test failures prior to the pull request, and [Coveralls](https://coveralls.io/repos/new) to see if the changed code is covered by tests.
- Create a pull request to pull the changes from your branch to the respawn master.

Guidelines
###########

- Separate code commits from reformatting commits.
- Provide tests for any newly added code.
- Follow PEP8.
- When committing only documentation changes please include [ci skip] in the commit message to avoid running tests on Travis-CI.

Reporting Issues
#################

When reporting issues, please include code that reproduces the issue and whenever possible, an image that demonstrates the issue. The best reproductions are self-contained scripts with minimal dependencies.

Provide details
################

- What did you do?
- What did you expect to happen?
- What actually happened?
- What versions of respawn and Python are you using?
