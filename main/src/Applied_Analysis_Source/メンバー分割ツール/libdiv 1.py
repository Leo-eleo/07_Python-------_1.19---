import time
import math
import argparse
import sys
import os


def main(infile, outdir, encode, extension, recLen):

    print("Infile          :["+infile+"]")
    print("Outdir          :["+outdir+"]")
    print("Encode          :["+encode+"]")

    # 時間計測開始
    time_sta = time.time()

    # 入力ファイルオープン
    fin = open(infile,  mode='r', encoding=encode, errors='ignore')
    datalist = fin.read().splitlines()

    # ディレクトリ作成
    os.makedirs(outdir, exist_ok=True)

    # 時間計測開始
    time_sta = time.time()
    totalline = len(datalist)
    delimiter = math.ceil(totalline/10)
    print("***LIBRARY DIV Start***")
    print('\r'+"Progress        :0％", end='')
    dsinf=False
    dsname=""
    for line, data in enumerate(datalist):
        if line % delimiter == 1:
            pst = int(line/totalline*100)
            print('\r'+"Progress        :"+str(pst)+"％", end='')
        if data and data[0] == "1" :
            predsname=dsname
            if "DSNAME :" in datalist[line+1]:
                dsname = datalist[line+1][34:].split()[0]
            if "LIBRARY NAME" in datalist[line+1]:
                dsname = datalist[line+1][53:].split()[0]
            if "DSNAME :" in datalist[line+1] and dsname != predsname:
                if not "(" in datalist[line+1]:
                    dsinf=True
                    if not line == 0:
                        fout.close()
                    outfile = outdir + "\\" + dsname + ".inf"
                    fout = open(outfile, 'w')
                else :
                    if not line == 0:
                        fout.close()
                    member = dsname.split('(')[1].split(')')[0]
                    outfile = outdir + "\\" + member + "."+extension
                    fout = open(outfile, 'w')
            if "LIBRARY NAME" in datalist[line+1] and dsname != predsname:
                    if not line == 0:
                        fout.close()
                    member = dsname.split('(')[1].split(')')[0]
                    outfile = outdir + "\\" + member + "."+extension
                    fout = open(outfile, 'w')
        if dsinf:
            fout.write(data+'\n')

        else:
            if data and data[0] == " " :
                if recLen > 100 :
                    if line+1 != len(datalist) and datalist[line+1][0] == '1':
                        inc=5
                    else:
                        inc=1
                    row = ""
                    i = 0
                    while len(row.encode(encode)) < 100:
                        row += data[14+i]
                        i += 1
                    if line+1 != len(datalist) and datalist[line+inc][5] == ' ':
                        fout.write(row)
                    else:
                        fout.write(row+'\n')
                else:
                    fout.write(data[14:]+'\n')
            else :
                pass

        if "END OF MEMBER LISTING" in data:
            dsinf=False

    # クローズ
    fin.close()
    fout.close()
    # 時間計測終了
    time_end = time.time()
    # 経過時間（秒）
    tim = round(time_end - time_sta, 2)
    print('\r'+"Progress        :100％")
    print('\r'+"Return Code     :[0]")
    print("***END:"+str(tim)+"(s)***")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='ライブラリ形式のソースコードを分割する')

    parser.add_argument('input', type=str,
                        help='インプットファイルパス')
    parser.add_argument('output', type=str,
                        help='アウトプットフォルダパス')
    parser.add_argument('-e', '--encode', type=str,
                        default=sys.getdefaultencoding(),
                        help='エンコード、デフォルトはOS準拠')
    parser.add_argument('-x', '--extension', type=str,
                        default='txt',
                        help='出力ソースの拡張子(.抜き)、デフォルトはtxt')
    parser.add_argument('-l', '--recLen', type=int,
                        default=80,
                        help='レコード長、デフォルトは80')
    args = parser.parse_args()

    main(args.input, args.output, args.encode, args.extension, args.recLen)
