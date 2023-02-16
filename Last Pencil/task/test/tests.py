from hstest import *
import re


class LastPencilTest(StageTest):
    @dynamic_test()
    def CheckOutput(self):
        main = TestedProgram()
        output = main.start().lower()
        lines = output.strip().split('\n')
        if len(lines) != 1 or "how many pencils" not in output:
            raise WrongAnswer("When the game starts, it should output only one line asking the user about the amount "
                              "of pencils they would like to use with the \"How many pencils\" string")

        output2 = main.execute("1")
        output2 = output2.replace(" ", "")
        pattern = re.compile(".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)")
        if len(output2.split()) != 1:
            raise WrongAnswer("When the user replies with the amount of pencils, the game should print 1 non-empty "
                              "line asking who will be the first player.\n"
                              f"{len(output2.split())} lines were found in the output.")
        if not re.match(pattern, output2):
            raise WrongAnswer("When the user replies with the amount of pencils, the game should ask who will"
                              " be the first player ending with the \"(\"Name1\", \"Name2\")\" string.")
        return CheckResult.correct()

    data = ["a", "_", "test", "|", "|||||", " ", "-", "two", "10g", "k5", "-0.2", "0.3"]

    @dynamic_test(data=data)
    def CheckNumericAmount(self, inp):
        main = TestedProgram()
        main.start()

        output = main.execute(inp).lower()

        if ("number of pencils" not in output) or ("numeric" not in output):
            raise WrongAnswer("When the user provides the number of pencils as a non-numeric sequence, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again "
                              "with the \"The number of pencils should be numeric\" string.")
        for i in range(1, 5):
            output = main.execute(inp).lower()
            if ("number of pencils" not in output) or ("numeric" not in output):
                raise WrongAnswer("When the user provides the number of pencils as a non-numeric sequence, the game should "
                                  "inform the user that their input is incorrect and prompt the user for input again "
                                  "with the \"The number of pencils should be numeric\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckNotZeroAmount(self):
        main = TestedProgram()
        main.start()
        output = main.execute("0").lower()

        if ("number of pencils" not in output) or ("positive" not in output):
            raise WrongAnswer("When the user provides \"0\" as a number of pencils, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again "
                              "with the \"The number of pencils should be positive\" string.")
        for i in range(1, 5):
            output = main.execute("0").lower()
            if ("number of pencils" not in output) or ("positive" not in output):
                raise WrongAnswer("When the user provides \"0\" as a number of pencils, the game should "
                                  "inform the user that their input is incorrect and prompt the user for input again "
                                  "with the \"The number of pencils should be positive\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckBothAmount(self):
        main = TestedProgram()
        main.start()

        output = main.execute("0").lower()
        if ("number of pencils" not in output) or ("positive" not in output):
            raise WrongAnswer("When the user provides \"0\" as a number of pencils, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again "
                              "with the \"The number of pencils should be positive\" string.")
        output = main.execute("a").lower()
        if ("number of pencils" not in output) or ("numeric" not in output):
            raise WrongAnswer("When the user provides the number of pencils as a non-numeric sequence, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again "
                              "with the \"The number of pencils should be numeric\" string.")
        output = main.execute("0").lower()
        if ("number of pencils" not in output) or ("positive" not in output):
            raise WrongAnswer("When the user provides \"0\" as a number of pencils, the game should "
                              "inform the user that their input is incorrect and prompt the user for input again "
                              "with the \"The number of pencils should be positive\" string.")
        output2 = main.execute("1")
        output2 = output2.replace(" ", "")
        pattern = re.compile(".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)")
        if not re.match(pattern, output2):
            raise WrongAnswer("When the user inputs the number of pencils correctly, the game should ask who will "
                              "be the first player ending with the \"(\"Name\", \"Name2\")\" string.")
        return CheckResult.correct()

    test_data = [
        [5, 1, [2, 1], 2, ["4", "a", "0", "-1", "_", "|", "|||||"], 2],
        [20, 1, [3, 2, 3, 1, 2, 3, 3, 2], 1, ["4", "a", "0", "-1", "_", "|", "|||||"], 2],
        [30, 1, [3, 2, 3, 1, 2, 3, 3, 3, 2, 3, 3], 2, ["4", "a", "0", "-1", "_", "|", "|||||"], 1],
        [5, 2, [2, 1], 2, ["4", "a", "0", "-1", "_", "|", "|||||"], 1],
        [20, 2, [3, 2, 3, 1, 2, 3, 3, 2], 1, ["4", "a", "0", "-1", "_", "|", "|||||"], 1],
        [30, 2, [3, 2, 3, 1, 2, 3, 3, 3, 2, 3, 3], 2, ["4", "a", "0", "-1", "_", "|", "|||||"], 2],
    ]

    @dynamic_test(data=test_data)
    def CheckGame(self, amount, first, moves, last, incorrect, winner):
        main = TestedProgram()
        main.start()

        output = main.execute(str(amount))
        output = output.replace(" ", "")

        if "who" not in output.lower() or 'first' not in output.lower():
            raise WrongAnswer("The game should ask the user to input the player that goes first.")

        leftName = output[output.rfind('(') + 1:output.rfind(',')]
        rightName = output[output.rfind(',') + 1:output.rfind(')')]

        prevPlayer = ""
        nextPlayer = ""
        if first == 1:
            prevPlayer = leftName
            nextPlayer = rightName
        else:
            prevPlayer = rightName
            nextPlayer = leftName

        output2 = main.execute(leftName+rightName).lower()

        if ("choose between" not in output2) or (leftName.lower() not in output2) or (rightName.lower() not in output2):
            raise WrongAnswer(f"When the user provides a name that is not '{leftName}' or '{rightName}', "
                              f"the game should inform the user that their input is incorrect "
                              f"and prompt the user for input again "
                              f"with the \"Choose between '{leftName}' and '{rightName}'\" string.")
        for i in range(1, 5):
            output2 = main.execute(leftName+rightName).lower()
            if ("choose between" not in output2) or (leftName.lower() not in output2) or (rightName.lower() not in output2):
                raise WrongAnswer(f"When the user provides a name that is not '{leftName}' or '{rightName}', "
                                  f"the game should inform the user that their input is incorrect "
                                  f"and prompt the user for input again "
                                  f"with the \"Choose between '{leftName}' and '{rightName}'\" string.")
        output3 = main.execute(prevPlayer).lower()

        lines = output3.strip().split('\n')
        linesNonEmpty = [s for s in lines if len(s) != 0]

        if len(linesNonEmpty) != 2:
            raise WrongAnswer("When the player provides the initial game conditions"
                              ", your program should print 2 non-empty lines:\n"
                              "one with with vertical bar symbols representing the number of pencils, "
                              "the other with the \"*NameX* turn\" string.\n"
                              f"{len(linesNonEmpty)} lines were found in the output.")

        checkPencils = [s for s in lines if '|' in s]
        if len(checkPencils) == 0:
            raise WrongAnswer("When the player provides the initial game conditions"
                              ", your program should print one line with several vertical bar "
                              "symbols ('|') representing pencils.")
        if len(checkPencils) > 1:
            raise WrongAnswer("When the player provides the game initial conditions"
                              ", your program should print only one line with several vertical bar "
                              "symbols ('|') representing pencils.")
        if len(list(set(checkPencils[0]))) != 1:
            raise WrongAnswer("The line with pencils should not contain any symbols other than the '|' symbol.")

        if len(checkPencils[0]) != int(amount):
            raise WrongAnswer("The line with pencils should contain as many '|' symbols as the player provided.")

        checkTurn = any((prevPlayer.lower() in s) and ("turn" in s) for s in lines)

        if not checkTurn:
            raise WrongAnswer(f"When the player provides the initial game conditions"
                              f" there should be a line in output that contains the \"{prevPlayer}\'s turn\""
                              f" string if {prevPlayer} is the first player.")

        onTable = amount

        for i in moves:
            for j in incorrect:
                output = main.execute(j).lower()
                if ("possible values" not in output) or ('1' not in output) or ('2' not in output) or ('3' not in output) :
                    raise WrongAnswer(f"If the player enters values different from"
                                      f" '1', '2', or '3', the game should inform the user that "
                                      f"their input is incorrect and prompt the user for input again"
                                      f" with the \"Possible values: '1', '2', '3'\" string.")
            onTable -= i
            output = main.execute(str(i)).lower()
            lines = output.strip().split('\n')
            linesNonEmpty = [s for s in lines if len(s) != 0]

            if len(linesNonEmpty) != 2:
                raise WrongAnswer("When one of the players enters the number of pencils they want to remove"
                                  ", the program should print 2 non-empty lines.")

            checkPencils = [s for s in lines if '|' in s]
            if len(checkPencils) == 0:
                raise WrongAnswer("When one of the players enters the amount of pencils they want to remove"
                                  ", your program should print one line with vertical bar symbols ('|') representing "
                                  "pencils.")
            if len(checkPencils) > 1:
                raise WrongAnswer("When one of the players enters the amount of pencils they want to remove"
                                  ", your program should print only one line with vertical bar symbols ('|') "
                                  "representing pencils.")
            if len(list(set(checkPencils[0]))) != 1:
                raise WrongAnswer("The line with pencils should not contain any symbols other than the '|' symbol.")

            if len(checkPencils[0]) != onTable:
                raise WrongAnswer("When one of the players enters the amount of pencils they want to remove, "
                                  "the line with pencils should contain as many '|' symbols as there are pencils left.")

            checkTurn = any((nextPlayer.lower() in s) and ("turn" in s) for s in lines)

            if not checkTurn:
                raise WrongAnswer(f"When {prevPlayer} enters the amount of pencils they want to remove"
                                  f" there should be a line in output that contains \"{nextPlayer} turn\".")
            prevPlayer, nextPlayer = nextPlayer, prevPlayer

        output = main.execute(str(last+1)).lower()
        if ("too many" not in output) or ('pencils' not in output):
            raise WrongAnswer("If the player enters the number of pencils that is greater than the current "
                              "number of pencils on the table, the game should inform the user that "
                              "their input is incorrect and prompt the user for input again "
                              "with the \"too many pencils\" string.")

        output = main.execute(str(last)).lower()
        lines = output.strip().split('\n')
        linesNonEmpty = [s for s in lines if len(s) != 0]

        winnerName = ""

        if winner == 1:
            winnerName = leftName
        if winner == 2:
            winnerName = rightName

        if len(linesNonEmpty) != 1 or (winnerName.lower() not in linesNonEmpty[0]) or ('win' not in linesNonEmpty[0] and 'won' not in linesNonEmpty[0]):
            if len(linesNonEmpty) >= 1:
                if winnerName.lower() not in linesNonEmpty[0] and (
                        'win' in linesNonEmpty[0] or 'won' in linesNonEmpty[0]):
                    raise WrongAnswer("Make sure you determined the winner of the game correctly.\n"
                                      "The player who takes the last pencil loses the game.")
            raise WrongAnswer("When the last pencil is taken, the program should print one line that informs "
                              "who is the winner in this game with \"*Name*\" and \"win\"/\"won\" strings.")

        if not main.is_finished():
            raise WrongAnswer("Your program should not request anything when there are no pencils left.")
        return CheckResult.correct()


if __name__ == '__main__':
    LastPencilTest().run_tests()
