import 'package:flutter/material.dart';
import 'package:parking_lotttttt/free_spaces_count_screen.dart';
import 'package:parking_lotttttt/free_spaces_names_screen.dart';
import 'package:parking_lotttttt/plate_difference_screen.dart';

class MainMenuScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text('Main Menu'),
        titleTextStyle: TextStyle(color: Colors.white, fontSize: 20,),
        backgroundColor: const Color.fromARGB(255, 8, 62, 106),
        leading: Padding(
          padding: const EdgeInsets.only(left: 1.0),
          child: Image.asset('logo.png'), 
        )
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
              child: MenuButton(
                label: 'Names of Empty Parking Spaces',
                navigateTo: FreeSpacesNamesScreen(),
                hoverImage: 'assets/ilk_foto.jpg', // Add the path to your image
                icon: Icons.format_list_numbered, // Different icon for this button
              ),
            ),
            Expanded(
              child: MenuButton(
                label: 'Number of Empty Parking Spaces',
                navigateTo: FreeSpacesCountScreen(),
                hoverImage: 'assets/ikinci.jpg', // Add the path to your image
                icon: Icons.location_on, // Different icon for this button
              ),
            ),
            Expanded(
              child: MenuButton(
                label: 'Plate Name and Parking Location',
                navigateTo: PlateDifferencesScreen(),
                hoverImage: 'assets/ucuncu.jpeg', // Add the path to your image
                icon: Icons.directions_car, // Different icon for this button
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class MenuButton extends StatefulWidget {
  final String label;
  final Widget navigateTo;
  final String hoverImage;
  final IconData icon; // Added icon parameter

  MenuButton({
    required this.label,
    required this.navigateTo,
    required this.hoverImage,
    required this.icon, // Added icon parameter
  });

  @override
  _MenuButtonState createState() => _MenuButtonState();
}

class _MenuButtonState extends State<MenuButton> {
  bool _isHovered = false;
  bool _isClicked = false;

  @override
  Widget build(BuildContext context) {
    double scale = 1.0;
    if (_isHovered) {
      scale = 1.1;
    }
    if (_isClicked) {
      scale = 1.2;
    }

    return MouseRegion(
      onEnter: (_) => setState(() => _isHovered = true),
      onExit: (_) => setState(() => _isHovered = false),
      child: Stack(
        children: [
          Positioned.fill(
           child: AnimatedOpacity(
              opacity: _isClicked ? 1.0 : 0.5, // Set to 1.0 when clicked, 0.5 otherwise
              duration: Duration(milliseconds: 300),
              child: Image.asset(
                widget.hoverImage,
                fit: BoxFit.cover,
              ),
            ),
          ),
          Center(
            child: AnimatedScale(
              scale: scale,
              duration: Duration(milliseconds: 100),
              child: PrettyShadowButton(
                label: widget.label,
                onPressed: () async {
                  setState(() => _isClicked = true);
                  await Future.delayed(Duration(milliseconds: 200));
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => widget.navigateTo),
                  ).then((_) => setState(() => _isClicked = false));
                },
                icon: widget.icon,
                shadowColor: const Color.fromARGB(255, 8, 62, 106),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class PrettyShadowButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final IconData icon;
  final Color shadowColor;

  PrettyShadowButton({
    required this.label,
    required this.onPressed,
    required this.icon,
    required this.shadowColor,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: onPressed,
      icon: Icon(icon),
      label: Text(label),
      style: ButtonStyle(
        shadowColor: MaterialStateProperty.all(shadowColor),
        elevation: MaterialStateProperty.all(10),
        backgroundColor: MaterialStateProperty.resolveWith<Color>(
          (Set<MaterialState> states) {
            if (states.contains(MaterialState.pressed)) {
              return Color.fromARGB(255, 8, 62, 106);
            } else if (states.contains(MaterialState.hovered)) {
              return Colors.grey[300]!;
            }
            return Colors.white; // Default color
          },
        ),
        foregroundColor: MaterialStateProperty.all(Colors.black),
      ),
    );
  }
}

void main() => runApp(MaterialApp(home: MainMenuScreen()));
