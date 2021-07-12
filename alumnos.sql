create database if not exists alumnos;
use alumnos;

CREATE TABLE alumnos (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(150),
    apellido VARCHAR(150),
    mail VARCHAR(255),
	horarios VARCHAR (200),
    cel VARCHAR(150),
    foto VARCHAR (5000),
    PRIMARY KEY (id)
);

insert into alumnos (nombre, apellido, mail, cel, foto) values
('Laura', 'Avalle', 'laura.avalle@gmail.com', '1566517318', '1978-11-01 '); 

SELECT * FROM alumnos;
