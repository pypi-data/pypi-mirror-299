import os
import hashlib
import json
import tempfile
from typing import Optional, Tuple
import pathlib
import logging

from roboto.action_runtime import ActionRuntime
from roboto import CreateTopicRequest, Dataset, Invocation, Topic, RepresentationStorageFormat, SetDefaultRepresentationRequest, RobotoClient
from roboto.association import Association, AssociationType
from roboto.exceptions import RobotoConflictException
from roboto.action_runtime.exceptions import ActionRuntimeException


def setup_output_folder_structure(
        file_path: str,
        input_dir: str
) -> Tuple[str, str]:
    """
    This function sets up the output folder structure for the visualization assets.

    Args:
    - file_path: The path to the input file.
    - input_dir: The input directory.

    Returns:
    - output_folder_path: The path to the output folder.
    - temp_dir: The path to the temporary directory.
    """
    relative_folder_path_of_file = os.path.split(file_path.split(input_dir)[1])[0]

    file_name = os.path.split(file_path)[1]

    output_folder_name_mcap, extension = os.path.splitext(file_name)

    relative_folder_path_of_file = relative_folder_path_of_file.lstrip("/")
    temp_dir = str(tempfile.TemporaryDirectory().name)

    output_folder_path = os.path.join(
        temp_dir,
        ".VISUALIZATION_ASSETS",
        relative_folder_path_of_file,
        output_folder_name_mcap,
    )

    print(f"Output folder path: {output_folder_path}")
    os.makedirs(output_folder_path, exist_ok=True)

    return output_folder_path, temp_dir


def create_topic(
    topic_association: Association,
    org_id: str,
    topic_name: str,
    message_path_requests,
    nr_msgs: int,
    first_timestamp: int,
    last_timestamp: int,
    msgtype: Optional[str]=None,
    schema_checksum: Optional[str]=None,
) -> Topic:
    """
    Create a new topic or get an existing one.

    Args:
        topic_association: Topic association object.
        org_id: Organization ID.
        topic_name: Topic name.
        message_path_requests: Message path requests.
        nr_msgs: Number of messages.
        first_timestamp: First timestamp of the messages.
        last_timestamp: Last timestamp of the messages.
        msgtype: Message type string. Optional.
        schema_checksum: SHA-256 checksum of the json schema. Optional

    Returns:
        topics.Topic: The created or retrieved topic.
    """
    try:
        topic = Topic.create(
                topic_name=topic_name,
                file_id=topic_association.association_id,
                schema_name=msgtype,
                schema_checksum=schema_checksum,
                start_time=first_timestamp,
                end_time=last_timestamp,
                message_paths=message_path_requests,
                caller_org_id=org_id
        )
    except RobotoConflictException:
        topic = Topic.from_name_and_file(
            topic_name=topic_name,
            file_id=topic_association.association_id,
            owner_org_id=org_id,
        )
        print(f"Topic already exists: {topic_name}")

    return topic


def set_default_representation(
    topic: Topic,
        topic_name: str,
        file_id: str,
) -> None:
    """
    Set the default representation for a topic.

    Args:
        topic: Topic object.
        topic_name: Topic name.
        file_id: File ID of the MCAP file.
    """
    try:
        topic.set_default_representation(
                association=Association(
                    association_type=AssociationType.File,
                    association_id=file_id
                ),
                storage_format=RepresentationStorageFormat.MCAP,
                version=1,
        )
    except RobotoConflictException:
        print(
            f"Conflict exception while setting default representation for topic: {topic_name}"
        )


def setup_logger(logger_name: str, print_to_console: bool = True, print_to_file: bool = False):
    """
    Set up the logger for the action.

    Returns:
    - None
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers
    logger.handlers = []

    if print_to_file:
        try:
            action_runtime = ActionRuntime.from_env()
            output_dir = action_runtime.output_dir
            invocation_id = action_runtime.invocation_id

        except ActionRuntimeException:
            output_dir = pathlib.Path.cwd()
            invocation_id = "local"

        log_file = (
                pathlib.Path(output_dir)
                / ".metrics"
                / f"process_timing_{invocation_id}.csv"
        )
        log_file.parent.mkdir(parents=True, exist_ok=True)
        # File handler
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    if print_to_console:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger


def compute_checksum(json_schema) -> str:
    """
    Computes the SHA-256 checksum of a given JSON schema.

    This function serializes the JSON schema, sorts its keys for consistency,
    and then computes the SHA-256 checksum of the serialized data.

    Args:
    - json_schema: A dictionary representing the JSON schema.

    Returns:
    - The SHA-256 checksum of the serialized JSON schema as a hexadecimal string.
    """
    serialized_schema = json.dumps(json_schema, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized_schema).hexdigest()


