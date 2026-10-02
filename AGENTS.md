# Testing rule changes on a real project

Unit tests are not enough to validate a rule change. Before you consider done
any change to a rule (a new rule, a change to an existing rule, a new fix, or a
change to an existing fix), test it against
[alltheplaces](https://github.com/alltheplaces/alltheplaces):

1. Shallow-clone alltheplaces at commit
   `dd9b5f8da34afb8969cfc48812309b052d886915` into a temporary directory
   outside this repository. Later commits of alltheplaces use scrapy-lint
   themselves, which hides reports.

2. Run `scrapy-lint` in the clone root, once from your branch and once from
   `origin/master`, and diff the two outputs:

   ```bash
   REPO=$PWD WORK=$(mktemp -d)
   git init -q $WORK/atp
   git -C $WORK/atp fetch -q --depth 1 https://github.com/alltheplaces/alltheplaces dd9b5f8da34afb8969cfc48812309b052d886915
   git -C $WORK/atp checkout -q FETCH_HEAD
   git worktree add --detach $WORK/master origin/master
   cd $WORK/atp
   uv run --project $WORK/master scrapy-lint > $WORK/before.txt
   uv run --project $REPO scrapy-lint > $WORK/after.txt
   diff $WORK/before.txt $WORK/after.txt
   git -C $REPO worktree remove $WORK/master
   ```

3. Check every issue that appears or disappears for the rules your change
   touches, and confirm that each one is a real issue, or a real fix of a
   misreport. For a new rule with many reports, classify all of them, e.g.
   with an AST script, and inspect examples of every bucket.

4. For fix changes, run `scrapy-lint --fix` on a copy of the clone, then check
   that the changed files compile, that each edit is equivalent to the
   original code, and that a new `scrapy-lint` run reports no new issues.
   Where possible, also run the alltheplaces tests (`uv run pytest`) and
   `uv run scrapy list` on the fixed copy.

5. Summarize the results in the pull request description: counts per rule
   before and after, and any report you consider debatable, with your reasons.

6. Turn every misreport you find this way into a test case in this
   repository.

Never commit to the alltheplaces clone, and never push anything to
alltheplaces.
