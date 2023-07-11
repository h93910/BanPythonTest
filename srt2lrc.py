if __name__ == '__main__2':
    import re

    srt_path = "D:\Ban\Music\国语歌\黄明志\黃明志 Ft. 蒼井空【別人的老婆】@高清無碼 2022 H.D. & Uncensored-a1T2FVLP29M.srt"
    r = "\d{2}:(\d{2}:\d{2},\d{2}).*?\d{2}:(\d{2}:\d{2},\d{2})"  # 寻找时间戳
    result = []
    with open(srt_path, encoding="utf-8") as f:
        content = f.read().splitlines()
        for i in range(1, len(content), 4):
            matchObj = re.match(r, content[i], re.M | re.I)
            if matchObj:
                result.append("[%s]%s\n" % (matchObj.group(1).replace(",", "."), content[i + 1]))
                result.append("[%s]\n" % (matchObj.group(2).replace(",", ".")))
        print(result)

    with open(srt_path.replace("srt", "lrc"), 'w+') as text:
        text.writelines(result)

# 咒分割成歌词文件
if __name__ == "__main__":
    from datetime import datetime
    import re

    content = '''tù sěizhà zhìduō

　　突瑟咤质多 (恶心鬼)

　　e mò dàn lì zhìduō

　　阿末怛唎质多　 (恶毒鬼)

　　wū shé hē là

　　乌阇诃啰　 (食精鬼)

　　qié pó hē là

　　伽婆诃啰　 (食胎鬼)

　　lú dì là hē là

　　嚧地啰诃啰　 (食血鬼)

　　pó suō hē là

　　婆娑诃啰 (食油鬼)

　　mó shé hē là

　　摩阇诃啰　 (食产鬼)

　　shé duō hē là

　　阇多诃啰 (食肉鬼)

　　shì bì duō hē là

　　视毖多诃啰　 (食命鬼)

　　bá lüè yè hē là

　　跋略夜诃啰　 (食祭鬼)

　　qiántuó hē là

　　干陀诃啰 (食香鬼)

　　bù shǐ bō hē là

　　布史波诃啰 (食花鬼)

　　pō là hē là

　　颇啰诃啰　 (食果鬼)

　　pó xiě hē là

　　婆写诃啰　 (食种子鬼)

　　bō bō zhìduō

　　般波质多　 (恶形鬼)

　　tù sěi zhà zhìduō

　　突瑟咤质多 (恶眼鬼)

　　làotuó là zhìduō

　　唠陀啰质多 (巨头鬼)(以佛菩萨千百亿身手，降伏一切大力鬼神)

　　yàochā jiēlà hē

　　药叉揭啰诃 (吞火鬼)

　　là chà suō jiē là hē

　　啰剎娑.揭啰诃 (吞水鬼)

　　bì lì duō　jiē là hē

　　闭口隶多.揭啰诃 (交手鬼)

　　pí shě zhē jiē là hē

　　毗舍遮.揭啰诃 (交足鬼)

　　bù duō jiē là hē

　　部多揭啰诃 (交身鬼)

　　jiū pánchá jiē là hē

　　鸠盘茶.揭啰诃 (分形鬼)

　　xī qiántuó jiē là hē

　　悉干陀.揭啰诃 (吐烟鬼)

　　wū dàn mó tuó jiē là hē

　　乌怛摩陀.揭啰诃 (吐火鬼)

　　chē yè jiē là hē

　　车夜揭啰诃 (形影鬼)

　　ebō sà mó làjiē là hē

　　阿播萨摩啰.揭啰诃 (羊头瞋鬼)

　　zhái qū gé chá qí níjiē là hē

　　宅袪革.茶耆尼.揭啰诃 (刑人狐鬼、狸魅女鬼)

　　lì fó dìjiē là hē

　　唎佛帝.揭啰诃 (恼小儿鬼)

　　shé mí jiā　jiē là hē

　　阇弥迦.揭啰诃 (如乌鬼)

　　shě jù níjiē là hē

　　舍俱尼.揭啰诃 (如鸟鬼)

　　lǎotuó là nándì jiā jiē là hē

　　姥陀啰难地迦.揭啰诃 (如猫鬼)

　　e lán pójiē là hē

　　阿蓝婆.揭啰诃 (如蛇鬼)

　　qián dù bō ní jiē là hē

　　干度波尼.揭啰诃 (如鸡鬼)

　　shí fá là yīnjiā xījiā

　　什伐啰　堙迦醯迦 (壮热鬼、一日疟鬼)

　　zhuìdì yàojiā

　　坠帝药迦 (二日疟鬼)

　　dá lì dì yàojiā

　　怛隶帝药迦 (三日疟鬼)

　　zhě tù tuō jiā

　　者突托迦 (五日疟鬼)

　　ní tíshí fá là　bì shānmóshí fá là

　　尼提.什伐啰　毖钐摩.什伐啰 (常热鬼、增寒鬼)

　　bó dǐ jiā

　　薄底迦 (风病鬼)

　　bí dǐ jiā

　　鼻底迦 (黄病鬼)

　　shì lì sěi mì jiā

　　室口隶瑟密迦 (疫病鬼)

　　suō nǐ bō dì jiā

　　娑你般帝迦 (痢病鬼)

　　sà póshí fá là

　　萨婆什伐啰 (头病鬼)

　　shì lú jí dì

　　室嚧吉帝

　　mò tuó pí dá lúzhìjiàn

　　末陀鞞达嚧制剑 (不食鬼)

　　eqǐ lú qián

　　阿绮嚧钳 (口痛鬼)

　　mu qié lúqián

　　目佉嚧钳 (齿痛鬼)

　　jié lì tù lú qián

　　羯唎突嚧钳 (唇痛鬼)

　　jiē là hē　jiē lán

　　揭啰诃.揭蓝 (身病鬼)

　　jié ná shūlán

　　羯拏输蓝

　　dànduō shūlán

　　惮多输蓝 (颐颔痛鬼)

　　qì lì yè shū lán

　　迄唎夜输蓝 (心痛鬼)

　　mò mò shū lán

　　末么输蓝 (头痛鬼)

　　bá lì shìpó shū lán

　　跋唎室婆输蓝 (两胁痛鬼)

　　bì lì sěizhà shūlán

　　毖栗瑟咤输蓝 (背痛鬼)

　　wūtuó là shūlán

　　乌陀啰输蓝 (腹痛鬼)

　　jiézhī shūlán

　　羯知输蓝 (腰痛鬼)

　　bá xī dì shūlán

　　跋悉帝输蓝 (踝痛鬼)

　　wū lú shūlán

　　邬嚧输蓝 (腿痛鬼)

　　chángqiéshūlán

　　常伽输蓝 (腕痛鬼)

　　hè xī duō shūlán

　　喝悉多输蓝 (两手痛鬼)

　　bá tuó shūlán

　　跋陀输蓝 (四肢骨节痛鬼)

　　suōfángyàngqié bōlà zhàngqiéshūlán

　　娑房盎伽.般啰丈伽输蓝 (两膊痛鬼)

　　bù duō bìduōchá

　　部多毖哆茶 (尸林鬼)

　　chá qí ní　shí pó là

　　茶耆尼 什婆啰 (魅鬼、一切疮鬼)

　　tuó tù lú jiā　jiànduō lú jízhī 　pó lù duō pí

　　陀突嚧迦　建咄嚧吉知　婆路多毗　 (蜘蛛疮鬼、疔疮鬼)

　　sà bō là hē ling qié

　　萨般嚧诃凌伽 (漫淫疮鬼、赤疮鬼)

　　shūshā dàn làsuō nà jié là

　　输沙怛啰　娑那羯啰 (小儿疮鬼、颠狂鬼)

　　pí shā yù jiā　e

　　毗沙喻迦 (癞疮鬼)

　　qí níwū tuó jiā

　　阿耆尼.乌陀迦 (火毒鬼、水毒鬼)

　　mò là pí là jiànduòlà

　　末啰鞞啰建跢啰 (女死鬼)

　　ejiā là mì lì duō dànliǎn bù jiā

　　阿迦啰密唎咄.怛敛部迦 (横死鬼、药草毒鬼)

　　dì lì là zhà

　　地栗剌咤 (蝎毒鬼)

　　bì lì sěi zhìjiā

　　毖唎瑟质迦

　　sà pó nà jù là

　　萨婆那俱啰 (蛇毒鬼)

　　sì yǐn qié bì jiē là lì yàochā dàn là chú

　　肆引伽弊.揭啰唎药叉.怛啰刍 (虎狼毒鬼、狮子毒鬼、一切恶毒鬼)

　　mò là shìfèidìshàn suō pí shàn

　　末啰视.吠帝钐.娑鞞钐 (熊罴毒鬼，用制此类一切恶鬼，悉皆畏伏)

　　xī dàn duō　bō dá là

　　悉怛多.钵怛啰 (依此大白伞盖心咒)

　　mó hē bá shé là sěiníshān

　　摩诃跋阇嚧瑟尼钐 (启请火头金刚藏王)

　　mó hē bō lài zhàngqílán

　　摩诃般赖丈耆蓝 (诸护法大力士神王圣众)

　　yè bō tù tuó shěyù shé nuó

　　夜波突陀.舍喻阇那　 (至此尽庆圆成)

　　biàn dálì nú

　　辫怛口隶拏

　　pí tuó yē　pántán jiā lú mí

　　毗陀耶.盘昙迦嚧弥 (依此佛顶光聚大明心咒，不得入我结缚界内)

　　dì shú pántán jiā lú mí

　　帝殊.盘昙迦嚧弥 (十二由旬结界地面,禁缚诸恶一切邪魔恶鬼神王,不能进入扰害)

　　bō là pítuópántán jiā lú mí

　　般啰毘陀.盘昙迦嚧弥 (依此咒缚诸恶鬼神众)

　　duō zhí tuō

　　哆侄他 (我今说此咒心)

　　ān

　　唵 (唵 为毗卢佛根本，能警觉一切)

　　ā　nàlì

　　阿那口隶 (无上)

　　pí shě tí　　 chì

　　毘舍提 (乃宣佛敕)

　　pí là bá shé làtuó lì

　　鞞啰跋阇啰陀唎 (一切众类，仰如来力)

　　pántuó pántuó nǐ

　　盘陀盘陀你 (闻诵此咒悉当合掌恭敬顶礼)

　　bá shé là bàng ní pàn

　　跋阇啰.谤尼泮 (汝等承佛威力，各来卫护，行住坐卧不相舍离)

　　hǔxìn dū lú yōng pàn

　　虎合牛　都嚧瓮泮 (再严伏一切朋党眷属。汝等谛听，各归其所)

　　suō pó hē

　　莎婆诃 (向无上道，直至菩提)

　 duō zhí tuō

　　哆侄他 (我今说此咒心)

　　ān

　　唵 (唵 为毗卢佛根本，能警觉一切)

　　ā　nàlì

　　阿那口隶 (无上)

　　pí shě tí　　 chì

　　毘舍提 (乃宣佛敕)

　　pí là bá shé làtuó lì

　　鞞啰跋阇啰陀唎 (一切众类，仰如来力)

　　pántuó pántuó nǐ

　　盘陀盘陀你 (闻诵此咒悉当合掌恭敬顶礼)

　　bá shé là bàng ní pàn

　　跋阇啰.谤尼泮 (汝等承佛威力，各来卫护，行住坐卧不相舍离)

　　hǔxìn dū lú yōng pàn

　　虎合牛　都嚧瓮泮 (再严伏一切朋党眷属。汝等谛听，各归其所)

　　suō pó hē

　　莎婆诃 (向无上道，直至菩提)

   duō zhí tuō

　　哆侄他 (我今说此咒心)

　　ān

　　唵 (唵 为毗卢佛根本，能警觉一切)

　　ā　nàlì

　　阿那口隶 (无上)

　　pí shě tí　　 chì

　　毘舍提 (乃宣佛敕)

　　pí là bá shé làtuó lì

　　鞞啰跋阇啰陀唎 (一切众类，仰如来力)

　　pántuó pántuó nǐ

　　盘陀盘陀你 (闻诵此咒悉当合掌恭敬顶礼)

　　bá shé là bàng ní pàn

　　跋阇啰.谤尼泮 (汝等承佛威力，各来卫护，行住坐卧不相舍离)

　　hǔxìn dū lú yōng pàn

　　虎合牛　都嚧瓮泮 (再严伏一切朋党眷属。汝等谛听，各归其所)

　　suō pó hē

　　莎婆诃 (向无上道，直至菩提)
    '''
    content = re.sub(r'\u3000', '', content)  # 去除空格
    content = [x.rstrip() for x in content.split('\n') if len(x.rstrip()) > 0]

    time_style = '%H:%M:%S'
    start_time = datetime.strptime('00:20:31', time_style)
    end_time = datetime.strptime('00:25:19', time_style)
    total_word = 0  # 总共多少个读的字
    for s in content[1::2]:  # 这里 arr[1::2] 表示从数组arr从下标1开始以步长为2提取元素。取出读的文字
        first_p = s.find('(')
        if first_p != -1:
            c = s[0:first_p]
        else:
            c = s
        print(c)
        total_word += len(c)
    interval = (end_time - start_time) / total_word  # 读每个字的间隔

    last_time = start_time  # 上一个时间点
    for i in range(0, len(content), 2):  # 两段为一节来取
        # - strftime('%M:%S.%f') 将时间格式化为分:秒.微秒
        # - [:8] 取格式化字符串的前8位,保留小数点后2位毫秒
        tag_time = last_time
        t = tag_time.strftime('%M:%S.%f')[:8]
        print(f'[{t}]{content[i]}')
        # 计算下一段词的起始时间
        s = content[i + 1]
        first_p = s.find('(')
        if first_p != -1:
            c = s[0:first_p]
        else:
            c = s
        print(f'[{t}]{c}')
        if first_p != -1:
            print(f'[{t}]{s[first_p:]}')
        last_time = last_time + interval * len(c)
    print(last_time.strftime('%M:%S.%f')[:8])
