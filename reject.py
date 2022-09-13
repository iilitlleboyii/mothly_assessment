import pandas as pd
import numpy as np
from deepfos.element.datatable import DataTableMySQL
from deepfos.element.finmodel import FinancialCube
from deepfos.element.rolestrategy import RoleStrategy
import datetime

try:
    from _debug import para1, para2
except ImportError:
    para1 = para2 = {}


def main(p1, p2):
    user = p1['user']
    Entity = p2['Entity']

    rs = RoleStrategy("YDKH_QXFA", folder_id='YDKH_QXFA', path='/Application/PermissionScheme/YDKH_QXFA')
    r_001 = rs.query(user=user, role='001')
    r_r_001 = r_001.records
    r_002 = rs.query(user=user, role='002')
    r_r_002 = r_002.records
    dim_expression = r_r_002[0].dim_expr[0]
    if r_r_001 and dim_expression != Entity:
        Year = p2['Year']
        Period = p2['Period']

        system_time = datetime.datetime.now()

        By1_user = 'Noby1'
        By2_user = 'Noby2'
        Detail_user = 'MA06'
        Misc_user = 'M03'

        By1_time = 'Noby1'
        By2_time = 'Noby2'
        Detail_time = 'MA07'
        Misc_time = 'M03'

        Cube_finance = FinancialCube("Fin_Cube_2")
        process_map = {'Year': f'Year{{{Year}}}', 'Period': f'Period{{{Period}}}'}
        data_block_map = {'Entity': f'Entity{{{Entity}}}'}

        MySQL_Table_month = DataTableMySQL("YDKH_LCJLB")
        t1 = MySQL_Table_month.table

        MySQL_Table_financialcube = DataTableMySQL("Fin_Cube_2")
        t2 = MySQL_Table_financialcube.table

        where1 = (t1.Entity == Entity) & (t1.Period == Period) & (t1.Year == Year)
        where2 = (t2.Entity == Entity) & (t2.Period == Period) & (t2.Year == Year) & (t2.By1 == By1_user) & (t2.By2 == By2_user) & (t2.Detail == Detail_user) & (t2.Misc == Misc_user)
        where3 = (t2.Entity == Entity) & (t2.Period == Period) & (t2.Year == Year) & (t2.By1 == By1_time) & (t2.By2 == By2_time) & (t2.Detail == Detail_time) & (t2.Misc == Misc_time)
        df = MySQL_Table_month.select(['result_status'], where=where1)
        origin_status = df['result_status'].iloc[0]
        if origin_status == '2':
            MySQL_Table_month.update({'result_status': '1', 'operate_user': user, 'operate_time': system_time}, where=where1)
            MySQL_Table_financialcube.delete(where=where2)
            MySQL_Table_financialcube.delete(where=where3)
            Cube_finance.pc_update(process_map=process_map, data_block_map=data_block_map, status='1')
        elif origin_status == '1':
            raise Exception("表单尚未提交，请提交表单！")
        elif origin_status == '3':
            raise Exception("表单数据已锁定，请勿修改！")
    else:
        raise Exception("暂无编辑权限，禁用撤回操作！")


if __name__ == '__main__':
    main(para1, para2)
