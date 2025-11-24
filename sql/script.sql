-- Catálogo de Status
CREATE TABLE public.verification_status (
    id uuid PRIMARY KEY,
    code varchar(50) NOT NULL UNIQUE,
    description varchar(255) NOT NULL
);

-- Catálogo de Document Type
CREATE TABLE public.document_type (
    id uuid PRIMARY KEY,
    code varchar(50) NOT NULL UNIQUE,
    description varchar(255) NOT NULL
);

-- Catálogo de Risk Level
CREATE TABLE public.risk_level_catalog (
    id uuid PRIMARY KEY,
    code varchar(20) NOT NULL UNIQUE,
    description varchar(255) NOT NULL
);

-- catalogo de paises
CREATE TABLE public.country_catalog (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,   -- Ej: 'MX', 'US'
    name VARCHAR(100) NOT NULL UNIQUE,  -- Ej: 'México', 'Estados Unidos'
    calling_code VARCHAR(10) NOT NULL,  -- Ej: '+52', '+1'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE public.verification_requests (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    full_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    phone varchar(50) NOT NULL,
    country_id uuid NOT NULL,
    document_type_id uuid NOT NULL,
    document_number varchar(100) NOT NULL,
    document_image_url text NULL,
    selfie_image_url text NULL,
    status_id uuid NOT NULL,
    risk_score int4 NULL,
    risk_level_id uuid NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT fk_document_type FOREIGN KEY(document_type_id) REFERENCES public.document_type(id),
    CONSTRAINT fk_status FOREIGN KEY(status_id) REFERENCES public.verification_status(id),
    CONSTRAINT fk_risk_level FOREIGN KEY(risk_level_id) REFERENCES public.risk_level_catalog(id),
    CONSTRAINT fk_country FOREIGN KEY(country_id) REFERENCES public.country_catalog(id)
);

-- Índices
CREATE INDEX idx_verification_status_id ON public.verification_requests(status_id);
CREATE INDEX idx_verification_document_type_id ON public.verification_requests(document_type_id);
CREATE INDEX idx_verification_risk_level_id ON public.verification_requests(risk_level_id);
CREATE INDEX idx_verification_country_id ON public.verification_requests(country_id);

CREATE OR REPLACE VIEW public.vw_verification_requests AS
SELECT
    vr.id,
    vr.full_name,
    vr.email,
    vr.phone,
    c.name AS country,
    c.calling_code AS country_calling_code,
    dt.code AS document_type,
    vr.document_number,
    vr.document_image_url,
    vr.selfie_image_url,
    vs.code AS status,
    vr.risk_score,
    rl.code AS risk_level,
    vr.created_at,
    vr.updated_at
FROM public.verification_requests vr
JOIN public.document_type dt ON vr.document_type_id = dt.id
JOIN public.verification_status vs ON vr.status_id = vs.id
JOIN public.risk_level_catalog rl ON vr.risk_level_id = rl.id
JOIN public.country_catalog c ON vr.country_id = c.id;

INSERT INTO public.verification_status (id, code, description)
VALUES
('e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 'pending', 'Pendiente de revisión'),
('f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 'approved', 'Verificación aprobada'),
('a3d3f9e4-3f4d-6c7d-bf55-3c4d5e6f7a8b', 'rejected', 'Verificación rechazada'),
('b4c4e0f5-4a5e-7d8e-cf66-4d5e6f7a8b9c', 'requires_information', 'Se requiere información adicional');

INSERT INTO public.document_type (id, code, description)
VALUES
('11111111-aaaa-aaaa-aaaa-111111111111', 'INE', 'Credencial de elector'),
('22222222-bbbb-bbbb-bbbb-222222222222', 'CC', 'Cédula de ciudadanía'),
('33333333-cccc-cccc-cccc-333333333333', 'Passport', 'Pasaporte'),
('44444444-dddd-dddd-dddd-444444444444', 'DNI', 'Documento Nacional de Identidad'),
('55555555-eeee-eeee-eeee-555555555555', 'Driver License', 'Licencia de conducir'),
('66666666-ffff-ffff-ffff-666666666666', 'DUI', 'Documento Único de Identidad'),
('77777777-aaaa-aaaa-aaaa-777777777777', 'Cedula', 'Cédula Nacional'),
('88888888-bbbb-bbbb-bbbb-888888888888', 'RUT', 'Rol Único Tributario'),
('99999999-cccc-cccc-cccc-999999999999', 'DPI', 'Documento Personal de Identificación'),
('aaaaaaaa-dddd-dddd-dddd-aaaaaaaaaaaa', 'Emirates ID', 'Emirates Identification Card'),
('bbbbbbbb-eeee-eeee-eeee-bbbbbbbbbbbb', 'CI', 'Cédula de Identidad'),
('cccccccc-ffff-ffff-ffff-cccccccccccc', 'RG', 'Registro General');

INSERT INTO public.risk_level_catalog (id, code, description)
VALUES
('11111111-1111-1111-1111-111111111111', 'low', 'Bajo'),
('22222222-2222-2222-2222-222222222222', 'medium', 'Medio'),
('33333333-3333-3333-3333-333333333333', 'high', 'Alto'),
('44444444-4444-4444-4444-444444444444', 'n/c', 'Por determinar');

-- CORRECCIÓN: Agregar Brasil que faltaba y usar IDs consistentes
INSERT INTO public.country_catalog (id, code, name, calling_code)
VALUES
('11111111-1111-1111-1111-111111111111', 'MX', 'México', '+52'),
('22222222-2222-2222-2222-222222222222', 'CO', 'Colombia', '+57'),
('33333333-3333-3333-3333-333333333333', 'US', 'Estados Unidos', '+1'),
('44444444-4444-4444-4444-444444444444', 'AR', 'Argentina', '+54'),
('55555555-5555-5555-5555-555555555555', 'BR', 'Brasil', '+55'),  -- Brasil agregado
('66666666-6666-6666-6666-666666666666', 'SV', 'El Salvador', '+503'),
('77777777-7777-7777-7777-777777777777', 'EC', 'Ecuador', '+593'),
('88888888-8888-8888-8888-888888888888', 'CL', 'Chile', '+56'),
('99999999-9999-9999-9999-999999999999', 'GT', 'Guatemala', '+502'),
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'AE', 'Emiratos Árabes Unidos', '+971'),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'PY', 'Paraguay', '+595'),
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'KR', 'Corea del Sur', '+82'),
('dddddddd-dddd-dddd-dddd-dddddddddddd', 'EG', 'Egipto', '+20'),
('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'DE', 'Alemania', '+49'),
('ffffffff-ffff-ffff-ffff-ffffffffffff', 'JP', 'Japón', '+81'),
('12121212-1212-1212-1212-121212121212', 'ES', 'España', '+34'),
('13131313-1313-1313-1313-131313131313', 'IT', 'Italia', '+39'),
('14141414-1414-1414-1414-141414141414', 'RU', 'Rusia', '+7'),
('15151515-1515-1515-1515-151515151515', 'GB', 'Reino Unido', '+44');

-- CORRECCIÓN: Ajustar los INSERT de verification_requests con IDs consistentes
INSERT INTO public.verification_requests
(full_name, email, phone, country_id, document_type_id, document_number, document_image_url, selfie_image_url, status_id, risk_score, risk_level_id, created_at, updated_at)
VALUES
('Carlos Méndez Ruiz', 'carlos.mendez@example.com', '+5215512341111', '11111111-1111-1111-1111-111111111111', '11111111-aaaa-aaaa-aaaa-111111111111', 'MDR89012344', 'https://cdn.fake/img/doc1.png', 'https://cdn.fake/img/selfie1.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 12, '11111111-1111-1111-1111-111111111111', '2025-03-15 10:23:45', '2025-03-15 10:23:45'),
('Ana Sofía Delgado', 'ana.delgado@example.com', '+573125554444', '22222222-2222-2222-2222-222222222222', '22222222-bbbb-bbbb-bbbb-222222222222', '1022334455', 'https://cdn.fake/img/doc2.png', 'https://cdn.fake/img/selfie2.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 5, '11111111-1111-1111-1111-111111111111', '2025-07-22 14:12:30', '2025-07-22 14:12:30'),
('John Peterson', 'john.peterson@example.com', '+14155551212', '33333333-3333-3333-3333-333333333333', '33333333-cccc-cccc-cccc-333333333333', 'US987654321', 'https://cdn.fake/img/doc3.png', 'https://cdn.fake/img/selfie3.png', 'a3d3f9e4-3f4d-6c7d-bf55-3c4d5e6f7a8b', 78, '33333333-3333-3333-3333-333333333333', '2025-01-08 08:55:12', '2025-01-08 08:55:12'),
('María Fernanda López', 'maria.lopez@example.com', '+549112223333', '44444444-4444-4444-4444-444444444444', '44444444-dddd-dddd-dddd-444444444444', '40991234', 'https://cdn.fake/img/doc4.png', 'https://cdn.fake/img/selfie4.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 22, '22222222-2222-2222-2222-222222222222', '2025-05-19 16:40:05', '2025-05-19 16:40:05'),
('Luiz Carvalho', 'luiz.carvalho@example.com', '+551199887766', '55555555-5555-5555-5555-555555555555', 'cccccccc-ffff-ffff-ffff-cccccccccccc', '23455678901', 'https://cdn.fake/img/doc5.png', 'https://cdn.fake/img/selfie5.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 10, '11111111-1111-1111-1111-111111111111', '2025-09-11 12:20:00', '2025-09-11 12:20:00'),
('Sofía Herrera', 'sofia.herrera@example.com', '+5215577744411', '11111111-1111-1111-1111-111111111111', '33333333-cccc-cccc-cccc-333333333333', 'GTM1122334', 'https://cdn.fake/img/doc6.png', 'https://cdn.fake/img/selfie6.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 8, '11111111-1111-1111-1111-111111111111', '2025-02-28 09:15:44', '2025-02-28 09:15:44'),
('Valentina Paredes', 'valentina.paredes@example.com', '+573004449999', '22222222-2222-2222-2222-222222222222', '22222222-bbbb-bbbb-bbbb-222222222222', '1009988776', 'https://cdn.fake/img/doc7.png', 'https://cdn.fake/img/selfie7.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 15, '22222222-2222-2222-2222-222222222222', '2025-06-03 11:30:10', '2025-06-03 11:30:10'),
('Eduardo Jiménez', 'eduardo.jimenez@example.com', '+5215588899911', '11111111-1111-1111-1111-111111111111', '11111111-aaaa-aaaa-aaaa-111111111111', 'JMN09283746', 'https://cdn.fake/img/doc8.png', 'https://cdn.fake/img/selfie8.png', 'a3d3f9e4-3f4d-6c7d-bf55-3c4d5e6f7a8b', 83, '33333333-3333-3333-3333-333333333333', '2025-08-15 18:05:22', '2025-08-15 18:05:22'),
('Patricia Gómez', 'patricia.gomez@example.com', '+34911223344', '12121212-1212-1212-1212-121212121212', '44444444-dddd-dddd-dddd-444444444444', '77220011X', 'https://cdn.fake/img/doc9.png', 'https://cdn.fake/img/selfie9.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 3, '11111111-1111-1111-1111-111111111111', '2025-04-10 13:22:11', '2025-04-10 13:22:11'),
('Hiroshi Tanaka', 'hiroshi.tanaka@example.com', '+81344556677', 'ffffffff-ffff-ffff-ffff-ffffffffffff', '33333333-cccc-cccc-cccc-333333333333', 'JP55667788', 'https://cdn.fake/img/doc10.png', 'https://cdn.fake/img/selfie10.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 18, '22222222-2222-2222-2222-222222222222', '2025-03-21 17:55:30', '2025-03-21 17:55:30'),
('Marco Antonio Silva', 'marco.silva@example.com', '+551198887744', '55555555-5555-5555-5555-555555555555', 'cccccccc-ffff-ffff-ffff-cccccccccccc', '33221444', 'https://cdn.fake/img/doc11.png', 'https://cdn.fake/img/selfie11.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 9, '11111111-1111-1111-1111-111111111111', '2025-01-28 10:10:10', '2025-01-28 10:10:10'),
('Emily Johnson', 'emily.johnson@example.com', '+16175551234', '33333333-3333-3333-3333-333333333333', '55555555-eeee-eeee-eeee-555555555555', 'D1234567', 'https://cdn.fake/img/doc12.png', 'https://cdn.fake/img/selfie12.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 29, '22222222-2222-2222-2222-222222222222', '2025-05-05 14:50:22', '2025-05-05 14:50:22'),
('José Luis Castillo', 'joseluis.castillo@example.com', '+5215588771122', '11111111-1111-1111-1111-111111111111', '11111111-aaaa-aaaa-aaaa-111111111111', 'CLS56788990', 'https://cdn.fake/img/doc13.png', 'https://cdn.fake/img/selfie13.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 6, '11111111-1111-1111-1111-111111111111', '2025-06-25 09:12:45', '2025-06-25 09:12:45'),
('Daniela Rivas', 'daniela.rivas@example.com', '+50377889900', '66666666-6666-6666-6666-666666666666', '66666666-ffff-ffff-ffff-666666666666', '04567781-2', 'https://cdn.fake/img/doc14.png', 'https://cdn.fake/img/selfie14.png', 'a3d3f9e4-3f4d-6c7d-bf55-3c4d5e6f7a8b', 91, '33333333-3333-3333-3333-333333333333', '2025-02-14 12:34:56', '2025-02-14 12:34:56'),
('Lucía Martínez', 'lucia.martinez@example.com', '+541155994433', '44444444-4444-4444-4444-444444444444', '44444444-dddd-dddd-dddd-444444444444', '44112233', 'https://cdn.fake/img/doc15.png', 'https://cdn.fake/img/selfie15.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 13, '11111111-1111-1111-1111-111111111111', '2025-08-02 08:22:33', '2025-08-02 08:22:33'),
('Felipe Andrade', 'felipe.andrade@example.com', '+593998877665', '77777777-7777-7777-7777-777777777777', '77777777-aaaa-aaaa-aaaa-777777777777', '1723344556', 'https://cdn.fake/img/doc16.png', 'https://cdn.fake/img/selfie16.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 20, '22222222-2222-2222-2222-222222222222', '2025-07-12 15:44:22', '2025-07-12 15:44:22'),
('Thomas Müller', 'thomas.muller@example.com', '+491511223344', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '33333333-cccc-cccc-cccc-333333333333', 'DE99887766', 'https://cdn.fake/img/doc17.png', 'https://cdn.fake/img/selfie17.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 4, '11111111-1111-1111-1111-111111111111', '2025-01-17 11:11:11', '2025-01-17 11:11:11'),
('Camila Torres', 'camila.torres@example.com', '+5215577553399', '11111111-1111-1111-1111-111111111111', '11111111-aaaa-aaaa-aaaa-111111111111', 'TRC55667788', 'https://cdn.fake/img/doc18.png', 'https://cdn.fake/img/selfie18.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 11, '11111111-1111-1111-1111-111111111111', '2025-06-08 14:20:20', '2025-06-08 14:20:20'),
('Robert Brown', 'robert.brown@example.com', '+442034455667', '15151515-1515-1515-1515-151515151515', '33333333-cccc-cccc-cccc-333333333333', 'UK22334455', 'https://cdn.fake/img/doc19.png', 'https://cdn.fake/img/selfie19.png', 'a3d3f9e4-3f4d-6c7d-bf55-3c4d5e6f7a8b', 88, '33333333-3333-3333-3333-333333333333', '2025-03-30 16:45:00', '2025-03-30 16:45:00'),
('Alejandro Peña', 'alejandro.pena@example.com', '+56999887766', '88888888-8888-8888-8888-888888888888', '88888888-bbbb-bbbb-bbbb-888888888888', '19555444-3', 'https://cdn.fake/img/doc20.png', 'https://cdn.fake/img/selfie20.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 16, '22222222-2222-2222-2222-222222222222', '2025-05-18 10:30:30', '2025-05-18 10:30:30'),
('Paola Moreno', 'paola.moreno@example.com', '+5215511122233', '11111111-1111-1111-1111-111111111111', '33333333-cccc-cccc-cccc-333333333333', 'MXL2233445', 'https://cdn.fake/img/doc21.png', 'https://cdn.fake/img/selfie21.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 7, '11111111-1111-1111-1111-111111111111', '2025-04-25 12:12:12', '2025-04-25 12:12:12'),
('Mateo Robles', 'mateo.robles@example.com', '+573115559900', '22222222-2222-2222-2222-222222222222', '22222222-bbbb-bbbb-bbbb-222222222222', '1002334455', 'https://cdn.fake/img/doc22.png', 'https://cdn.fake/img/selfie22.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 24, '22222222-2222-2222-2222-222222222222', '2025-07-01 15:50:50', '2025-07-01 15:50:50'),
('Isabella Cruz', 'isabella.cruz@example.com', '+50244556677', '99999999-9999-9999-9999-999999999999', '99999999-cccc-cccc-cccc-999999999999', '256788990101', 'https://cdn.fake/img/doc23.png', 'https://cdn.fake/img/selfie23.png', 'a3d3f9e4-3f4d-6c7d-bf55-3c4d5e6f7a8b', 79, '33333333-3333-3333-3333-333333333333', '2025-03-12 11:11:11', '2025-03-12 11:11:11'),
('Renato Moretti', 'renato.moretti@example.com', '+390445667788', '13131313-1313-1313-1313-131313131313', '33333333-cccc-cccc-cccc-333333333333', 'IT55667788', 'https://cdn.fake/img/doc24.png', 'https://cdn.fake/img/selfie24.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 14, '22222222-2222-2222-2222-222222222222', '2025-06-21 10:10:10', '2025-06-21 10:10:10'),
('Carolina Patiño', 'carolina.patino@example.com', '+573223334455', '22222222-2222-2222-2222-222222222222', '22222222-bbbb-bbbb-bbbb-222222222222', '10055667788', 'https://cdn.fake/img/doc25.png', 'https://cdn.fake/img/selfie25.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 6, '11111111-1111-1111-1111-111111111111', '2025-08-10 08:08:08', '2025-08-10 08:08:08'),
('Andrés Salazar', 'andres.salazar@example.com', '+5215566677889', '11111111-1111-1111-1111-111111111111', '11111111-aaaa-aaaa-aaaa-111111111111', 'SLZ99887766', 'https://cdn.fake/img/doc26.png', 'https://cdn.fake/img/selfie26.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 19, '22222222-2222-2222-2222-222222222222', '2025-02-20 13:20:20', '2025-02-20 13:20:20'),
('Natalia Rojas', 'natalia.rojas@example.com', '+573334445566', '22222222-2222-2222-2222-222222222222', '22222222-bbbb-bbbb-bbbb-222222222222', '1011223344', 'https://cdn.fake/img/doc27.png', 'https://cdn.fake/img/selfie27.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 21, '22222222-2222-2222-2222-222222222222', '2025-03-03 14:44:44', '2025-03-03 14:44:44'),
('Diego Herrera', 'diego.herrera@example.com', '+5215577998877', '11111111-1111-1111-1111-111111111111', '11111111-aaaa-aaaa-aaaa-111111111111', 'DGH11223344', 'https://cdn.fake/img/doc28.png', 'https://cdn.fake/img/selfie28.png', 'e1f1c7d2-1d2b-4a5b-bf33-1a2b3c4d5e6f', 17, '22222222-2222-2222-2222-222222222222', '2025-05-14 09:09:09', '2025-05-14 09:09:09'),
('Santiago López', 'santiago.lopez@example.com', '+5215588332211', '11111111-1111-1111-1111-111111111111', '33333333-cccc-cccc-cccc-333333333333', 'SLO55667788', 'https://cdn.fake/img/doc29.png', 'https://cdn.fake/img/selfie29.png', 'a3d3f9e4-3f4d-6c7d-bf55-3c4d5e6f7a8b', 32, '33333333-3333-3333-3333-333333333333', '2025-01-30 12:12:12', '2025-01-30 12:12:12'),
('Valeria Mendoza', 'valeria.mendoza@example.com', '+5215577665544', '11111111-1111-1111-1111-111111111111', '11111111-aaaa-aaaa-aaaa-111111111111', 'VMN22334455', 'https://cdn.fake/img/doc30.png', 'https://cdn.fake/img/selfie30.png', 'f2e2d8c3-2e3c-5b6c-af44-2b3c4d5e6f7a', 27, '22222222-2222-2222-2222-222222222222', '2025-06-11 11:11:11', '2025-06-11 11:11:11');