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
    H2 REAL,
    CH4 REAL,
    C2H6 REAL,
    C2H4 REAL,
    C2H2 REAL,
    CO REAL,
    COH2 REAL,

    /**/
    DGA_scores REAL[6][6],
    oil_scores REAL[6][6],
    DS_weight REAL,
    IT_weight REAL,
    AN_weight REAL,
    WC_weight REAL,
    C_weight REAL,
    DF_weight REAL,

    /**/
    DGATC_scores REAL[4][4],
    DGATC_quantity REAL,

    /**/
    factor REAL[4],
    micro_water_weight REAL,
    acid_value_weight REAL,
    dielectric_loss_weight REAL,
    breakdown_voltage_weight REAL,

    /*low, medium, high*/
    algoritmo1 REAL[3],
    /*oil, gases, furan*/
    algoritmo2 REAL[3]
); 

CREATE TABLE ges_ativos.transformer_algorithm_weights (
    id_transformer INTEGER REFERENCES ges_ativos.transformer(id_transformer),
    id_algorithm INTEGER CHECK(id_algorithm>=0 and id_algorithm<=4),
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
    H2 REAL,
    CH4 REAL,
    C2H6 REAL,
    C2H4 REAL,
    C2H2 REAL,
    CO REAL,
    COH2 REAL
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
    indice INTEGER CHECK(indice>=-2 AND indice<=2)
);
