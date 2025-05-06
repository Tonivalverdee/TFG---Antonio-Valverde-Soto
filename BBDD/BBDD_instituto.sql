create database if not exists instituto;
use instituto;

create table if not exists alumnos(
    id int auto_increment primary key,
    nombre varchar(50) not null,
    apellidos varchar(50) not null,
    fecha_nacimiento date not null,
    dni varchar(9) not null unique,
    direccion varchar(100) not null,
    telefono int(9) not null
);
