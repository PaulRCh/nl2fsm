from collections import deque

from mealymachinemodel.mealymachine import MealyMachine
from mealymachinemodel.state import State
from mealymachinemodel.transition import Transition


class ProductState(State):
    state1 : State
    state2 : State
    pair_id : str
    diff : bool

    def __init__(self, e1:State, e2:State, diff=False):
        super().__init__(f'{e1.get_id()}.{e2.get_id()}')
        self.state1 = e1
        self.state2 = e2
        self.pair_id=-1
        self.diff=diff
        d = 1 if self.diff else 0
        self.set_name(self.get_name()+'.'+ str(d))

    def get_pair_id(self)->str:
        return self.pair_id

    def set_pair_id(self, p_id:str):
        self.pair_id =p_id


class ProductMealyMachine(MealyMachine) :
    diff_states_id : set
    machine1 : MealyMachine
    machine2 : MealyMachine
    pairedid_to_id : dict #[pair_id:id]
    # diff_transitions_m1 : list
    # diff_transitions_m2 : list

    def __init__(self, mm1: MealyMachine, mm2: MealyMachine):
        super().__init__(mm1.input_alphabet,mm1.output_alphabet)
        self.machine1=mm1
        self.machine2=mm2
        self.pairedid_to_id =dict()
        self.diff_states_id = set()
        # self.diff_transitions_m1 = list()
        # self.diff_transitions_m2 = list()

    @staticmethod
    def build_pair_id(e1:State, e2:State, diff=False)->str:
        d = 1 if diff else 0
        return str(e1.get_id())+'.'+str(e2.get_id())+'.'+str(d)

    def _determine_and_add_next_state(self,  tr1:Transition, tr2: Transition) -> Transition:
        tgt1, tgt2 = tr1.get_tgt(), tr2.get_tgt()
        output1, output2 = tr1.get_output(), tr2.get_output()
        # retrouver l'état cible dans le produit ou le crée s'il
        # n'existe pas encore
        # if (output1 == output2) :
        #     output = output1
        # else :
        #     output = f'{output1}.{output2}'
        #     self.diff_transitions_m1.append(tr1)
        #     self.diff_transitions_m2.append(tr2)
        output = output1 if (output1 == output2) else f'{output1}.{output2}'
        diff =  False if (output1 ==output2)  else  True
        pairid_tgt = ProductMealyMachine.build_pair_id(tgt1,tgt2,diff)
        if pairid_tgt in self.pairedid_to_id:
            id_tgt = self.pairedid_to_id[pairid_tgt]
            tgt = self.get_state(id_tgt)
        else :
            tgt = self.add_state(ProductState(tgt1,tgt2,diff))
            tgt.set_pair_id(pairid_tgt)
            self.pairedid_to_id[pairid_tgt] = tgt.get_id()


        return tgt, output, diff



    def make_product(self):
        #initialisation
        src = ProductState(self.machine1.get_initial_state(),
                                   self.machine2.get_initial_state())
        src = self.add_state(src)
        self.set_initial_state(src.get_id())
        pairid_src = ProductMealyMachine.build_pair_id(src.state1, src.state2)
        src.set_pair_id(pairid_src)
        self.pairedid_to_id[pairid_src] = src.get_id()
        #
        aVisiter = deque()
        dejaVisite = list() #
        aVisiter.append(src)
        while len(aVisiter) > 0 :
            src = aVisiter.popleft()
            dejaVisite.append(src)
            src1, src2 = src.state1, src.state2
            for a in self.input_alphabet :
                trs1, trs2 = src1.get_out_transition(a), src2.get_out_transition(a)
                for tr1 in trs1:
                    for tr2 in trs2 :
                        tgt, output, diff = self._determine_and_add_next_state(tr1,tr2)
                        #ajout de la transition
                        tr = self.add_transition(src.get_id(), a, output, tgt.get_id())
                        if diff==True :
                            self.diff_states_id.add(tr.get_tgt().get_id())
                        if (tr.get_tgt() not in dejaVisite) \
                                and (tr.get_tgt() not in aVisiter) :
                            aVisiter.append(tr.get_tgt())
        return self

    def find_a_path_to_diff_state(self) :
        return self.find_a_path_to_one_state_in(self.diff_states_id)
    
    def get_wrong_transitions(self):
        exclusive_m1_tr = list()
        exclusive_m2_tr = list()
        diff = True
        m1_tr = self.machine1.get_transitions()
        m2_tr = self.machine2.get_transitions()
        for tr1 in m1_tr:
            for tr2 in m2_tr:
                if tr1.get_src().get_id() == tr2.get_src().get_id() and tr1.get_input() == tr2.get_input() and tr1.get_output() == tr2.get_output() and tr1.get_tgt().get_id() == tr2.get_tgt().get_id():
                    diff = False
                    break
            if diff:
                exclusive_m1_tr.append(tr1)
            diff = True
        for tr2 in m2_tr:
            for tr1 in m1_tr:
                if tr1.get_src().get_id() == tr2.get_src().get_id() and tr1.get_input() == tr2.get_input() and tr1.get_output() == tr2.get_output() and tr1.get_tgt().get_id() == tr2.get_tgt().get_id():
                    diff = False
                    break
            if diff:
                exclusive_m2_tr.append(tr2)
            diff = True
        return exclusive_m1_tr, exclusive_m2_tr
    
    def get_good_transitions(self):
        m2_tr = self.machine2.get_transitions()
        _, wrong_m2 = self.get_wrong_transitions()
        good_m2_tr = list()
        for tr in m2_tr:
            if tr not in wrong_m2:
                good_m2_tr.append(tr)
        return good_m2_tr



        




