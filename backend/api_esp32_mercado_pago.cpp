#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// MercadoPago API details
const char* mercadopagoApiUrl = "https://api.mercadopago.com/v1/payments";
const char* accessToken = "TEST-4398345889891464-091700-8613ae160df3f80b73b46f43616b3237-495427135";

// Model
class PaymentModel {
public:
  String id;
  float amount;
  String status;

  PaymentModel() : amount(0.0) {}
};

// View (simplified for ESP32)
class PaymentView {
public:
  void displayPaymentStatus(const PaymentModel& payment) {
    Serial.println("Payment Status:");
    Serial.print("ID: ");
    Serial.println(payment.id);
    Serial.print("Amount: ");
    Serial.println(payment.amount);
    Serial.print("Status: ");
    Serial.println(payment.status);
  }
};

// Controller
class PaymentController {
private:
  PaymentModel model;
  PaymentView view;
  
public:
  PaymentController() {}

  bool createPayment(float amount) {
    HTTPClient http;
    http.begin(mercadopagoApiUrl);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("Authorization", "Bearer " + String(accessToken));

    StaticJsonDocument<200> doc;
    doc["transaction_amount"] = amount;
    doc["description"] = "Product description";
    doc["payment_method_id"] = "pix";
    doc["payer"]["email"] = "test@test.com";

    String requestBody;
    serializeJson(doc, requestBody);

    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode > 0) {
      String response = http.getString();
      
      DynamicJsonDocument responseDoc(1024);
      deserializeJson(responseDoc, response);

      model.id = responseDoc["id"].as<String>();
      model.amount = responseDoc["transaction_amount"].as<float>();
      model.status = responseDoc["status"].as<String>();

      view.displayPaymentStatus(model);
      return true;
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
      return false;
    }
  }

  bool checkPaymentStatus(const String& paymentId) {
    HTTPClient http;
    String url = String(mercadopagoApiUrl) + "/" + paymentId;
    http.begin(url);
    http.addHeader("Authorization", "Bearer " + String(accessToken));

    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      String response = http.getString();
      
      DynamicJsonDocument responseDoc(1024);
      deserializeJson(responseDoc, response);

      model.id = responseDoc["id"].as<String>();
      model.amount = responseDoc["transaction_amount"].as<float>();
      model.status = responseDoc["status"].as<String>();

      view.displayPaymentStatus(model);
      return true;
    } else {
      Serial.print("Error on sending GET: ");
      Serial.println(httpResponseCode);
      return false;
    }
  }
};

PaymentController paymentController;

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Create a payment
  if (paymentController.createPayment(100.0)) {
    Serial.println("Payment created successfully");
  } else {
    Serial.println("Failed to create payment");
  }
}

void loop() {
  // You can add code here to periodically check payment status
  delay(5000);
}