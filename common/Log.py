import logging

def loginit():
    loginfo = "%(levelname)-10s"
    logtime = "%(asctime)s "
    logthread = "%(threadName)-50s"
    logmsg = "%(message)s"
    
    logging.basicConfig(level = logging.INFO,
    # logging.basicConfig(filename = 'serverlog.log', level = logging.INFO, filemode = 'w',
                        format = loginfo + logtime + logthread + logmsg)
