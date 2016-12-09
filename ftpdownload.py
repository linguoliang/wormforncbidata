import ftplib
import os
import socket
import sys

# HOST = 'ftp-trace.ncbi.nlm.nih.gov'
DIRN = './'
FILE = 'xue.jpg'
USER_NAME = ''
PWD = ''


# def rcussivedownload(f, DIR, FDIR, HOST, filelist):
#
#     try:
#         f.cwd(DIR)
#     except:
#         filelist.append(["error",'','0',False])
#         return
#     tupleinform = f.mlsd()
#     for item in tupleinform:
#         print(item)
#         isdownload = True
#         if item[1]["type"] == "file":
#             link = "ftp://" + HOST + "/" + FDIR + "/" + item[0]
#             size = item[1]['size']
#             filename = item[0]
#             try:
#                 file = open(item[0], 'wb')
#                 f.retrbinary('RETR %s' % os.path.basename(item[0]), file.write)
#                 file.close()
#             except:
#                 isdownload = False
#                 print('ERROR:cannot read file %s' % item[0])
#                 os.unlink(item[0])
#                 file.close()
#             filelist.append([filename, link, size, isdownload])
#         elif item[1]["type"] == "dir":
#             rcussivedownload(f, item[0], FDIR + '/' + item[0], HOST, filelist)
#     f.cwd("..")

def rcussivedownload(DIR, HOST, filelist):
    m = openftp(HOST)
    if m[0] != 1:
        print(m[1], file=sys.stderr)
        filelist.append(["error", '', '0', False])
        m[1].quit()
        return
    f = m[1]
    try:
        f.cwd(DIR)
    except:
        filelist.append(["error", '', '0', False])
        f.quit()
        return
    listfor=[]
    tupleinform = f.mlsd()
    for item in tupleinform:
        listfor.append(item)
    f.quit()
    for item in listfor:
        # print(item)
        isdownload = True
        if item[1]["type"] == "file":
            m = openftp(HOST)
            if m[0] != 1:
                print(m[1], file=sys.stderr)
                filelist.append(["error", '', '0', False])
                m[1].quit()
                return
            f = m[1]
            try:
                f.cwd(DIR)
            except:
                filelist.append(["error", '', '0', False])
                f.quit()
                return
            link = "ftp://" + HOST + "/" + DIR + "/" + item[0]
            size = item[1]['size']
            filename = item[0]
            f.voidcmd('TYPE I')
            fsize = f.size(filename)
            if fsize == 0:  # localfime's site is 0
                filelist.append([filename, link, size, isdownload])

            # check local file isn't exists and get the local file size
            lsize = 0
            if os.path.exists(filename):
                lsize = os.stat(filename).st_size

            if lsize >= fsize:
                print('local file is bigger or equal remote file')
                print(filename+"is downloaded")
                filelist.append([filename, link, size, isdownload])
                f.quit()
                return

            blocksize = 1024 * 1024
            cmpsize = lsize
            f.voidcmd('TYPE I')
            conn = f.transfercmd('RETR ' + filename, lsize)
            lwrite = open(filename, 'ab')
            while True:
                data = conn.recv(blocksize)
                if not data:
                    break
                lwrite.write(data)
                cmpsize += len(data)
                # print('\b' * 30, 'download process:%.2f%%' % (float(cmpsize) / fsize * 100),end='\r')
            print(filename+"is downloaded")
            lwrite.close()
            f.voidcmd('NOOP')
            f.voidresp()
            conn.close()
            f.quit()
            # try:
            #     file = open(item[0], 'wb')
            #     f.retrbinary('RETR %s' % os.path.basename(item[0]), file.write)
            #     file.close()
            # except:
            #     isdownload = False
            #     print('ERROR:cannot read file %s' % item[0])
            #     os.unlink(item[0])
            #     file.close()
            filelist.append([filename, link, size, isdownload])
        elif item[1]["type"] == "dir":
            rcussivedownload(DIR + '/' + item[0], HOST, filelist)
            # else:
            #     f.quit()
            # f.cwd("..")



def openftp(HOST, USER_NAME='', PWD=''):
    try:
        f = ftplib.FTP()
    except(socket.error, socket.gaierror) as e:
        print('ERROR:cannot reach %s' % HOST)
        return (0, f)
    # print('*** Connected to host %s' % HOST)
    f.connect(HOST)
    try:
        f.login(USER_NAME, PWD)
    except ftplib.error_perm:
        print('ERROR:cannot login USER_NAME=%s, PWD=%s' % (USER_NAME, PWD))
        f.quit()
        return (0, f)
    # print('*** Logined in as %s' % USER_NAME)
    return (1, f)


def DownloadFile(HOST, DIR):
    # try:
    #     f = ftplib.FTP()
    # except(socket.error, socket.gaierror) as e:
    #     print('ERROR:cannot reach %s' % HOST)
    #     return
    # print('*** Connected to host %s' % HOST)
    # f.connect(HOST)
    # try:
    #     f.login()
    # except ftplib.error_perm:
    #     print('ERROR:cannot login USER_NAME=%s, PWD=%s' % (USER_NAME, PWD))
    #     f.quit()
    #     return
    # print('*** Logined in as %s' % USER_NAME)
    filelist = []
    rcussivedownload(DIR, HOST, filelist)
    # f.quit()
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
    # return # except ftplib.error_perm:
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
