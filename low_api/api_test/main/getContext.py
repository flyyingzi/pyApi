
from getCommond import GetCommond

class GetContext:

    def __init__(self):
        self.get_Commond = GetCommond()
        self.commond = self.json.getCommond() 

    def reContext(self):
        yl_name = self.get_Commond.get_commond_name(self.commond)
        returnG = self.get_Commond.get_commond_Return(self.commond)
        context = self.get_Commond.get_commond_Context(self.commond)

        
