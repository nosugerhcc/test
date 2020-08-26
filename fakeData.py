import numpy as np
import pandas as pd
def getData(state):
    reward={'pow_q_length':[-1500,-1231,-961,-646,-312,-45,120,256,456,741]}
    dataFrame=pd.DataFrame(reward,index=['156','146','136','126','116','106','96','86','76','66'])
    reward=dataFrame.loc[state,'pow_q_length']
    return reward

if __name__=='__main__':
    print(getData('56'))