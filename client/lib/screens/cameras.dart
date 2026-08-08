import 'package:flutter/material.dart';

class Cameras extends StatelessWidget {
  const Cameras({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsetsGeometry.all(8.0),
          child: Text("Cameras", textAlign: TextAlign.center),
        ),
      ],
    );
  }
}
