import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

class FreeSpacesCountScreen extends StatefulWidget {
  @override
  _FreeSpacesCountScreenState createState() => _FreeSpacesCountScreenState();
}

class _FreeSpacesCountScreenState extends State<FreeSpacesCountScreen> {
  int freeSpacesCount = 0;
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    fetchParkingSpacesCount();
    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      fetchParkingSpacesCount();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> fetchParkingSpacesCount() async {
    final response = await http.get(Uri.parse('http://192.168.162.198:5000/get_spaces'));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      setState(() {
        freeSpacesCount = data['free_spaces_count'];
      });
    } else {
      throw Exception('Failed to load parking spaces data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Number of Empty Parking Spaces'),
        titleTextStyle: TextStyle(color: Colors.white, fontSize: 20,),
        backgroundColor: const Color.fromARGB(255, 8, 62, 106),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Center(
          child: Text(
            'Number of Empty Parking Spaces: $freeSpacesCount',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }
}