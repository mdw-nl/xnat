from config_handler import Config
from consumer import Consumer
from send_dicom_to_XNAT import sendDICOM

rabbitMQ_config = Config("rabbitMQxnat")
cons = Consumer(rmq_config=rabbitMQ_config)
cons.open_connection_rmq()
cons.send_message("messages")