#!/usr/bin/env bash
export DAY=$(date "+%-d")

EXERCISE=$(curl -s -b $(cat cookies.txt) "https://adventofcode.com/2020/day/$DAY" | sed -n '/^<main>/,/^<\/main>/p;/^<\/main>/q' | html2text -nobs -width 75)

export EXERCISE_COMMENT=$EXERCISE

FILE="src/day${DAY}.rs"
if test -f $FILE; then
    echo "$FILE exists already."
    BACKUP="src/day${DAY}_from_template.rs.bak"
    cat ./template.rs.tpls  | envsubst '${EXERCISE_COMMENT},${DAY}' > $BACKUP
    echo "Wrote to $BACKUP."
    exit 0
fi

cat ./template.rs.tpls  | envsubst '${EXERCISE_COMMENT},${DAY}' > $FILE

echo "Wrote to $FILE."
