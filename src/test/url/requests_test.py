import re

import requests


class OtaModel:
    def __init__(self, hw, hwv, swv):
        self.hw = hw
        self.hwv = hwv
        self.swv = swv

    def __str__(self):
        return 'hw:%s,hwv:%s,swv:%s' % (self.hw, self.hwv, self.swv)


class request_test:
    def __init__(self, ota_model):
        self.url = 'http://t.ota1.os.qiku.com/ota/checkupdate' + \
                   '?m2=4a5a82237b2675d098352934a0522ec6' + \
                   '&cpuid=unknow' + \
                   '&userstart=1' + \
                   '&hw=' + ota_model.hw + \
                   '&imei=8948a03ce379af65a3bba93e1dd9cb2d' + \
                   '&hwv=' + ota_model.hwv + \
                   '&swv=' + ota_model.swv + \
                   '&src_type=stable' \
                   '&serialno=47f569cd' \
                   '&curnetwork=0' \
                   '&emmc=90014a484247346132a447f569cdc300'

    def test(self):
        print(self.url)
        res = requests.get(self.url)

        print(res.status_code)


def analyze_input():
    # exists = os.path.exists(input_file)
    # if not exists:
    #     print("参数文件不存在，请确认文件路径！！")
    #     exit()
    params_list = []
    with open('C:\\Users\weidongdong\Desktop\临时\ota\\args.txt') as input_f:
        for line in input_f.readlines():
            r = re.compile('\t+')
            split = r.split(line.strip('\n'))
            model = OtaModel(split[0], split[1], split[2])
            params_list.append(model)

    return params_list


if __name__ == '__main__':
    params = analyze_input()

    # out_dir = sys.argv[2]
    for param in params:
        print(param)
        test = request_test(param)
        test.test()
