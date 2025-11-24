// Seleccionar / crear base de datos
use kyc;

// Crear colección si no existe
db.createCollection("verification_logs");

// Insertar datos de prueba
db.verification_logs.insertMany([
  {
    _id: ObjectId("6922baf8d95a14af52222f2d"),
    request_id: "11111111-2222-3333-4444-555555555555",
    score: 85,
    risk_level: "medium",
    rules_triggered: [
      "EMAIL_DOMAIN_RISK"
    ],
    rules_detail: {
      EMAIL_DOMAIN_RISK: {
        email: "test@riskmail.com",
        domain: "riskmail.com",
        is_risky: true
      }
    },
    engine_version: "1.0.0",
    processed_at: ISODate("2025-01-01T00:00:00.000Z"),
    processing_time_ms: 50
  },
  {
    _id: ObjectId("6922baf8d95a14af52222f2e"),
    request_id: "aaaaaaa-cccc-dddd-eeee-ffffffffffff",
    score: 40,
    risk_level: "high",
    rules_triggered: [
      "COUNTRY_RESTRICTED",
      "DOCUMENT_LENGTH_INVALID"
    ],
    rules_detail: {},
    engine_version: "1.0.0",
    processed_at: ISODate("2025-01-01T00:00:00.000Z"),
    processing_time_ms: 80
  }
]);

print("✔ Datos insertados correctamente en kyc.verification_logs");
