#!/work/chem-xuhb/apps/deepmd-kit/bin/python
#origin code: /share/home/chem-lij/xuhb/apps/deepmd-kit/lib/python3.9/site-packages/dpdata/system.py
import dpdata
import numpy as np

# 加载 cp2k/md 格式数据
#多轨迹合并
#data = dpdata.LabeledSystem('./cp2k_md', cp2k_output_name='cp2k.log',fmt='cp2k/aimd_output')
#fmt='cp2kdata/md' is so slow
#date1=dpdata.LabeledSystem(...,restart=True)

#data.to_deepmd_raw('./test')
#cp xyzf2raw.py 
#data = dpdata.LabeledSystem('./',fmt='deepmd/raw') 
#单个轨迹
#data = dpdata.LabeledSystem('./cp2k_md', cp2k_output_name='cp2k.log',fmt='cp2k/aimd_output')

# 随机选择20%个索引，用于生成验证集;其他的索引，用于生成训练集
frame_all = len( data )
frame_val = int( 0.2 * len(data) )
frame_tra = frame_all - frame_val
index_validation = np.random.choice(frame_all,size=frame_val,replace=False)
index_training = list(set(range(frame_all))-set(index_validation))

# 创建子数据集：训练集,测试集
data_training = data.sub_system(index_training)
data_validation = data.sub_system(index_validation)

# 导出训练集,测试集（deepmd/npy格式）
data_training.to_deepmd_npy('./training_data')
data_validation.to_deepmd_npy('./validation_data')

print('# 数据包含 %d frames' % len(data))
print('# 训练数据包含 %d frames' % len(data_training))
print('# 验证数据包含 %d frames' % len(data_validation))
