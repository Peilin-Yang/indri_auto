#!/bin/sh

indri_root=''
base_para_fn='index_builder'
corpora_root='/tuna1/collections/newswire/'
output_index_root='/tuna1/scratch/yangpeilyn/Indri/index/'
log_root='/tuna1/scratch/yangpeilyn/Indri/index.logs/'
allowed_corpus=(wt2g disk12)
corpus_types=(trecweb trectext)
mem_use_gb=(2 3)
#para_fns=(disk12 disk45 aquaint wt2g wt10g gov2)
mkdir -p $output_index_root
for k in {1..2} # we run each setting 3 times...
do
    for (( i=0; i<${#allowed_corpus[*]}; i++ ))
    do
        rm -rf $output_index_root$allowed_corpus[$i]
        python indri_index_builder.py \
         --indri_root "$indri_root" \
         --build_para_fn "$base_para_fn"\
         --corpus_type "${corpus_types[$i]}" \
         --mem_gb "${mem_use_gb[$i]}" \
         --corpus_root "$corpora_root${allowed_corpus[$i]}" \
         --index_root "$output_index_root" \
         --log_root $log_root
    done
done
