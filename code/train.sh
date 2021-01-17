echo "training base model"
python -u RoBERTa_MRC_sw.py train gpu-1,2 base &> base.log

echo "training label_sm model"
python -u RoBERTa_MRC_ls.py train gpu-1,2 label_sm &> label_sm.log

echo "training weighted_ls model"
python -u RoBERTa_MRC_wl.py train gpu-1,2 weighted_ls &> weighted_ls.log

