/*
 * To build this you need to add esp32 by Espressif systems from the Boards
 * Manager of Arduino IDE

 */

#include "WiFi.h"
#include "HTTPClient.h"

/*
 * DallasTemeprature and its dependencies from the 
 * Library Manager (github.com/milesburton/Arduino-Temperature-Control
 * -Library, 3.7.9)
 */

#include <OneWire.h>
#include <DallasTemperature.h>

#define LED_BUILTIN 2

#define ONE_WIRE_BUS 4

# define NODE_ID 1

const char* ssid = "panoulu";

// globals
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

int badHttpResponses = 0;
int sequence = 0;

//
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  Serial.begin(115200);
  
  sensors.begin();
  
  WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(2 * 1000);
    Serial.println("Connecting to panoulu..");
  }

  Serial.println("Connected to panoulu");

  digitalWrite(LED_BUILTIN, LOW);
}

//
void loop() {
  /*
   * Temperature
   */

  sensors.requestTemperatures(); 
  float temperature = sensors.getTempCByIndex(0);
  //Serial.print("Temperature is ");
  //Serial.print(temperature);
  //Serial.println(" C");

  /*
   * Measurement body
   */

  String msg = String("id=") + NODE_ID
    + "&temperature=" + temperature
    + "&millis=" + millis()
    + "&bad_http_responses=" + badHttpResponses;

  /*
   * Http request
   */
  
  HTTPClient http;

  http.begin("http://kahviot-api.sik.fi/v1/metrics/new");
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int resCode = http.POST(msg);

  http.end();

  /*
   * HTTP response and errors
   */

  //Serial.print("Got response: ");
  //Serial.println(resCode);

  if (resCode != 200) {
    badHttpResponses++;
  }

  /*
   * Restart ESP in all sorts of cases :P
   */
  if (resCode == 420 
    || badHttpResponses > 10 
    || WiFi.status() != WL_CONNECTED) {
    delay(120 * 1000);
    ESP.restart();
  }

  delay(10 * 1000);
}
