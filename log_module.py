import logging
logger = logging.getLogger("protopool")
hdlr = logging.FileHandler('./protopool.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
