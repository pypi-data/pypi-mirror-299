from pathlib import Path
from roboto_ingestion_utils.image_dir import image_dir_to_mcap
from PIL import Image
import numpy as np
import io

from mcap.reader import make_reader
from mcap_protobuf.decoder import DecoderFactory as DecoderFactory_pb2
from foxglove_schemas_protobuf.CompressedImage_pb2 import CompressedImage as CompressedImage_pb2

from rosbags.image import compressed_image_to_cvimage
from rosbags.typesys import Stores, get_typestore
from rosbags.typesys.stores.latest import sensor_msgs__msg__CompressedImage as CompressedImage_ros2

typestore = get_typestore(Stores.LATEST)

def test_image_dir_to_protobuf_mcap():
    """
    """
    input_dir = Path("./test_inputs/imgs").resolve()
    topic_name = 'imgs'
    output_dir = Path("./output").resolve()
    if not output_dir.exists():
        output_dir.mkdir()

    topic_info_dict, topic_metrics_dict, _, field_type_mappings = image_dir_to_mcap(input_dir=input_dir,
                                                                                    output_dir=output_dir,
                                                                                    timestamp_format="nanoseconds",
                                                                                    frame_rate=10,
                                                                                    start_timestamp=0,
                                                                                    encoding="protobuf")

    topic_entry = topic_info_dict[topic_name]
    mcap_file = Path(topic_entry["mcap_path"])
    assert mcap_file.exists()

    # read protobuf file
    reader = make_reader(open(mcap_file, "rb"), decoder_factories=[DecoderFactory_pb2()]) 

    for schema_, channel_, message_, proto_msg in reader.iter_decoded_messages():
        compressed_img = CompressedImage_pb2()
        compressed_img.ParseFromString(message_.data)

        # smoke test: reading out image
        img_bytes = io.BytesIO(compressed_img.data)
        img = Image.open(img_bytes)
        assert img is not None

    mcap_file.unlink()

def test_image_dir_to_cdr_mcap():
    """
    """
    input_dir = Path("./test_inputs/imgs").resolve()
    topic_name = 'imgs'
    output_dir = Path("./output").resolve()

    if not output_dir.exists():
        output_dir.mkdir()

    topic_info_dict, topic_metrics_dict, _, field_type_mappings = image_dir_to_mcap(input_dir=input_dir,
                                                                                    output_dir=output_dir,
                                                                                    timestamp_format="seconds",
                                                                                    timestamps=[0, 5],
                                                                                    encoding="cdr")

    topic_entry = topic_info_dict[topic_name]
    mcap_file = Path(topic_entry["mcap_path"])
    assert mcap_file.exists()

    reader = make_reader(open(mcap_file, "rb")) 
    # iterate through encoded messages
    for schema, channel, message in reader.iter_messages(topics=[topic_name]):
        print(type(message))
        image_msg = typestore.deserialize_cdr(message.data,
                                              typename=CompressedImage_ros2.__msgtype__)
        cv_image = compressed_image_to_cvimage(image_msg)
        assert cv_image is not None
        assert len(cv_image.shape) == 3

    mcap_file.unlink()


