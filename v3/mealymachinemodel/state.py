import random


class State(object) :
    _id_in_mealy_machine : int
    _name : str
    _inTransition : dict #{input: list[Transition], }
    _outTransition : dict #{input: list[Transition], }
    def __init__(self, name:str, id = -1):
        self._id_in_mealy_machine = id
        self._name = name
        self._inTransition = dict()
        self._outTransition = dict()

    def __str__(self):
        rst = f'{self._id_in_mealy_machine} [label ="{self._name}"]'
        """rst+='\n Liste de transition sortantes'
        for listeTransition in self._outTransition.values() :
            for tr in listeTransition :
                rst += f'\n {str(tr)}'
        rst+='\n Liste de transition entrantes'
        for listeTransition in self._inTransition.values() :
            for tr in listeTransition :
                rst += f'\n {str(tr)}'
        """
        return rst

    def get_name(self) ->str:
        return self._name

    def set_name(self,name:str):
        self._name =name

    def get_id(self) ->int :
        return self._id_in_mealy_machine
    
    def set_id(self, id:int):
        self._id_in_mealy_machine = id

    def add_out(self,  tr):
        input  = tr.get_input()
        if (input not in self._outTransition.keys()) :
            self._outTransition[input] = []
        self._outTransition[input].append(tr)

    def add_in(self,  tr):
        input  = tr.get_input()
        if (input not in self._inTransition.keys()) :
            self._inTransition[input] = []
        self._inTransition[input].append(tr)

    def get_defined_input(self)->list :
        return list(self._outTransition.keys())

    def get_out_transition(self,input=None):
        if input==None :
            return self._outTransition.values()
        else :
            return self._outTransition[input]

    def get_in_transition(self,input:str):
        return self._inTransition[input]

    def toDot(self) :
         return f's_{self._id_in_mealy_machine} [label="{self._name}" shape="circle"]'

    def toNL(self) :
      descCandidate = [f"state {self._name}",f"{self._name}", f"control state{self._name}", f"location {self._name}"]
      rst = random.choice(descCandidate)
      return rst


