import 'dart:io';
import 'dart:convert' as convert;

void main() async {
  HttpServer.bind("0.0.0.0", 5001).then((HttpServer server) {
    print("Listening on " +
        server.address.address +
        ":" +
        server.port.toString() +
        "/");
    server.listen((HttpRequest req) {
      print("Request:  " + req.requestedUri.toString());
      Map resp_map;
      try {
        // Gather our data
        String mark_1 = req.requestedUri.queryParameters['mark_1'];
        String mark_2 = req.requestedUri.queryParameters['mark_2'];
        String mark_3 = req.requestedUri.queryParameters['mark_3'];
        String mark_4 = req.requestedUri.queryParameters['mark_4'];
        String mark_5 = req.requestedUri.queryParameters['mark_5'];

        var lst_marks = [mark_1, mark_2, mark_3, mark_4, mark_5];
        double marks_av = totalMarks(lst_marks) / 5;
        resp_map = {
          'grade_1': determineGrade(mark_1),
          'grade_2': determineGrade(mark_2),
          'grade_3': determineGrade(mark_3),
          'grade_4': determineGrade(mark_4),
          'grade_5': determineGrade(mark_5),
          'overall_grade': determineGrade(marks_av.toString())
        };
      } catch (e) {
        resp_map = {'error_msg': "An unexpected error has occurred"};
      }
      // Build our Response
      req.response.headers.set('Content-type', 'application/json');
      req.response.headers.set('Access-Control-Allow-Origin', '*');
      req.response.write(convert.jsonEncode(resp_map));
      req.response.close();
    });
  });
  print("Connection lost");
}

int totalMarks(var marks) {
  int totalMarks = 0;
  for (var mark in marks) {
    totalMarks = totalMarks + int.parse(mark);
  }
  return totalMarks;
}

String determineGrade(String mark) {
  double markI = double.parse(mark);
  if (markI >= 80) {
    return "Distinction";
  } else if (markI >= 70) {
    return "Commendation";
  } else if (markI >= 60) {
    return "Pass";
  } else if (markI >= 50) {
    return "Marginal Fail";
  } else if (markI >= 40) {
    return "Fail";
  } else {
    return "Low Fail";
  }
}
