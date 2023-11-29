import pytest
import main as my_app

def testTotalMarks():
    marks = [5, 2, 4, 5, 6]
    total = my_app.getTotal(marks)
    assert total == 22

def testTotalMarks0():
    marks = []
    total = my_app.getTotal(marks)
    assert total == 0
