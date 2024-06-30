import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

class FreeSpacesNamesScreen extends StatefulWidget {
  @override
  _FreeSpacesNamesScreenState createState() => _FreeSpacesNamesScreenState();
}

class _FreeSpacesNamesScreenState extends State<FreeSpacesNamesScreen> {
  List<String> freeSpacesNames = [];
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    fetchParkingSpacesNames();
    _timer = Timer.periodic(Duration(seconds: 3), (timer) {
      fetchParkingSpacesNames();
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  Future<void> fetchParkingSpacesNames() async {
    final response = await http.get(Uri.parse('http://192.168.162.198:5000/get_spaces'));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      setState(() {
        freeSpacesNames = List<String>.from(data['free_spaces_names']);
      });
    } else {
      throw Exception('Failed to load parking spaces data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Names of Empty Parking Spaces'),
        titleTextStyle: TextStyle(color: Colors.white, fontSize: 20,),
        backgroundColor: const Color.fromARGB(255, 8, 62, 106),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: ListView.builder(
          itemCount: freeSpacesNames.length,
          itemBuilder: (context, index) {
            return ListTile(
              title: Text(freeSpacesNames[index]),
            );
          },
        ),
      ),
    );
  }
}