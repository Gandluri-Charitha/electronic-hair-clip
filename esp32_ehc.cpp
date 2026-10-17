#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Big Star position and motion variables
float starX = 64.0;
float starY = 32.0;
float vx = 0.8;
float vy = 0.6;

// Small background stars structure
#define NUM_BACKGROUND_STARS 12
struct BgStar {
  float x, y;
  float speed;
};
BgStar bgStars[NUM_BACKGROUND_STARS];

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // ESP32 I2C pins: SDA=21, SCL=22

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.clearDisplay();

  // Initialize random background stars
  for (int i = 0; i < NUM_BACKGROUND_STARS; i++) {
    bgStars[i].x = random(0, SCREEN_WIDTH);
    bgStars[i].y = random(0, SCREEN_HEIGHT);
    bgStars[i].speed = random(5, 15) / 10.0;
  }
}

// Function to draw the big chubby cute star with anime face
void drawBigCuteStar(int x, int y) {
  // Chubby star body using Adafruit GFX primitives
  display.fillTriangle(x, y - 26, x - 14, y - 3, x + 14, y - 3, SSD1306_WHITE);
  display.fillTriangle(x - 24, y + 20, x - 16, y - 6, x, y + 3, SSD1306_WHITE);
  display.fillTriangle(x + 24, y + 20, x + 16, y - 6, x, y + 3, SSD1306_WHITE);
  display.fillTriangle(x - 30, y - 3, x - 9, y - 11, x - 9, y + 9, SSD1306_WHITE);
  display.fillTriangle(x + 30, y - 3, x + 9, y - 11, x + 9, y + 9, SSD1306_WHITE);
  display.fillCircle(x, y, 13, SSD1306_WHITE);

  // Left Eye & Shine
  display.fillCircle(x - 8, y - 2, 6, SSD1306_BLACK);
  display.drawPixel(x - 10, y - 4, SSD1306_WHITE);
  display.drawPixel(x - 9, y - 4, SSD1306_WHITE);
  display.drawPixel(x - 7, y, SSD1306_WHITE);

  // Right Eye & Shine
  display.fillCircle(x + 8, y - 2, 6, SSD1306_BLACK);
  display.drawPixel(x + 6, y - 4, SSD1306_WHITE);
  display.drawPixel(x + 7, y - 4, SSD1306_WHITE);
  display.drawPixel(x + 9, y, SSD1306_WHITE);

  // Rosy Cheeks
  display.fillCircle(x - 14, y + 5, 2, SSD1306_BLACK);
  display.fillCircle(x + 14, y + 5, 2, SSD1306_BLACK);

  // Smiling Mouth
  display.fillCircle(x, y + 5, 3, SSD1306_BLACK);
  display.fillRect(x - 3, y + 3, 7, 3, SSD1306_WHITE);
}

void loop() {
  display.clearDisplay();

  // 1. Update and draw small background stars to fill empty space
  for (int i = 0; i < NUM_BACKGROUND_STARS; i++) {
    int bx = (int)bgStars[i].x;
    int by = (int)bgStars[i].y;
    display.drawPixel(bx, by, SSD1306_WHITE);
    if (i % 2 == 0) {
      display.drawPixel(bx - 1, by, SSD1306_WHITE);
      display.drawPixel(bx + 1, by, SSD1306_WHITE);
    }

    // Move background stars slowly downwards
    bgStars[i].y += bgStars[i].speed;
    if (bgStars[i].y >= SCREEN_HEIGHT) {
      bgStars[i].y = 0;
      bgStars[i].x = random(0, SCREEN_WIDTH);
    }
  }

  // 2. Draw the big cute star on top
  drawBigCuteStar((int)starX, (int)starY);

  // Update big star motion
  starX += vx;
  starY += vy;

  // Bounce gracefully off the edges
  if (starX <= 32 || starX >= SCREEN_WIDTH - 32) {
    vx *= -1;
  }
  if (starY <= 28 || starY >= SCREEN_HEIGHT - 28) {
    vy *= -1;
  }

  display.display();
  delay(40);
}