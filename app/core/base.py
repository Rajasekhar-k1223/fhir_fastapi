from abc import ABC,abstractmethod

class FHIRService(ABC):
    @abstractmethod
    def create(self,data:dict):
        pass
    
    @abstractmethod
    def get_by_id(self,resource_id:str):
        pass