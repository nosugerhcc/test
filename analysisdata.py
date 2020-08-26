import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import get_csv_file

file_lists= get_csv_file.get_csv_file(".",".csv")

index=[]
q_length_list=[]

for file_path in file_lists:
    path_relative=os.path.split(file_path)[1]
    path_relative_send_rate=path_relative[8:-4]
    index.append(path_relative_send_rate)
    df=pd.read_csv(file_path,sep=' ',names=['swid2','length2', 'timedelta2', 'swid3','length3',
                                            'timedelta3','swid1','length1', 'timedelta1','load'])
    df_have_q_length=df[df['length3']!=0]
    if df_have_q_length.shape[0]==0:
        q_length_list.append(0)
        continue
    x=0
    for i in range(df_have_q_length.shape[0]):
         x+=pow(df_have_q_length.iloc[i,4],2)
    x/=df_have_q_length.shape[0]
    q_length_list.append(x)

d={'q_length':q_length_list}

dataFrame1=pd.DataFrame(d,index=index)
print(dataFrame1)

# x=np.arange(0,18)
# y=np.linspace(100,100,18)
# a=np.arange(0,18)
# b=np.linspace(60,60,18)
# plt.plot(x,y,label="Idealization")
# plt.plot(a,b,label="static strategy")
# plt.plot(list_utilization_q_learning,'-',label="q-learning")
# plt.yticks(range(50,130,10))
#
# plt.xlabel("time")
# plt.ylabel("link_utilization")
# plt.title("q_learning vs static strategy")
# plt.legend()
#
# plt.show()
# #
#

