#!/bin/bash


generate_confusion_string() {
  local size=$1
  cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w "$size" | head -n 1
}


if [ "$#" -lt 4 ]; then
    echo "Use: $0 <confusion_strings_count> <num_iterations_values> <python_script> <n>"
    exit 1
fi

confusion_strings_count=$1
num_iterations_values=$2
python_script=$3
n=$4


confusion_strings=()
for size in $(seq 1 $confusion_strings_count); do
  for _ in $(seq 1 $n); do
    confusion_strings+=("$(generate_confusion_string "$size")")
  done
done


echo "Confusion Strings: ${confusion_strings[@]}"


python3 "$python_script" "${confusion_strings[@]}" "$num_iterations_values" "$n"
