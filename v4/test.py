import display.affichage as dis
import prompt as prt


def test_generate_automaton_prompt():
    mm, dot, nl = prt.generate_automaton_prompt(5)
    dis.show_mealy_machine(mm)
    print("nl = \n", nl)

def main():
    test_generate_automaton_prompt()

main()
