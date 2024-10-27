from pydifact.segmentcollection import SegmentCollection

class EDIFACTParser:
    
    def parse_file(file_path):
        parsed_data = {}
        with open(file_path, 'r') as file:
            segments = SegmentCollection.from_str(file.read())
        
            for segment in segments.segments:
                if segment.tag in parsed_data:
                    # Converte para lista se já existe e não é uma lista
                    if not isinstance(parsed_data[segment.tag], list):
                        parsed_data[segment.tag] = [parsed_data[segment.tag]]
                    # Adiciona o segmento à lista
                    parsed_data[segment.tag].append(segment.elements)
                else:
                    parsed_data[segment.tag] = segment.elements

        # Imprime o dicionário completo apenas uma vez após o loop
        return parsed_data
