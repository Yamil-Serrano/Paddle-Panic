# Paddle Panic 

## 🎮 About
This project was inspired by a friend who was taking an introduction to programming class. After helping him develop a basic Pong game for his course, I became interested in the concept and decided to create my first version based on the structure of his code. From there, I expanded the idea by adding a CPU-controlled opponen and sound effects to enhance the gameplay experience. To ensure smooth performance across different screen refresh rates, I implemented delta time physics.

## ✨ Features
- Adaptive ball physics using delta time for smooth gameplay on different frame rates
- AI-controlled opponent with dynamic movement
- Collision detection with paddles and walls
- Impact sounds for paddle hits, wall bounces, and scoring
- Score tracking and automatic resets after a point is scored
- FPS counter for debugging

## 🛠️ Installation & Running the Game
### Prerequisites
- Python 3.x
- Pygame (install using `pip install pygame`)

### Running the Game
1. Clone this repository:
   ```sh
   git clone https://github.com/Yamil-Serrano/paddle-panic.git
   ```
2. Navigate to the project directory:
   ```sh
   cd paddle-panic
   ```
3. Run the game:
   ```sh
   python paddle_panic.py
   ```

## 🕹️ Controls
- **Arrow Up (↑)**: Move paddle up
- **Arrow Down (↓)**: Move paddle down
- **Spacebar**: Start the ball movement

## 🔊 Sound Effects
The game includes sound effects for:
- Paddle hits
- Wall bounces
- Scoring points

If you want to replace or disable sounds, modify the `pygame.mixer.Sound()` calls in the script.

## License
This project is open-source and available under the MIT License.

---
Happy playing! 🏓

