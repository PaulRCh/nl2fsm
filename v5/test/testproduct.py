
from test.testmealymachine import *

if __name__ == "__main__":
    mm1= build_machine1()
    affichage.show_mealy_machine(mm1)
    mm2= build_machine2()
    affichage.show_mealy_machine(mm2)
    produit = productalgorithms.ProductMealyMachine(mm1,mm2)
    produit.make_product()
    affichage.show_mealy_machine(produit)
    iseq, path = produit.find_a_path_to_diff_state()
    print(iseq, path)
