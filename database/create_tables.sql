CREATE DATABASE seai;
\c seai
CREATE SCHEMA ges_ativos;


CREATE TYPE algorithm AS ENUM ('algorithm1', 'algorithm2', 'algorithm3', 'algorithm4');

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
    id_algorithm ALGORITHM,
    id_weights INTEGER REFERENCES ges_ativos.weights(id_weights),
    PRIMARY KEY (id_transformer, id_algorithm, id_weights)
);

CREATE TABLE ges_ativos.oil_quality_measurements (
    id_oil_quality_measurement SERIAL PRIMARY KEY,
    breakdown_voltage REAL,
    water_content REAL,
    acidity REAL,
    color TEXT,
    interfacial_tension REAL
);

CREATE TABLE ges_ativos.furfural_measurements(
    id_furfural_measurement SERIAL PRIMARY KEY,
    timestamp_furfural_measurement TIMESTAMP,
    quantity REAL
);

CREATE TABLE ges_ativos.dissolved_gas_measurements (
    id_dissolved_gas_measurement SERIAL PRIMARY KEY,
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
    timestamp_load_measurement TIMESTAMP,
    power_factor REAL,
    load_factor REAL
);

CREATE TABLE ges_ativos.maintenance (
    id_maintenance SERIAL PRIMARY KEY, 
    timestamp_maintenance TIMESTAMP,
    bushings BOOLEAN,
    oil_leaks BOOLEAN,
    infrea_red BOOLEAN,
    cooling BOOLEAN,
    main_tank BOOLEAN,
    oil_tank BOOLEAN,
    foundation BOOLEAN,
    grounding BOOLEAN, 
    gaskets BOOLEAN,
    connectors BOOLEAN
);
