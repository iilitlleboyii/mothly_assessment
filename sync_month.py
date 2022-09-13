import pandas as pd
import numpy as np
from deepfos.element.datatable import DataTableMySQL
from deepfos.element.dimension import Dimension
from deepfos.lib.sysutils import complete_cartesian_product
import datetime
import uuid

try:
    from _debug import para1, para2
except ImportError:
    para1 = para2 = {}


def main(p1, p2):
    # 获取页面必选信息
    user = p1['user']
    system_time = datetime.datetime.now()
    Year = p2[0]['Year']
    Period = p2[0]['Period']
    if not Year:
        raise Exception("年份为必选项！")
    if not Period:
        raise Exception("期间为必选项！")

    # 从月度考核提交审批记录表查数
    MySQL_Table_month = DataTableMySQL("YDKH_LCJLB")
    t = MySQL_Table_month.table
    df = MySQL_Table_month.select()

    # 查Entity维度信息，获取name和is_active
    dimension1 = Dimension("Entity")
    dim1 = dimension1.query('Base(OrganizationalStructure,0);', fields=['name', 'is_active'])
    Entity_exist_dictlist = []
    Entity_exist_name_list = []
    Entity_notexist_name_list = []

    # 需要同步的维度成员状态必须要为True
    for m in dim1:
        if m.name in df['Entity'].values:
            Entity_exist_dictlist.append({'Entity': m.name, 'Entity_status': str(m.is_active)})
            if str(m.is_active) == 'True':
                Entity_exist_name_list.append(m.name)
        else:
            if str(m.is_active) == 'True':
                Entity_notexist_name_list.append(m.name)
    # 用于生成对应的维度表达式字符串，后面也是类似
    new_Entity_fix = ';'.join(Entity_notexist_name_list)
    old_Entity_fix = ';'.join(Entity_exist_name_list)

    # 查Period维度信息
    dimension2 = Dimension("Period")
    dim2 = dimension2.query('Base(TotalPeriod,0);', fields=['name'])
    Period_name_list = []
    for m in dim2:
        Period_name_list.append(m.name)
    Period_name_list = Period_name_list[Period_name_list.index(Period):]
    Period_fix = ';'.join(Period_name_list)

    # 初始化一个空的df，用于后面补数据
    df_insert = pd.DataFrame(columns=df.columns.values)

    # 查询数据表已存在人员是否存在当前年份的数据，如果没有则增加，如果有则更新旧数据
    df_old_year = df[['Year']].copy()
    df_old_year.drop_duplicates(inplace=True)
    if Year not in df_old_year['Year'].values:
        if old_Entity_fix:
            fix_exist = {'Entity': old_Entity_fix, 'Entity_status': 'True', 'Year': Year, 'Period': Period_fix,
                         'result_status': '1', 'partition_id': '0', 'process_operation_id': '0', 'operate_user': user}
            df_insert_exist = complete_cartesian_product(fix=fix_exist, df=df_insert)
            for index, row in df_insert_exist.iterrows():
                # 这里去掉生成的编码里的'-'是因为平台识别不了，后面也是相同原因
                row['record_id'] = str(uuid.uuid1()).replace('-', '')
            # datatime类型数据非str，不能直接补数据，需要后面自己手动加
            df_insert_exist[['operate_time']] = system_time
            MySQL_Table_month.insert_df(df_insert_exist, chunksize=5000, auto_fit=True)
    else:
        # 初始化一个空df，用于存需要更新的行，以便后续一起更新
        df_update = pd.DataFrame(columns=df.columns.values)
        for d in Entity_exist_dictlist:
            df_test = df[(df['Entity'] == d['Entity']) & (df['Year'] == Year) & (df['Period'] == Period)].copy()
            if df_test['Entity_status'].iloc[0] != d['Entity_status']:
                # df_temp用于临时存储每个实体的有用数据，每次循环结束将数据拼接到df_update
                df_temp = df[(df['Entity'] == d['Entity']) & (df['Year'] == Year)].copy()
                this_index = df_temp[(df_temp['Entity'] == d['Entity']) & (df_temp['Year'] == Year) & (df_temp['Period'] == Period)].index[0]
                # 需要的数据是当前期间及以后的，所以这里借用索引判断之后的数据
                df_temp = df_temp[df_temp.index >= this_index]
                df_temp[['Entity_status']] = d['Entity_status']
                df_update = df_update.append(df_temp)
        df_update[['where']] = ''
        if len(df_update) > 0:
            for index, row in df_update.iterrows():
                df_update.at[index, 'where'] = f"record_id='{row['record_id']}'"
            MySQL_Table_month.update_from_dataframe(df_update)

    # 新增数据表不存在人员的数据
    if new_Entity_fix:
        fix_notexist = {'Entity': new_Entity_fix, 'Entity_status': 'True', 'Year': Year, 'Period': Period_fix, 'result_status': '1', 'partition_id': '0',
                        'process_operation_id': '0', 'operate_user': user}
        df_insert_notexist = complete_cartesian_product(fix=fix_notexist, df=df_insert)
        for index, row in df_insert_notexist.iterrows():
            row['record_id'] = str(uuid.uuid1()).replace('-', '')
        df_insert_notexist[['operate_time']] = system_time
        MySQL_Table_month.insert_df(df_insert_notexist, chunksize=5000, auto_fit=True)


if __name__ == '__main__':
    main(para1, para2)
