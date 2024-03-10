import logging

#configure logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='log.txt',
    filemode='a'
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)


# Call the setup function to configure logging
setup_logging()
