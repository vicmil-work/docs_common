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

`git checkout --b my_new_branch`

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
