from activeinference.observationtable import ObservationTable
from activeinference.teacher import Teacher
from activeinference.learner import Learner
from test import testmealymachine
from display import affichage

oracle = testmealymachine.build_oracle()
teacher = Teacher(oracle)

ia =('a','b')
oa = ('0','1','2')
obstable = ObservationTable(ia,oa,teacher)
mm = obstable.build_hypothesis()
#affichage.show_mealy_machine(mm)

if obstable.isclosed() :
    print("is closed")
else :
    print("not closed")

if obstable.isoutputconsistent() :
    print("output consistent")
else :
    print("non output consistent")

if obstable.istransitionconsistent() :
    print("transition consistent")
else :
    print("non transition consistent")

learner = Learner(ia,oa,teacher)
hypothesis = learner.learn()
#affichage.show_mealy_machine(hypothesis)
