from fastapi import HTTPException
from pydifact.segmentcollection import SegmentCollection #Interchange
from typing import Dict, List, Any
class EDIFACTParser:
    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        parsed_data = {}
        try:
            with open(file_path, 'r') as file:
                segments = SegmentCollection.from_str(file.read())
            
            for segment in segments.segments:
                if segment.tag in parsed_data:
                    if not isinstance(parsed_data[segment.tag], list):
                        parsed_data[segment.tag] = [parsed_data[segment.tag]]
                    parsed_data[segment.tag].append(segment.elements)
                else:
                    parsed_data[segment.tag] = segment.elements
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing file: {e}")
        
        return parsed_data
# class EDIFACTParser:
    
#     @staticmethod
#     def parse_file(file_path: str) -> Dict[str, List[List[Any]]]:
#         parsed_data = {}
#         try:
#             interchange = Interchange.from_file(file_path)

#             for message in interchange.get_messages():
#                 for segment in message.segments:
#                     # Garante que a estrutura de cada tag é uma lista de listas
#                     if segment.tag in parsed_data:
#                         parsed_data[segment.tag].append(segment.elements)
#                     else:
#                         parsed_data[segment.tag] = [segment.elements]

#         except Exception as e:
#             print(f"Error parsing file: {e}")

#         return parsed_data
