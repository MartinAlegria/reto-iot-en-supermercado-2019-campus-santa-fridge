select sku, nombre, genero, count (genero) as conteo
from semana_i.datos_rfid inner join semana_i.datos_camara on (datos_camara.id_sesion=datos_rfid.id_sesion)
group by genero, nombre, sku;

select sku, nombre, edad, count (edad) as conteo, datos_rfid.ts
from semana_i.datos_rfid inner join semana_i.datos_camara on (datos_camara.id_sesion=datos_rfid.id_sesion)
group by edad, nombre, sku, datos_rfid.ts;

select edad, count(edad) as conteo
from semana_i.datos_camara
group by edad
order by edad asc;

select genero, count(genero) as conteo
from semana_i.datos_camara
group by genero
order by genero asc;

select extract(dayofweek from ts) as day, count(*) as Visitas
from semana_i.datos_camara
group by day
order by day;
