class Deteccion:
    def __init__(self, text):
        self.text = text
        
        print(f"Se ha insertado un nuevo texto: {self.text}")
           
    def info (self):
        print(f"deteccion: {self.text}")    
    
    def __str__(self):
        return f"{self.text}"