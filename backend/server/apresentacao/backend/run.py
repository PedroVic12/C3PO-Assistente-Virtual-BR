import sys
from converters.factory import ConverterFactory

class PresentationFacade:
    def __init__(self):
        self.factory = ConverterFactory()

    def generate(self, formats):
        if 'all' in formats:
            formats = ['pdf', 'pptx', 'video']
        
        for fmt in formats:
            try:
                converter = self.factory.get_converter(fmt)
                converter.convert()
            except Exception as e:
                print(f"❌ Erro ao converter para {fmt}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        formats_to_generate = sys.argv[1:]
        facade = PresentationFacade()
        facade.generate(formats_to_generate)
    else:
        print("Uso: python run.py [pdf|pptx|video|all]")
