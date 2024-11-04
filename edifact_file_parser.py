from pydifact.segmentcollection import Interchange
from typing import Dict, List, Any

class EDIFACTParser:
    
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, List[List[Any]]]:
        parsed_data = {}
        try:
            interchange = Interchange.from_file(file_path)

            for message in interchange.get_messages():
                for segment in message.segments:
                    # Garante que a estrutura de cada tag é uma lista de listas
                    if segment.tag in parsed_data:
                        parsed_data[segment.tag].append(segment.elements)
                    else:
                        parsed_data[segment.tag] = [segment.elements]

        except Exception as e:
            print(f"Error parsing file: {e}")

        return parsed_data
