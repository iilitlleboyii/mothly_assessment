import pandas as pd
import numpy as np
from deepfos.element.datatable import DataTableMySQL
from deepfos.element.finmodel import FinancialCube
from deepfos.element.rolestrategy import RoleStrategy
from deepfos.api.space import SpaceAPI
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
        SAPI = SpaceAPI(header=p1, sync=True)
        UserInfo = SAPI.user.query(userId=user)
        userName = UserInfo.userName
        nickName = UserInfo.nickName

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
        t = MySQL_Table_month.table

        MySQL_Table_financialcube = DataTableMySQL("Fin_Cube_2")

        where = (t.Entity == Entity) & (t.Period == Period) & (t.Year == Year)
        df = MySQL_Table_month.select(['result_status'], where=where)
        if df['result_status'].iloc[0] == '1':
            MySQL_Table_month.update({'result_status': '2', 'operate_user':user, 'operate_time':system_time}, where=where)
            MySQL_Table_financialcube.insert({'Year': Year, 'Period': Period, 'Entity': Entity, 'By1': By1_user, 'By2': By2_user, 'Detail': Detail_user, 'Misc': Misc_user, 'string_val': nickName if nickName else userName})
            MySQL_Table_financialcube.insert({'Year': Year, 'Period': Period, 'Entity': Entity, 'By1': By1_time, 'By2': By2_time, 'Detail': Detail_time, 'Misc': Misc_time, 'string_val': str(system_time)})
            Cube_finance.pc_update(process_map=process_map, data_block_map=data_block_map, status='2')
        else:
            raise Exception("当前页面已提交，请勿重复提交！")
    else:
        raise Exception("暂无编辑权限，禁用提交操作！")


if __name__ == '__main__':
    main(para1, para2)
