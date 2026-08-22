// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:pisec_client/main.dart';
import 'package:pisec_client/models/api/responses/video_response.dart';
import 'package:pisec_client/models/const_datetime.dart';
import 'package:pisec_client/screens/cameras.dart';
import 'package:pisec_client/screens/settings.dart';
import 'package:pisec_client/screens/videos.dart';

void main() {
  testWidgets('Startup smoke test', (WidgetTester tester) async {
    const List<VideoResponse> videos = [
      VideoResponse(1, "test1", 1, ConstDateTime(0)),
      VideoResponse(2, "test2", 1, ConstDateTime(1)),
      VideoResponse(3, "test3", 2, ConstDateTime(0)),
    ];
    const List<Widget> pages = [Videos(videos: videos), Cameras(), Settings()];

    // Must initialise locale before running the app due to date formatting
    initializeDateFormatting("en_GB");

    // Build our app and trigger a frame.
    await tester.pumpWidget(const PisecApp(pages: pages));
  });
}
