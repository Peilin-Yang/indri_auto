#!/bin/sh

anserini_root='/anserini/repo/root/'
index_root='/output/index/root/'
log_root='/logs/root/'
corpora_root='/corpora/root/'
corpora=(disk12 disk45 AQUAINT wt2g gov2)
ctypes=(Trec Trec Trec Wt Gov2)
for c in {1..3} 
do
    if [ $c -eq 1 ]; then
       cond=""
    elif [ $c -eq 2 ]; then
       cond="--pos"
    elif [ $c -eq 3 ]; then
       cond="--pos --docvec --raw"
    fi
    for m in 0 1
    do
        if [ $m -eq 0 ]; then
           merge=""
        else
           merge="--merge"
        fi
        for t in 44 
        do
            for k in {1..2} # we run each setting 2 times...
            do
                for (( i=0; i<${#corpora[*]}; i++ ))
                do
                    python anserini_index_builder.py \
                     --anserini_root "$anserini_root" \
                     --corpus_root "$corpora_root/${corpora[$i]}" \
                     --ctype ${ctypes[$i]} \
                     --output_root $index_root \
                     --threads $t $cond $merge \
                     --log_root $log_root
                done
            done
        done
    done
done
