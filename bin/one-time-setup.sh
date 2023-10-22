#!/bin/sh
set -e
PROJECT_NAME="Entanglment_visualizer"

PACKAGE_PATH=$(dirname "$(pwd)")

WS_PATH="/opt/$PROJECT_NAME"

echo "Your project path is $PACKAGE_PATH"
echo "Start setup"

echo "git commit template setup"
git config --local commit.template $PACKAGE_PATH/template.tmpl

echo "Project setup"
export_we="export QENVWS=$PACKAGE_PATH"
export_path="export PATH=$PATH:$PACKAGE_PATH/bin"

if [ "$SHELL" = "/bin/bash" ]; then
    echo "Running in Bash"
	last_line=$(tail -n 1 ~/.bashrc)
	if [ "$last_line" != "$export_path"  ]; then
		echo "register workspace && bin path"
		echo "$export_we" >> ~/.bashrc
		echo "$export_path" >> ~/.bashrc
	else
		echo "Already registered bin path"
	fi

elif [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ] ; then
    echo "Running in Zsh"
    last_line=$(tail -n 1 ~/.zshrc)
	if [ "$last_line" != "$export_path"  ]; then
		echo "register workspace && bin path"
		echo "$export_we" >> ~/.zshrc
		echo "$export_path" >> ~/.zshrc
	else
		echo "Already registered bin path"
	fi
else
    echo "Running in a different shell (not Bash or Zsh)"
    echo "Only support in zsh or bash sorry."
fi
