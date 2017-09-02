#!/bin/sh

indri_root=''
base_para_fn='index_builder'
corpora_root='add/your/corpora/root/here'
output_index_root='/add/your/output/root/here'
log_root='/add/your/logs/root/here'
allowed_corpus=(gov2 cw09)
corpus_types=(trecweb warc)
mem_use_gb=(300 500)
#para_fns=(disk12 disk45 aquaint wt2g wt10g gov2 cw09)
#corpus_types=(trectext trectext trectext trecweb trecweb trecweb warc)
#mem_use_gb=(4 4 8 4 20 300 500)
for k in {1..2} # we run each setting 3 times...
do
    for (( i=0; i<${#allowed_corpus[*]}; i++ ))
    do
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
