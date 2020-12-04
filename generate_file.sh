#!/usr/bin/env bash
export DAY=$(date "+%-d")

EXERCISE=$(curl -s -b $(cat cookies.txt) "https://adventofcode.com/2020/day/$DAY" | sed -n '/^<main>/,/^<\/main>/p;/^<\/main>/q' | html2text -nobs -width 75)

export EXERCISE_COMMENT=$EXERCISE

FILE="src/day${DAY}.rs"
if test -f $FILE; then
    echo "Already exists $FILE"
else
    cat ./template.rs.tpls  | envsubst '${EXERCISE_COMMENT},${DAY}' > $FILE
    echo "Wrote to $FILE2"
fi

FILE2="py/day${DAY}.py"
if test -f $FILE2; then
    echo "Already exists $FILE2"
else
    echo "Wrote to $FILE2"
    cat ./template.py.tpls  | envsubst '${EXERCISE_COMMENT},${DAY}' > $FILE2
fi
