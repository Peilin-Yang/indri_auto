# Indexing
1. Download the latest version of Indri from: https://sourceforge.net/projects/lemur/files/lemur/ 
  * `./configure --prefix=/your/own/path/`
  * `make`
  * `make install`

2. `git clone https://github.com/Peilin-Yang/indri_auto.git`

3. Modify whatever applies to you in `build_indri_index_all.sh`. Specifically,
  * `corpora_root`: the path(folder) of the collections
  * `output_index_root`: where to put the index
  * `log_root`: where to put the logs
  * `allowed_corpus`: names of the corpora folde that will be indexed. the rest of the folders will be ignored.
  * `corpus_types`: the corresponding corpus types for `allowed_corpus`.
  * `mem_use_gb`: the memory will be allocated for those corpora.
  
  

