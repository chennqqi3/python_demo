import re

content = '<downloadURL>http://o.qikucdn.com/test/filedownload/ota/Android/QK1607/PX/stable_7.0.011.PX.170320.360_360_QK1607_CN_stable_7.0.014.PX.170323.360_360_QK1607_CN/update_1490594453675.zip</downloadURL><dstGroup>stable</dstGroup><dstVersion>7.0.014.PX.170323.360_360_QK1607_CN</dstVersion><md5>EB544CB92DE1E4E979C27EC39BEF93C9</md5><priority>'
pattern = re.compile('<downloadURL>(.*)</downloadURL>.*[<md5>(.*)</md5>]', re.S)

match = re.search(pattern, content)

if match:
    print('ddfd')
