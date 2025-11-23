CREATE TABLE verification_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    country VARCHAR(100) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    document_number VARCHAR(100) NOT NULL,
    document_image_url TEXT,
    selfie_image_url TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    risk_score INTEGER,
    risk_level VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para búsquedas eficientes
CREATE INDEX idx_verification_status ON verification_requests(status);
CREATE INDEX idx_verification_email ON verification_requests(email);
CREATE INDEX idx_verification_created_at ON verification_requests(created_at);



INSERT INTO public.verification_requests
(full_name, email, phone, country, document_type, document_number, document_image_url, selfie_image_url, status, risk_score, risk_level)
VALUES
('Carlos Méndez Ruiz', 'carlos.mendez@example.com', '+5215512341111', 'México', 'INE', 'MDR89012344', 'https://cdn.fake/img/doc1.png', 'https://cdn.fake/img/selfie1.png', 'pending', 12, 'low'),
('Ana Sofía Delgado', 'ana.delgado@example.com', '+573125554444', 'Colombia', 'CC', '1022334455', 'https://cdn.fake/img/doc2.png', 'https://cdn.fake/img/selfie2.png', 'approved', 5, 'low'),
('John Peterson', 'john.peterson@example.com', '+14155551212', 'Estados Unidos', 'Passport', 'US987654321', 'https://cdn.fake/img/doc3.png', 'https://cdn.fake/img/selfie3.png', 'rejected', 78, 'high'),
('María Fernanda López', 'maria.lopez@example.com', '+549112223333', 'Argentina', 'DNI', '40991234', 'https://cdn.fake/img/doc4.png', 'https://cdn.fake/img/selfie4.png', 'pending', 22, 'medium'),
('Luiz Carvalho', 'luiz.carvalho@example.com', '+551199887766', 'Brasil', 'CPF', '23455678901', 'https://cdn.fake/img/doc5.png', 'https://cdn.fake/img/selfie5.png', 'pending', 10, 'low'),
('Sofía Herrera', 'sofia.herrera@example.com', '+5215577744411', 'México', 'Pasaporte', 'GTM1122334', 'https://cdn.fake/img/doc6.png', 'https://cdn.fake/img/selfie6.png', 'approved', 8, 'low'),
('Valentina Paredes', 'valentina.paredes@example.com', '+573004449999', 'Colombia', 'CC', '1009988776', 'https://cdn.fake/img/doc7.png', 'https://cdn.fake/img/selfie7.png', 'pending', 15, 'medium'),
('Eduardo Jiménez', 'eduardo.jimenez@example.com', '+5215588899911', 'México', 'INE', 'JMN09283746', 'https://cdn.fake/img/doc8.png', 'https://cdn.fake/img/selfie8.png', 'rejected', 83, 'high'),
('Patricia Gómez', 'patricia.gomez@example.com', '+34911223344', 'España', 'DNI', '77220011X', 'https://cdn.fake/img/doc9.png', 'https://cdn.fake/img/selfie9.png', 'approved', 3, 'low'),
('Hiroshi Tanaka', 'hiroshi.tanaka@example.com', '+81344556677', 'Japón', 'Passport', 'JP55667788', 'https://cdn.fake/img/doc10.png', 'https://cdn.fake/img/selfie10.png', 'pending', 18, 'medium'),
('Marco Antonio Silva', 'marco.silva@example.com', '+551198887744', 'Brasil', 'RG', '33221444', 'https://cdn.fake/img/doc11.png', 'https://cdn.fake/img/selfie11.png', 'pending', 9, 'low'),
('Emily Johnson', 'emily.johnson@example.com', '+16175551234', 'Estados Unidos', 'Driver License', 'D1234567', 'https://cdn.fake/img/doc12.png', 'https://cdn.fake/img/selfie12.png', 'pending', 29, 'medium'),
('José Luis Castillo', 'joseluis.castillo@example.com', '+5215588771122', 'México', 'INE', 'CLS56788990', 'https://cdn.fake/img/doc13.png', 'https://cdn.fake/img/selfie13.png', 'approved', 6, 'low'),
('Daniela Rivas', 'daniela.rivas@example.com', '+50377889900', 'El Salvador', 'DUI', '04567781-2', 'https://cdn.fake/img/doc14.png', 'https://cdn.fake/img/selfie14.png', 'rejected', 91, 'high'),
('Lucía Martínez', 'lucia.martinez@example.com', '+541155994433', 'Argentina', 'DNI', '44112233', 'https://cdn.fake/img/doc15.png', 'https://cdn.fake/img/selfie15.png', 'pending', 13, 'low'),
('Felipe Andrade', 'felipe.andrade@example.com', '+593998877665', 'Ecuador', 'Cedula', '1723344556', 'https://cdn.fake/img/doc16.png', 'https://cdn.fake/img/selfie16.png', 'pending', 20, 'medium'),
('Thomas Müller', 'thomas.muller@example.com', '+491511223344', 'Alemania', 'Passport', 'DE99887766', 'https://cdn.fake/img/doc17.png', 'https://cdn.fake/img/selfie17.png', 'approved', 4, 'low'),
('Camila Torres', 'camila.torres@example.com', '+5215577553399', 'México', 'INE', 'TRC55667788', 'https://cdn.fake/img/doc18.png', 'https://cdn.fake/img/selfie18.png', 'pending', 11, 'low'),
('Robert Brown', 'robert.brown@example.com', '+442034455667', 'Reino Unido', 'Passport', 'UK22334455', 'https://cdn.fake/img/doc19.png', 'https://cdn.fake/img/selfie19.png', 'rejected', 88, 'high'),
('Alejandro Peña', 'alejandro.pena@example.com', '+56999887766', 'Chile', 'RUT', '19555444-3', 'https://cdn.fake/img/doc20.png', 'https://cdn.fake/img/selfie20.png', 'pending', 16, 'medium'),
('Paola Moreno', 'paola.moreno@example.com', '+5215511122233', 'México', 'Pasaporte', 'MXL2233445', 'https://cdn.fake/img/doc21.png', 'https://cdn.fake/img/selfie21.png', 'approved', 7, 'low'),
('Mateo Robles', 'mateo.robles@example.com', '+573115559900', 'Colombia', 'CC', '1002334455', 'https://cdn.fake/img/doc22.png', 'https://cdn.fake/img/selfie22.png', 'pending', 24, 'medium'),
('Isabella Cruz', 'isabella.cruz@example.com', '+50244556677', 'Guatemala', 'DPI', '256788990101', 'https://cdn.fake/img/doc23.png', 'https://cdn.fake/img/selfie23.png', 'rejected', 79, 'high'),
('Renato Moretti', 'renato.moretti@example.com', '+390445667788', 'Italia', 'Passport', 'IT55667788', 'https://cdn.fake/img/doc24.png', 'https://cdn.fake/img/selfie24.png', 'pending', 14, 'medium'),
('Elena Petrova', 'elena.petrova@example.com', '+74995556677', 'Rusia', 'Passport', 'RU33445566', 'https://cdn.fake/img/doc25.png', 'https://cdn.fake/img/selfie25.png', 'approved', 2, 'low'),
('Mohammed Al-Fayed', 'mohammed.alfayed@example.com', '+971501112233', 'Emiratos Árabes Unidos', 'Emirates ID', '784-1990-1234567-1', 'https://cdn.fake/img/doc26.png', 'https://cdn.fake/img/selfie26.png', 'pending', 30, 'medium'),
('Laura Ruiz', 'laura.ruiz@example.com', '+5215599922211', 'México', 'INE', 'LRZ77889911', 'https://cdn.fake/img/doc27.png', 'https://cdn.fake/img/selfie27.png', 'pending', 12, 'low'),
('Pedro Alvarez', 'pedro.alvarez@example.com', '+595991112233', 'Paraguay', 'CI', '4556677', 'https://cdn.fake/img/doc28.png', 'https://cdn.fake/img/selfie28.png', 'approved', 9, 'low'),
('Daniel Park', 'daniel.park@example.com', '+821012345678', 'Corea del Sur', 'Passport', 'KR77889900', 'https://cdn.fake/img/doc29.png', 'https://cdn.fake/img/selfie29.png', 'pending', 19, 'medium'),
('Nadia Hussein', 'nadia.hussein@example.com', '+201155667788', 'Egipto', 'Passport', 'EG44556677', 'https://cdn.fake/img/doc30.png', 'https://cdn.fake/img/selfie30.png', 'rejected', 86, 'high');
