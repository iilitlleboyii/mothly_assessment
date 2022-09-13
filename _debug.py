from deepfos.options import OPTION

# -----------------------------------------------------------------------------
# 从系统中获取以下参数
#: 环境参数
# para1 = {'app': 'xkffcv001', 'space': 'xkffcv', 'user': 'ab7e4870-6fa2-4507-aa4b-bda02099c676', 'language': 'zh-cn',
#          'token': 'E0C8D31E8C788544457C1916ED3108EB417290795A6678A446EBB438B6BFBA69',
#          'cookie': 'alpha_deepfos_users=%7B%22color%22%3A%224%22%2C%22email%22%3A%22xianhao.yu%40deepfinance.com%22%2C%22invitationActivation%22%3Atrue%2C%22mobilePhone%22%3A%2217671003464%22%2C%22nickName%22%3A%22%E4%BD%99%E5%85%88%E6%B5%A9%22%2C%22nickname%22%3A%22%E4%BD%99%E5%85%88%E6%B5%A9%22%2C%22token%22%3A%22E0C8D31E8C788544457C1916ED3108EB417290795A6678A446EBB438B6BFBA69%22%2C%22tokenKey%22%3A%22alpha_deepfos_token%22%2C%22type%22%3A1%2C%22userId%22%3A%22ab7e4870-6fa2-4507-aa4b-bda02099c676%22%2C%22username%22%3A%22Axian%22%7D; alpha_deepfos_token=E0C8D31E8C788544457C1916ED3108EB417290795A6678A446EBB438B6BFBA69',
#          'envUrl': 'http://web-gateway'}
para1 = {'app': 'xkffcv001', 'space': 'xkffcv', 'user': '185f66d3-083d-4c9b-b653-fe3fa505c26a', 'language': 'zh-cn', 'token': 'E9FF4FF9F0EEFD65597745707CD1CFCB470D04EDF57F6AB8F2F901139AEF0CC0', 'cookie': 'cloud_deepfos_users=%7B%22color%22%3A%226%22%2C%22email%22%3A%22weiqi.jiang%40deepfinance.com%22%2C%22invitationActivation%22%3Atrue%2C%22nickName%22%3A%22%E8%92%8B%E7%8E%AE%E7%90%A6%22%2C%22nickname%22%3A%22%E8%92%8B%E7%8E%AE%E7%90%A6%22%2C%22token%22%3A%22F3B6A329328574D2215DE52549AE7BAF5ED7C35441B4E9FE1BB27C723EB6F06C%22%2C%22tokenKey%22%3A%22cloud_deepfos_token%22%2C%22type%22%3A1%2C%22userId%22%3A%222f9337a9-f288-40e4-aef6-fcf11689a2db%22%2C%22username%22%3A%22JWQ%22%7D; cloud_deepfos_token=F3B6A329328574D2215DE52549AE7BAF5ED7C35441B4E9FE1BB27C723EB6F06C; alpha_deepfos_users=%7B%22color%22%3A%224%22%2C%22email%22%3A%22haiyan.zhang%40proinnova.com.cn%22%2C%22invitationActivation%22%3Atrue%2C%22nickName%22%3A%22%22%2C%22nickname%22%3A%22%22%2C%22token%22%3A%22E9FF4FF9F0EEFD65597745707CD1CFCB470D04EDF57F6AB8F2F901139AEF0CC0%22%2C%22tokenKey%22%3A%22alpha_deepfos_token%22%2C%22type%22%3A1%2C%22userId%22%3A%22185f66d3-083d-4c9b-b653-fe3fa505c26a%22%2C%22username%22%3A%22Zhanghaiyan%22%7D; alpha_deepfos_token=E9FF4FF9F0EEFD65597745707CD1CFCB470D04EDF57F6AB8F2F901139AEF0CC0', 'envUrl': 'http://web-gateway'}
#: 业务参数
# para2 = [{'Year': '2022', 'Period': '8'}]
# para2 = [{'record_id': '8b0386d421f611edb1cbbecf7ba854f4'}, {'record_id': '8b03c32e21f611edb1cbbecf7ba854f4'},
#          {'record_id': '8b03f7d621f611edb1cbbecf7ba854f4'}]
para2 = {'Year': '2022', 'Period': '6', 'Entity': 'FDC010', 'By1': 'NoBy1', 'By2': 'NoBy2', 'sheetName': '项目成员月度考核表',
         'sheetId': 'SHTa2f06e64a9db'}

#: 环境域名，根据自己的使用环境更改
host = "https://alpha.deepfos.com"

# -----------------------------------------------------------------------------
# 下面的代码是固定的

OPTION.general.use_eureka = False
OPTION.server.base = f"{host}/seepln-server"
OPTION.server.app = f"{host}/seepln-server/app-server"
OPTION.server.system = f"{host}/seepln-server/system-server"
OPTION.server.space = f"{host}/seepln-server/space-server"
OPTION.server.platform_file = f"{host}/seepln-server/platform-file-server"
OPTION.api.header = para1
OPTION.api.dump_on_failure = True
