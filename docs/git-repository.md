# Git repository

For developers have write access to this repository:

1. Clone this GitHub repository to your local machine and change into the local repo
	```shell
	git clone git@github.com:geometalab/osmaxx.git osmaxx && cd osmaxx
	```
	You can specify the name of the remote origin by adding param -o. Example: `-o 'gitHub'`

2. Enable [git-flow](https://github.com/nvie/gitflow) for the local repo
	```shell
	git checkout master # or git checkout -b master origin/master
	git flow init -d
	```

	(This project uses git-flow's default branch names and branch name prefixes, which `-d` automatically accepts.)

	You should now be on the `develop` branch. Otherwise checkout the development branch: `git checkout development`.
3. Clone the third party repositories we use through [git submodules](http://www.git-scm.com/book/en/v2/Git-Tools-Submodules)

	```shell
	git submodule init && git submodule update
	```


## Contribute

1. Create a feature branch for your contribution
	```shell
	git flow feature start 'my-awesome-feature#gitHubIssueNumber'
	```

2. Code and commit as usual
3. Run flake8, checks and tests
	```shell
	./test.sh
	```

3. Once you're finished, push the feature branch back to this GitHub repo
	```shell
	git flow feature publish
	```

	(Do **not** use `git flow feature finish`, as we use pull requests for review purposes.)

4. Create a pull request against branch `develop`. Link the issue, inform the reviewers about the checks you did and add review tasks as subtasks (see below), e.g:
	```markdown
	Implementation of feature #123 (Merge will close #123 ).

	* locales **NOT** compiled -> do this on release (prevent huge locale diffs in changes)
	* ran flake8
	* ran check
	* ran test
	* tested views by hand:
	  * /orders/new [get/post]
	  * /orders/{id}

	To be reviewed by:
	- [ ] @some-developer
	- [ ] @another-developer
	```


## Release

### Create release branch (example)
```shell
git flow release start '1.4.0'
```


### Todo on release

* Compile locales
* Run all tests
* Test development and production containers
* Update documentation
	* Readme
	* Wiki


### Finish release

```shell
git flow release finish '1.4.0'

git checkout develop
git push github develop --tags

git checkout master
git push github develop --tags

git checkout develop
```

Go to Github repository /releases and add description of the release.