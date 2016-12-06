import os
import os.path
import subprocess

def retrieving(file,outpath,link):
    '''Download data'''
    log= open(outpath+file+'_log.txt','w')
    os.chdir(outpath)
    print(os.curdir)
    try:
        cmd = 'wget '+link
        print(cmd)
        if not os.path.exists(outpath+file):
            status = subprocess.call(cmd)
            if status !=0:
                log.write('\nFailed:'+file)
            else:
                log.write('\nSuccess:'+file)
        log.flush()
    except:
        log.write('\nFailed:'+file)
    log.close()