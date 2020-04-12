from db.models import ProblemRecored
from db.models import ProblemJudgeResultStatusEnum,ProblemJudgeStatusEnum

def test_case1():
    problem = ProblemRecored()
    print(problem.toString())
    #problem_dict = {'code': '#include <stdio.h>\n int main(){ printf("\n"); }', 'lang': 'c', 'test_cases': [{'input': '1', 'output': '2'}, ], 'notify': 'http://localhost/ok'}
    problem_dict = {'code': '#include <stdio.h>\n int main(){ printf("\n"); }', 'lang': 'c', 'test_cases': [{'input': '1', 'output': '2'}, ], 'notify1': 'http://localhost/ok'}
    problem.updateProblem(problem_dict)
    print(problem.toString())

def test_case2():
    problem = ProblemRecored()
    problem_dict = {'code': '#include <stdio.h>\n int main(){ printf("\n"); }', 'lang': 'c', 'test_cases': [{'input': '1', 'output': '2'}, ], 'notify1': 'http://localhost/ok'}
    problem.updateProblem(problem_dict)

    otherProblem = ProblemRecored()
    otherProblem.fromString(problem.toString())
    print(otherProblem.toString())
    print(otherProblem.problem_judge_result_status_list)
    print(otherProblem.problem_judge_status_list)

def test_case3():
    print(ProblemJudgeResultStatusEnum.AC)
    print(ProblemJudgeStatusEnum.waiting)

if __name__ == "__main__":
    #test_case1()
    #test_case2()
    test_case3()