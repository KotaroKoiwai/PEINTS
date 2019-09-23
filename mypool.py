# -*- coding: utf-8 -*-

from multiprocessing import Process, Pipe, cpu_count


class MyPool:
    proc_num = cpu_count()

    def __init__(self, proc_num):
        self.proc_num = proc_num

    def map(self, func, args):
        def pipefunc(conn, arg):
            conn.send(func(arg))
            conn.close()

        ret = []
        k = 0
        while (k < len(args)):
            plist = []
            clist = []
            end = min(k + self.proc_num, len(args))
            for arg in args[k:end]:
                pconn, cconn = Pipe()
                plist.append(Process(target=pipefunc, args=(cconn, arg,)))
                clist.append(pconn)
            for p in plist:
                p.start()
            for conn in clist:
                ret.append(conn.recv())
            for p in plist:
                p.join()
            k += self.proc_num
        return ret
