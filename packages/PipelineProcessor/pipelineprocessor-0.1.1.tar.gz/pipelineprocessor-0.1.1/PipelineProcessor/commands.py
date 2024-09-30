from typing import Optional
import typer
import sys
import logging
from logging import Logger

from PipelineProcessor.BasicFunctionRepository import BasicFunctionRepository
from PipelineProcessor.BasicStreamFunctionRepository import BasicStreamBasicFunctionRepository
from PipelineProcessor.FileHandler import FileHandler
from PipelineProcessor.Processor import Processor
from PipelineProcessor.StreamFunctionRepository import StreamFunctionRepository
from PipelineProcessor.YmlConfigLoader import YmlConfigLoader

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
app = typer.Typer()

@app.command()
def process_file(input_filename: str, yml_path: str, output_filename: Optional[str] = None) -> None:
    """
    Processes a file according to transformations specified in a YAML configuration file.

    Args:
        input_filename (str): Path to the input file.
        yml_path (str): Path to the YAML configuration file specifying transformations.
        output_filename (Optional[str]): Path to the output file where transformed data will be saved.
                                        If None, the output is not saved to a file.
    """
    # logging
    logger: Logger = logging.getLogger()

    file_handler: FileHandler = FileHandler(logger=logger, input_filename=input_filename,
                                            output_filename=output_filename)
    yml_config_loader: YmlConfigLoader = YmlConfigLoader(logger=logger, yml_path=yml_path)
    repository: BasicFunctionRepository = BasicFunctionRepository()
    processor = Processor(logger=logger, io_handler=file_handler, config_loader=yml_config_loader,
                          function_repositories=[repository])
    processor.process(['upper_case', 'remove_stop_words', 'lower_case', 'uk_to_us', 'capitalized'])

stream_app = typer.Typer()

@stream_app.command()
def process_file_stream_pipeline(input_filename: str,
                                 yml_path: str,
                                 additional_function_path: Optional[str] = None,
                                 output_filename: Optional[str] = None) -> None:
    """
    Processes a file in a streaming manner using multiple function repositories, potentially including
    additional transformations loaded from a specified path.

    Args:
        input_filename (str): Path to the input file.
        yml_path (str): Path to the YAML configuration file specifying transformations.
        additional_function_path (Optional[str]): Path to an additional file containing more transformation functions.
        output_filename (Optional[str]): Path to the output file where transformed data will be saved.
                                         If None, the output is not saved to a file.
    """
    # logging
    logger: Logger = logging.getLogger()

    # instantiate File handler
    file_handler: FileHandler = FileHandler(logger=logger, input_filename=input_filename,
                                            output_filename=output_filename)
    # instantiate Yml Config Loader
    yml_config_loader: YmlConfigLoader = YmlConfigLoader(logger=logger, yml_path=yml_path)

    # instantiate Function repositories
    stream_repository: StreamFunctionRepository = StreamFunctionRepository()
    extended_stream_repository: BasicStreamBasicFunctionRepository = BasicStreamBasicFunctionRepository()

    # instantiate processor
    processor: Processor = Processor(logger=logger, io_handler=file_handler,
                                     config_loader=yml_config_loader,
                                     function_repositories=[stream_repository, extended_stream_repository])
    # call processor
    processor.stream_process(additional_function_path=additional_function_path)
