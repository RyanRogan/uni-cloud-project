import 'package:test/test.dart';

import 'app.dart' as app;

void main() {
  test('TotalMarks function should return correct value for total marks', () {
    var m = ["10", "10", "10", "50", "50"];
    expect(app.totalMarks(m), 130);
  });

  group("Grade Classifier", () {
    test('Should Return Distinction when grade is greater than or equal to 80',
        () {
      String grade = "80";
      expect(app.determineGrade(grade), "Distinction");
    });
    test('Should Return Commendation when grade is greater than or equal to 70',
        () {
      String grade = "70";
      expect(app.determineGrade(grade), "Commendation");
    });

    test('Should Return Pass when grade is greater than or equal to 60', () {
      String grade = "60";
      expect(app.determineGrade(grade), "Pass");
    });

    test(
        'Should Return Marginal Fail when grade is greater than or equal to 50',
        () {
      String grade = "50";
      expect(app.determineGrade(grade), "Marginal Fail");
    });

    test('Should Return Fail when grade is greater than or equal to 40', () {
      String grade = "40";
      expect(app.determineGrade(grade), "Fail");
    });

    test('Should Return Low Fail when grade is less than 40', () {
      String grade = "25";
      expect(app.determineGrade(grade), "Low Fail");
    });
  });
}
