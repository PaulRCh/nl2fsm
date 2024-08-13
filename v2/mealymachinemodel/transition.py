from mealymachinemodel import state
import random

class Transition (object) :
    _id_in_mealy_machine : int
    _src : state.State
    _tgt : state.State
    _input : str
    _output : str
    def __init__(self, src: state.State, input:str, output : str, tgt: state.State):
         self._src = src
         self._tgt = tgt
         self._input = input
         self._output = output
         self._id_in_mealy_machine = -1
         self._src.add_out(self)
         self._tgt.add_in(self)

    def  get_input(self) ->str :
        return self._input

    def  get_output(self) ->str :
        return self._output

    def get_src(self) -> state.State:
        return self._src

    def get_tgt(self) -> state.State:
        return self._tgt

    def set_id(self,id:int):
        self._id_in_mealy_machine = id

    def get_id(self):
        return self._id_in_mealy_machine

    def __str__(self):
         return f'{self._src.get_id()} -- {self._tgt.get_id()} [label="{self._input}/{self._output}"]'

    def toDot(self) -> str :
        rst = "\n\t" + f"s_{self._src.get_id()} -> s_{self._tgt.get_id()}"
        rst+= f'[label="{self._input}/{self._output}"]'
        return rst

    def toNL(self) -> str :
       liste = [f"{self._fromtoNL()} {self._outputtoNL()} and {self._movetoNL()} {self._inputtoNL()}",
                f"{self._outputtoNL()} and {self._movetoNL()} {self._inputtoNL()} {self._fromtoNL()}"]
       rst = random.choice(liste)
       return rst


    def _fromtoNL(self) -> str :
        liste = [f"from {self._src.toNL()}",
                 f"from state {self._src.toNL()}",
                 f"in state {self._src.toNL()}",
                 f"in  {self._src.toNL()}",
                 f"when the system is in {self._src.toNL()}",
                 f"when it is in {self._src.toNL()}"]
        rst = random.choice(liste)
        return rst

    def _movetoNL(self) -> str :
        liste = [f"{self._systemtoNL()} moves to {self._tgt.toNL()}",
                 f"{self._systemtoNL()} reaches {self._tgt.toNL()}",
                 f"{self._tgt.toNL()} is reached"]
        rst = random.choice(liste)
        return rst

    def _systemtoNL(self) ->str :
       liste = ["it", "the system", "the application"]
       rst = random.choice(liste)
       return rst

    def _inputtoNL(self) -> str :
        liste= [f"if the input is {self._input}",
                f"if the input {self._input} occurs",
                f"if  {self._input} occurs",
                f"on occurence of input {self._input}",
                f"on occurence of {self._input}"]
        rst = random.choice(liste)
        return rst

    def _outputtoNL(self) -> str :
        liste= [f"{self._systemtoNL()} produces {self._output}",
                f"{self._systemtoNL()} returns {self._output}",
                f", {self._output} is produced",
                f"the output {self._output} is produced",
                f", {self._output} is returned"]
        rst = random.choice(liste)
        return rst



