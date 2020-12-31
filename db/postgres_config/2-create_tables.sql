CREATE DATABASE seai;
\c seai
CREATE SCHEMA ges_ativos;


CREATE TABLE ges_ativos.transformer (
    id_transformer TEXT PRIMARY KEY,
    age INTEGER,
    nominal_voltage REAL
);

CREATE TABLE ges_ativos.weights (
    id_weights SERIAL PRIMARY KEY,
    id_algorithm INTEGER CHECK(id_algorithm>=1 AND id_algorithm<=4),
    id_transformer TEXT REFERENCES ges_ativos.transformer(id_transformer) ON DELETE CASCADE,
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

CREATE TABLE ges_ativos.oil_quality_measurements (
    id_oil_quality_measurement SERIAL PRIMARY KEY,
    id_transformer TEXT REFERENCES ges_ativos.transformer(id_transformer) ON DELETE CASCADE,
    datestamp DATE,
    breakdown_voltage REAL,
    water_content REAL,
    acidity REAL,
    color REAL,
    interfacial_tension REAL
);

CREATE TABLE ges_ativos.furfural_measurements(
    id_furfural_measurement SERIAL PRIMARY KEY,
    id_transformer TEXT REFERENCES ges_ativos.transformer(id_transformer) ON DELETE CASCADE,
    datestamp DATE,
    quantity REAL
);

CREATE TABLE ges_ativos.dissolved_gas_measurements (
    id_dissolved_gas_measurement SERIAL PRIMARY KEY,
    id_transformer TEXT REFERENCES ges_ativos.transformer(id_transformer) ON DELETE CASCADE,
    datestamp DATE,
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
    id_transformer TEXT REFERENCES ges_ativos.transformer(id_transformer) ON DELETE CASCADE,
    datestamp DATE,
    power_factor REAL,
    load_factor REAL
);

CREATE TABLE ges_ativos.maintenance (
    id_maintenance SERIAL PRIMARY KEY, 
    id_transformer TEXT REFERENCES ges_ativos.transformer(id_transformer) ON DELETE CASCADE,
    datestamp DATE,
    descript TEXT,
    impact_index INTEGER CHECK(impact_index >=-2 AND impact_index <=2)
);