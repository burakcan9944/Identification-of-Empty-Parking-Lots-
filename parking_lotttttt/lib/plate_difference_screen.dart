import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

class PlateDifferencesScreen extends StatefulWidget {
  @override
  _PlateDifferencesScreenState createState() => _PlateDifferencesScreenState();
}

class _PlateDifferencesScreenState extends State<PlateDifferencesScreen> {
  String plateName = "";
  String differences = ""; // String olarak güncellendi
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    fetchPlateDifferences();
    _timer = Timer.periodic(Duration(seconds: 3), (timer) {
      fetchPlateDifferences();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> fetchPlateDifferences() async {
    final response = await http.get(Uri.parse('http://192.168.162.198:5000/get_spaces'));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      setState(() {
        plateName = data['plate_name'];
        differences = data['differences']; // difference doğrudan atanır
      });
    } else {
      throw Exception('Failed to load plate differences');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Plate Name and Parking Location'),
        titleTextStyle: TextStyle(color: Colors.white, fontSize: 20,),
        backgroundColor: const Color.fromARGB(255, 8, 62, 106),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            Text(
              '$plateName = $differences', // Veri burada kullanılır
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}