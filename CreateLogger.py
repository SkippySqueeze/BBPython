import logging

formatter = logging.Formatter('%(asctime)s %(message)s')


def createlogger(name, folder, filename, level):
	logger = logging.getLogger(name)
	hdlr_1 = logging.FileHandler('logs/'+folder+'/'+filename+'.log')
	hdlr_1.setFormatter(formatter)
	hdlr_1.setLevel(level)
	logger.addHandler(hdlr_1)
	logger.setLevel(level)
	return logger
