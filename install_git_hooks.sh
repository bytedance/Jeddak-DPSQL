# Force using a uniform pre-commit file
cat << EOF > .git/hooks/pre-commit
#!/bin/sh
make lint&&make fast_test
EOF
  chmod u+x ./.git/hooks/pre-commit

cat << EOF > .git/hooks/pre-push
#!/bin/sh
make test
EOF
  chmod u+x ./.git/hooks/pre-push
