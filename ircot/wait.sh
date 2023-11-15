# wait until a process with pid XXX is finished
# now, XXX is 3350476
# then `./reproduce.sh ircot flan-t5-large hotpotqa`
# poll every 10 minutes, print the timing information

# ps ax | grep <some_process_name>
# Usage: bash wait.sh 3350476
# currently running threshold = 0.95

# TO-DO:
# modify ircot.py 
# ./reproduce.sh oner flan-t5-large hotpotqa

while true; do
    if [ -d "/proc/$1" ]; then
        date
        sleep 600
    else
        # mkdir predictions_saved/sim_0.95 &&
        # mv predictions/ircot_flan* predictions_saved/sim_0.95 &&
        source ~/.bashrc &&
        conda activate ircot &&
        echo "In conda environment: $CONDA_DEFAULT_ENV"
        ./similarity_exp.sh oner flan-t5-base hotpotqa 90
        break
    fi
done
