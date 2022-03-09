cd $PWD/static_code_analysis/repo
git clone --depth 1 --branch $2 $1

directory=$(echo $1 | sed 's%^.*/\([^/]*\)\.git$%\1%g')

cd $directory
echo 'Open' $directory 'repository'

if [ $3 = "INFO" ]; then
    docker run --rm -v "${PWD}:/src" returntocorp/semgrep --config=auto --metrics=on --no-autofix -o result.json --json --severity=INFO
elif [ $3 = "WARNING" ]; then
    docker run --rm -v "${PWD}:/src" returntocorp/semgrep --config=auto --metrics=on --no-autofix -o result.json --json --severity=WARNING
elif [ $3 = "ERROR" ]; then
    docker run --rm -v "${PWD}:/src" returntocorp/semgrep --config=auto --metrics=on --no-autofix -o result.json --json --severity=ERROR
else
    docker run --rm -v "${PWD}:/src" returntocorp/semgrep --config=auto --metrics=on --no-autofix -o result.json --json
fi

cp result.json ../../result.json

cd ..

rm -rf $directory
