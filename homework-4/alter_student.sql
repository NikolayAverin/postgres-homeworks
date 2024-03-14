-- 1. Создать таблицу student с полями student_id serial, first_name varchar, last_name varchar, birthday date, phone varchar
CREATE TABLE student
    (
	student_id serial,
	first_name varchar,
	last_name varchar,
	birthday date,
	phone varchar
    )

-- 2. Добавить в таблицу student колонку middle_name varchar
ALTER TABLE student
ADD COLUMN middle_name varchar


-- 3. Удалить колонку middle_name
ALTER TABLE student
DROP COLUMN middle_name

-- 4. Переименовать колонку birthday в birth_date
ALTER TABLE student
RENAME COLUMN birthday TO birth_date

-- 5. Изменить тип данных колонки phone на varchar(32)
ALTER TABLE student
ALTER COLUMN phone SET DATA TYPE varchar(32)

-- 6. Вставить три любых записи с автогенерацией идентификатора
INSERT INTO student (first_name, last_name, birth_date, phone) VALUES
('Guido', 'Rossum', '1956-01-31', '89997775533'),
('Edgar', 'Codd', '1923-08-23', '89876543210'),
('Rasmus', 'Lerdorf', '1968-11-22', '89258147253')

-- 7. Удалить все данные из таблицы со сбросом идентификатор в исходное состояние
TRUNCATE TABLE student RESTART IDENTITY