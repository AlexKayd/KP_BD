INSERT INTO public.admins (login, password, name, surname, sex, phone_number)
VALUES
    ('admin1', 111, 'Иван', 'Иванов', 'мужской', '89001112233'),
    ('admin2', 123, 'Мария', 'Петрова', 'женский', '89004445566'),
    ('admin3', 222, 'Алексей', 'Сидоров', 'мужской', '89007778899'),
    ('admin4', 101, 'Елена', 'Кузнецова', 'женский', '89009990000');


INSERT INTO public.diameters (diameter_id, diameter) 
VALUES
(4, 25.00),
(5, 40.00),
(6, 76.00);


INSERT INTO public.materials (material_id, material, price) 
VALUES
(11, 'Матовая бумага', 0.35),
(12, 'Полуглянцевая бумага', 0.38),
(13, 'Глянцевая бумага', 0.44),
(14, 'Голографическая бумага', 0.80),
(15, 'Термобумага', 0.48),
(16, 'Термотрансферная бумага', 0.66),
(17, 'Полиэтиленовая пленка', 0.52),
(18, 'Полипропиленовая пленка', 0.56),
(19, 'Биодеградируемая пленка', 0.60),
(20, 'Сатин', 0.70);


INSERT INTO public.sizes (size_id, "size", price) 
VALUES
(20, '30х20', 0.35),
(21, '40х30', 0.40),
(22, '43х25', 0.44),
(23, '58х30', 0.60),
(24, '58х40', 0.63),
(25, '58х60', 0.67),
(26, '75х120', 0.72),
(27, '100х50', 0.80),
(28, '100х72', 0.85),
(29, '100х150', 0.90),
(30, '150х50', 0.99); 