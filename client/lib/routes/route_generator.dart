import 'package:flutter/material.dart';
import 'package:pisec_client/main.dart';

class RouteGenerator {
  final List<Widget> mainPages;

  const RouteGenerator({required this.mainPages});

  Route<dynamic> generateRoutes(RouteSettings settings) {
    final args = settings.arguments;
    switch (settings.name) {
      case '/':
        if (args == null) {
          return _homePageRoute();
        }
        if (args is int && args >= 0 && args < 3) {
          return _homePageRoute(pageIdx: args);
        }
        return _errorRoute(message: "Args for home page must be int or empty");
      case '/videos':
        return _homePageRoute(pageIdx: 0);
      case '/cameras':
        return _homePageRoute(pageIdx: 1);
      case '/settings':
        return _homePageRoute(pageIdx: 2);
      case '/unfinished':
        return _unfinishedRoute();
      default:
        return _errorRoute(message: "Invalid page route");
    }
  }

  Route<dynamic> _errorRoute({String message = "Error has occured"}) {
    return MaterialPageRoute(
      builder: (_) {
        return Scaffold(
          appBar: AppBar(title: Text("Error")),
          body: Center(child: Text(message)),
        );
      },
    );
  }

  Route<dynamic> _unfinishedRoute() {
    return MaterialPageRoute(
      builder: (_) => Scaffold(
        appBar: AppBar(title: Text("Unfinished page")),
        body: Center(child: Text("This page is unfinished")),
      ),
    );
  }

  Route<dynamic> _homePageRoute({int pageIdx = 0}) {
    return MaterialPageRoute(
      builder: (_) => MyHomePage(
        title: 'Pisec Home',
        pages: mainPages,
        initPageIndex: pageIdx,
      ),
    );
  }
}
