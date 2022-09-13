from deepfos.element.datatable import DataTableMySQL
import datetime
import pandas as pd
import numpy as np

try:
    from _debug import para1, para2
except ImportError:
    para1 = para2 = {}


def main(p1, p2):
    user = p1['user']
    system_time = datetime.datetime.now()
    MySQL_Table_month = DataTableMySQL("YDKH_LCJLB")
    t = MySQL_Table_month.table
    df = pd.DataFrame(columns=['record_id', 'result_status'])
    for row in p2:
        df_temp = MySQL_Table_month.select(['record_id', 'result_status'], where=(t.record_id == row['record_id']) & (t.result_status == '2'))
        df = df.append(df_temp, ignore_index=True)
    df['result_status'], df['operate_user'], df['operate_time'] = ['3', user, system_time]
    for index, row in df.iterrows():
        MySQL_Table_month.update({'result_status':row['result_status'], 'operate_user':row['operate_user'], 'operate_time':row['operate_time']}, where=t.record_id==row['record_id'])


if __name__ == '__main__':
    main(para1, para2)
