if __name__ == '__main__':
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
