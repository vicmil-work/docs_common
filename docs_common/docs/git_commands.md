# Usefull git commands

### Create a new branch locally

```
git checkout -b my_new_branch
```

### Create a new branch locally without any commit history

```
git checkout --orphan my_new_branch
```

### Create a new branch locally with commit history

`git checkout -b my_new_branch`

### Push a local branch to upstream if upstream branch does not exist

```
git push --set-upstream origin my_new_branch
```

### Overwrite history of remote repo with local repo

```
git push origin my_new_branch --force
```

### Undo last commit(only affecting git history, all files remain the same)

```bash
git reset HEAD~1
```

### Delete branch

```
git branch -D master
```

### Generate a new ssh key

```
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### Push local code to new branch in remote repo

Create git repo

```
git init
```

Create a new branch that you would like to push

```
git checkout -b my_new_branch
```

Set the repo to be connected to the remote repo you would like to push to

```
git remote add origin https://github.com/my_git_repo_to_use
```

Add a commit
```
git add -A
git commit -m "add initial code"
```

Push the code to the remote repo and create a new remote branch

```
git push -u origin my_new_branch
```

### Unstage files for commit

```
git restore --staged <file>
```

### Mark file as deleted that was previously tracked(does not change the local file, only the commit)

```
git update-index --remove <file>
```

### Pull down all submodules in repo
(downloads the dependencies as it was when it was pushed)
```
git submodule update --init --recursive
```
