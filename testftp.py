import ftplib
import os
import socket
import sys

# HOST = 'ftp-trace.ncbi.nlm.nih.gov'
DIRN = './'
FILE = 'xue.jpg'
USER_NAME = ''
PWD = ''


def rcussivedownload(f, DIR, FDIR, HOST, filelist):
    f.cwd(DIR)
    tupleinform = f.mlsd()
    for item in tupleinform:
        print(item)
        isdownload = True
        if item[1]["type"] == "file":
            link = "ftp://" + HOST + "/" + FDIR + "/" + item[0]
            size = item[1]['size']
            filename = item[0]
            try:
                file = open(item[0], 'wb')
                f.retrbinary('RETR %s' % os.path.basename(item[0]), file.write)
                file.close()
            except:
                isdownload = False
                print('ERROR:cannot read file %s' % item[0])
                os.unlink(item[0])
                file.close()
            filelist.append([filename, link, size, isdownload])
        elif item[1]["type"] == "dir":
            rcussivedownload(f, item[0], FDIR + '/' + item[0], HOST, filelist)
    f.cwd("..")


def DownloadFile(HOST, DIR):
    try:
        f = ftplib.FTP()
    except(socket.error, socket.gaierror) as e:
        print('ERROR:cannot reach %s' % HOST)
        return
    print('*** Connected to host %s' % HOST)
    f.connect(HOST)
    try:
        f.login()
    except ftplib.error_perm:
        print('ERROR:cannot login USER_NAME=%s, PWD=%s' % (USER_NAME, PWD))
        f.quit()
        return
    print('*** Logined in as %s' % USER_NAME)
    filelist = []
    rcussivedownload(f, DIR, DIR, HOST, filelist)
    f.quit()
    return filelist
    # f.cwd(DIR)
    # tupleinform=f.mlsd()
    # for item in tupleinform:
    #     print(item)
    #     if item[1]["type"]=="file":
    #         link="ftp://"+HOST+"/"+DIR+"/"+item[0]
    #         size=item[1]['size']
    #         with open(item[0],'w') as file:
    #             f.retrbinary('RETR %s' % item[0],file)
    #     elif item[1]["type"]=="dir":
    #         DownloadFile(HOST,DIR+'/'+item[0])
    # try:
    #     f.cwd(DIRN)
    # except ftplib.error_perm:
    #     print('ERROR:cannot CD to %s' % DIRN)
    #     f.quit()
    #     return
    #
    # try:
    #     file = open(file_name, 'wb')
    #     f.retrbinary('RETR %s' % file_name, file.write)
    #     file.close()
    #
    # except ftplib.error_perm:
    #     print('ERROR:cannot read file %s' % file_name)
    #     os.unlink(file_name)
    #     file.close()
    # else:
    #     print('*** Downloaded %s to %s' % (file_name, os.getcwd()))
    # f.quit()
    # return


if __name__ == '__main__':
    DownloadFile(sys.argv[1], sys.argv[2])
    # DownloadFile("ftp-trace.ncbi.nlm.nih.gov","sra/sra-instant/reads/ByExp/sra/SRX/SRX003/SRX003135")
