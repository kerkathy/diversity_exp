# same as reproduce.sh but add --similarity_threshold for each command
# usage for retrieval only: bash similarity_exp.sh oner none hotpotqa
# usage for retrieval + qa: bash similarity_exp.sh oner_qa flan-t5-base hotpotqa
# This runs similarity experiment for threshold [80, 70, 60, 50, 40, 99 95 85 35 30 25 20]

threshold=(99)
for i in ${threshold[*]}
do
echo "$i"
done

#!/usr/bin/env bash

# Expected command line argument values.
valid_systems=("ircot" "ircot_qa" "oner" "oner_qa" "nor_qa")
valid_models=("codex" "flan-t5-xxl" "flan-t5-xl" "flan-t5-large" "flan-t5-base" "none")
valid_datasets=("hotpotqa" "2wikimultihopqa" "musique" "iirc")

# Function to check if an argument is valid
check_argument() {
    local arg="$1"
    local position="$2"
    local valid_values=("${!3}")
    local system="$4"

    if ! [[ " ${valid_values[*]} " =~ " $arg " ]]; then
        echo "argument number $position is not a valid. Please provide one of: ${valid_values[*]}"
        echo "but now the argument is $arg"
        exit 1
    fi

    # if [[ $position -eq 2 && $arg == "none" && $1 != "oner" ]]; then
    if [[ $position -eq 2 && $arg == "none" && $system != "oner" ]]; then
        echo "The model argument can only be 'none' only if the system argument is 'oner'."
        echo "but now the system argument is $1"
        exit 1
    fi
}

# Check the number of arguments
if [[ $# -ne 3 ]]; then
    echo "Error: Invalid number of arguments. Expected format: ./similarity.sh SYSTEM MODEL DATASET"
    exit 1
fi

# Check the validity of arguments
check_argument "$1" 1 valid_systems[*]
check_argument "$2" 2 valid_models[*] $1
check_argument "$3" 3 valid_datasets[*]

# run similarity threshold
for i in ${threshold[*]}
do
    echo ">>>> Instantiate experiment configs with different HPs and write them in files. <<<<"
    python runner.py $1 $2 $3 write --prompt_set 1 --similarity_threshold $i
    python runner.py $1 $2 $3 write --prompt_set 2 --similarity_threshold $i
    python runner.py $1 $2 $3 write --prompt_set 3 --similarity_threshold $i
    # if you make a change to base_configs, the above steps need to be rerun to
    # regenerate instantiated experiment configs (with HPs populated)

    echo ">>>> Run experiments for different HPs on the dev set. <<<<"
    python runner.py $1 $2 $3 predict --prompt_set 1 --similarity_threshold $i
    ## If prediction files already exist, it won't redo them. Pass --force if you want to redo.

    # echo ">>>> Run evaluation for different HPs on the dev set. <<<<"
    # python runner.py $1 $2 $3 evaluate --prompt_set 1 --similarity_threshold $i
    # ## This runs by default after prediction. This is mainly to show a standalone option.

    # echo ">>>> Show results for experiments with different HPs <<<<"
    # python runner.py $1 $2 $3 summarize --prompt_set 1 --similarity_threshold $i
    # ## Not necessary as such, it'll just show you the results using different HPs in a nice table.

    # echo ">>>> Pick the best HP and save the config with that HP. <<<<"
    # python runner.py $1 $2 $3 write --prompt_set 1 --best --similarity_threshold $i
    # python runner.py $1 $2 $3 write --prompt_set 2 --best --similarity_threshold $i
    # python runner.py $1 $2 $3 write --prompt_set 3 --best --similarity_threshold $i

    # echo ">>>> Run the experiment with best HP on the test set <<<<"
    # python runner.py $1 $2 $3 predict --prompt_set 1 --best --eval_test --official --similarity_threshold $i
    # python runner.py $1 $2 $3 predict --prompt_set 2 --best --eval_test --official --similarity_threshold $i
    # python runner.py $1 $2 $3 predict --prompt_set 3 --best --eval_test --official --similarity_threshold $i
    # ## If prediction files already exist, it won't redo them. Pass --force if you want to redo.

    # echo ">>>> Run evaluation for the best HP on the test set <<<<"
    # python runner.py $1 $2 $3 evaluate --prompt_set 1 --best --eval_test --official --similarity_threshold $i
    # python runner.py $1 $2 $3 evaluate --prompt_set 2 --best --eval_test --official --similarity_threshold $i
    # python runner.py $1 $2 $3 evaluate --prompt_set 3 --best --eval_test --official --similarity_threshold $i
    # ## This runs by default after prediction. This is mainly to show a standalone option.

    # echo ">>>> Summarize best test results for individual prompts and aggregate (mean +- std) of them) <<<<"
    # python runner.py $1 $2 $3 summarize --prompt_set 1 --best --eval_test --official --similarity_threshold $i
    # python runner.py $1 $2 $3 summarize --prompt_set 2 --best --eval_test --official --similarity_threshold $i
    # python runner.py $1 $2 $3 summarize --prompt_set 3 --best --eval_test --official --similarity_threshold $i
    # python runner.py $1 $2 $3 summarize --prompt_set aggregate --best --eval_test --official --similarity_threshold $i
    # # The mean and std in the final command is what we reported in the paper.
done