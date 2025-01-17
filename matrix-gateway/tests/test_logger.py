import logging
from app.utils.logging import setup_logger  # Adjust the import based on your project structure

def test_setup_logger():
    # Test setup_logger function
    logger_name = "test_logger"
    logger_level = logging.DEBUG

    # Call the setup_logger function
    logger = setup_logger(logger_name, logger_level)

    # Assertions
    assert logger.name == logger_name, "Logger name does not match"
    assert logger.level == logger_level, "Logger level does not match"

    # Check if the logger has a StreamHandler
    stream_handler = None
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            stream_handler = handler
            break
    assert stream_handler is not None, "Logger should have a StreamHandler"

    # Check if the handler has the correct formatter
    formatter = stream_handler.formatter
    assert isinstance(formatter, logging.Formatter), "Handler should have a Formatter"
    assert (
        formatter._fmt == '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ), "Formatter format does not match"

    # Check if the handler is added only once
    assert len(logger.handlers) == 1, "Logger should only have one handler"
