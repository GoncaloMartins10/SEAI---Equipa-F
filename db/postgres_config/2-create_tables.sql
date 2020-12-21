CREATE DATABASE seai;
\c seai
CREATE SCHEMA ges_ativos;


CREATE TABLE ges_ativos.transformer (
    id_transformer SERIAL PRIMARY KEY,
    age INTEGER,
    nominal_voltage REAL
);

CREATE TABLE ges_ativos.weights (
    id_weights SERIAL PRIMARY KEY,
    
    /**/

    h2 REAL,
    ch4 REAL,
    c2h6 REAL,
    c2h4 REAL,
    c2h2 REAL,
    co REAL,
    coh2 REAL,

    /**/
    dga REAL[6][6],
    oil REAL[6][6],

    ds REAL,
    it REAL,
    an REAL,
    wc REAL,
    c REAL,
    df REAL,

    /**/
    dgatc_scores REAL[4][4],
    dgatc_quant REAL,

    /**/
    factor REAL[4],
    micro_water REAL,
    acid_value REAL,
    dielectric_loss REAL,
    breakdown_voltage REAL,

    /*low, medium, high*/
    algorithm1 REAL[3],
    /*oil, gases, furan*/
    algorithm4 REAL[3]
); 

CREATE TABLE ges_ativos.transformer_algorithm_weights (
    id_transformer INTEGER REFERENCES ges_ativos.transformer(id_transformer),
    id_algorithm INTEGER CHECK(id_algorithm>=1 AND id_algorithm<=4),
    id_weights INTEGER REFERENCES ges_ativos.weights(id_weights),
    PRIMARY KEY (id_transformer, id_algorithm)
);

CREATE TABLE ges_ativos.oil_quality_measurements (
    id_oil_quality_measurement SERIAL PRIMARY KEY,
    id_transformer INTEGER REFERENCES ges_ativos.transformer(id_transformer),
    timestamp_oil_quality_measurement TIMESTAMP,
    breakdown_voltage REAL,
    water_content REAL,
    acidity REAL,
    color REAL,
    interfacial_tension REAL
);

CREATE TABLE ges_ativos.furfural_measurements(
    id_furfural_measurement SERIAL PRIMARY KEY,
    id_transformer INTEGER REFERENCES ges_ativos.transformer(id_transformer),
    timestamp_furfural_measurement TIMESTAMP,
    quantity REAL
);

CREATE TABLE ges_ativos.dissolved_gas_measurements (
    id_dissolved_gas_measurement SERIAL PRIMARY KEY,
    id_transformer INTEGER REFERENCES ges_ativos.transformer(id_transformer),
    timestamp_dissolved_gas_measurements TIMESTAMP,
    h2 REAL,
    ch4 REAL,
    c2h6 REAL,
    c2h4 REAL,
    c2h2 REAL,
    co REAL,
    coh2 REAL
);

CREATE TABLE ges_ativos.load_measurements (
    id_load_measurement SERIAL PRIMARY KEY,
    id_transformer INTEGER REFERENCES ges_ativos.transformer(id_transformer),
    timestamp_load_measurement TIMESTAMP,
    power_factor REAL,
    load_factor REAL
);

CREATE TABLE ges_ativos.maintenance (
    id_maintenance SERIAL PRIMARY KEY, 
    id_transformer INTEGER REFERENCES ges_ativos.transformer(id_transformer),
    timestamp_maintenance TIMESTAMP,
    indice INTEGER CHECK(indice>=-2 AND indice <=2)
);
