import logging

def loginit():
    loginfo = "%(levelname)-10s"
    logtime = "%(asctime)s "
    logthread = "%(threadName)-50s"
    logmsg = "%(message)s"
    
    logging.basicConfig(level = logging.INFO,
    # logging.basicConfig(filename = 'serverlog.log', level = logging.INFO, filemode = 'w',
                        format = loginfo + logtime + logthread + logmsg)
    
    # README
    # Használat:
    # import logging
    # logging.info("LOGIN message received")
    # talán kicsit szebb lenne, ha ezt az osztály kéne importolni és lenne itt egy loginfo(str) függvény

