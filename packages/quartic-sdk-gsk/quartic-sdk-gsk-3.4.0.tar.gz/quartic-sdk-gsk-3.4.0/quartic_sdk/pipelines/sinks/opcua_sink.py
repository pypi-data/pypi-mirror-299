from .base_sink import SinkApp
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS
from pydantic import BaseModel
import pandas as pd
from opcua import Client
from opcua.ua import DataValue
import time

class OPCUASinkConfig(BaseModel):
    opcua_url: str

class OPCUASinkApp(SinkApp):
    connector_class: str = CONNECTOR_CLASS.OPCUA.value
    connector_config: OPCUASinkConfig

    def __connect_opcua(self):
        try:
            if not hasattr(self, 'client'):
                self.client = Client(self.config.opcua_url)
                self.client.connect()
                print(f"Connected to OPC UA server at {self.config.opcua_url}")
        except Exception as e:
            print(f"Failed to connect to OPC UA server: {str(e)}")
            raise e
    
    def __get_opcua_node(self, node_id: str):
        while True:
            try:
                if not hasattr(self, 'nodes'):
                    self.nodes = {}
                if node_id not in self.nodes:
                    self.nodes[node_id] = self.client.get_node(node_id)
                return self.nodes[node_id]
            except Exception as e:
                print(f"Failed to get OPC UA node {node_id}: {str(e)}")
                self.__connect_opcua()
                time.sleep(self.WAIT_BEFORE_RETRY_SECONDS)
                continue
    
    def validate_transformation_output(**kwargs):
        batch_dict = kwargs['data']
        assert isinstance(batch_dict, dict), "Output of transformation/Input to write_data must be a dictionary"
        for key, value in batch_dict.items():
            assert isinstance(key, str), "Key of the transformation output dictionary must be a string (node id)"
            assert isinstance(value, list), "Values of the transformation output dictionary must be a list (list[DataValue])"
            for data_value in value:
                assert isinstance(data_value, DataValue), "Values of the transformation output dictionary must be a list of DataValue objects"
    
    def write_data(self, batch_dict: dict, spark):
        self.__connect_opcua()
        
        for key, value in batch_dict.items():
            node = self.__get_opcua_node(key)
            for data_value in value:
                while True:
                    try:
                        node.set_value(data_value)
                        print(f"Writing value {value} to OPC UA node {key}")
                    except Exception as e:
                        print(f"Error writing to OPC UA server: {str(e)}")
                        self.__connect_opcua()
                        time.sleep(self.WAIT_BEFORE_RETRY_SECONDS)
                        continue
                    break
