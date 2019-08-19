import numpy as np
import pandas as pd
import time
import random
import os
from multiprocessing import Pool

df = pd.read_csv('./data/fixed_data.csv', dtype='str', index_col=False)
del df['Unnamed: 0']
list_ho = df['HO'].tolist()
list_dem = df['DEM'].tolist()
list_ten = df['TEN'].tolist()


def get_random_data(i):
    global list_ho
    global list_dem
    global list_ten
    ho = np.random.choice(list_ho)
    dem = np.random.choice(list_dem)
    ten = np.random.choice(list_ten)
    ngay = np.random.randint(1, 32)
    thang = np.random.randint(1, 13)
    nam = np.random.randint(1901, 2019)
    sex = np.random.randint(0, 2)
    tinhKS = '{:02d}TTT'.format(np.random.randint(1, 65))
    huyenKS = '{:003d}HH'.format(np.random.randint(0, 260))
    xaKS = '{:00005d}'.format(np.random.randint(0, 20000))
    if int(str(nam)[:2])+1 == 21 and sex == 0:
        soCMTND = tinhKS[:2]+'1'
    elif int(str(nam)[:2])+1 == 21 and sex == 1:
        soCMTND = tinhKS[:2]+'0'
    elif int(str(nam)[:2])+1 == 20 and sex == 0:
        soCMTND = tinhKS[:2]+'3'
    elif int(str(nam)[:2])+1 == 20 and sex == 1:
        soCMTND = tinhKS[:2]+'2'
    soCMTND += str(nam)[-2:]+'{:000006d}'.format(np.random.randint(0, 1000000))
    new_row = [sex, tinhKS, huyenKS, xaKS,
               soCMTND, ho, dem, ten, ngay, thang, nam]
    return new_row


def main():
    global df
    start = time.time()
    print(time.strftime('%X %x'))
    i = 0
    while i < 10000000:
        pool = Pool(processes=6)
        results = pool.map(get_random_data, [j for j in range(100000)])
        i += 100000
        pool.close()
        df_result = pd.DataFrame(results, columns=[
                                 'GIOI_TINH', 'MA_TINH_KS', 'MA_HUYEN_KS', 'MA_XA_KS', 'SO_CMTND', 'HO', 'DEM', 'TEN', 'NGAY', 'THANG', 'NAM'])
        if not os.path.isfile('./data/new_record2.csv'):
            df_result.to_csv('./data/new_record2.csv')
        else:
            df_result.to_csv('./data/new_record2.csv', mode='a',
                             header=False, index_label=False)
        # print ('Join data')
        # joined_df = pd.concat([df,df_result],ignore_index=True,sort=False)
    print(time.time()-start)
    print(time.strftime('%X %x'))


if __name__ == '__main__':
    main()
