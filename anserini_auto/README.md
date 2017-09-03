### Indexing
1. `git clone https://github.com/Peilin-Yang/indri_auto.git`

2. `cd indri_auto/anserini_auto`

3. Uncomment the following variables and modify them in `build_anserini_index_all.sh`. Specifically,
  * `anserini_root`: the Anserini repo root, this is for locating the `IndexCollection` binary
  * `corpora_root`: the path(folder) of the collections
  * `index_root`: where to put the index
  * `log_root`: where to put the logs
  * `corpora`: names of the corpora folder that will be indexed. the rest of the folders(collections) will not be indexed.
  * `ctypes`: the corresponding corpus types for `allowed_corpus`. must be one of (`Trec`, `Wt`, `Gov2`, `CW09`, `CW12`)
  
  *also look at the `cond`, `merge`, `t` (for threads), `k` (iterations) for whatever applies*

4. `nohup bash build_indri_index_all.sh &`

### Print Indexing Efficiency Results
`python anserini_efficiency_cal.py --log_root /the/log/folder/of/the/indexing/ --type index`
