#!/usr/bin/env python
# encoding: utf-8

import fcntl

class file_rw_lock():
    # linux 文件格式
    # 锁位置

    def __init__(self, lockfile):
        self.lockfilename = lockfile

    def __openlockfile(self, filename):
        if not os.path.exists(filename):
            try:
                cmdStr = 'touch %s'
                args = [filename]
                exec_single_cmd_with_log(cmdStr, args=args)
                os.chmod(filename, (stat.S_IRWXU | stat.S_ISGID)
                         & (~stat.S_IXGRP))
            except Exception, e:
                return None

        file = None
        try:
            file = open(filename, "w")
        except Exception, e:
            pass
        return file

    def try_r_lock(self):
        self.lockfile = self.__openlockfile(self.lockfilename)

        if self.lockfile == None:
            return False
        bexcret = False
        try:
            fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
            bexcret = True
        except :
            pass
        return bexcret

    def try_w_lock(self):
        self.lockfile = self.__openlockfile(self.lockfilename)
        if not self.lockfile:
            return False

        bexcret = False
        try:
            fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            bexcret = True
        except IOError, e:
            pass
        return bexcret

    def unlock(self):
        if self.lockfile:
            fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_UN)
            self.lockfile.close()

    def wait_r_lock(self):
        wself.lockfile = self.__openlockfile(self.lockfilename)

        if self.lockfile == None:
            return False
        bexcret = False
        try:
            fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_SH)
            bexcret = True
        except IOError, e:
            pass
        return bexcret

    def wait_w_lock(self):
        self.lockfile = self.__openlockfile(self.lockfilename)
        if not self.lockfile:
            return False

        bexcret = False
        try:
            fcntl.flock(self.lockfile.fileno(), fcntl.LOCK_EX)
            bexcret = True
        except IOError, e:
            pass
        return bexcret
