import React, {useEffect, useState } from 'react';
import {makeStyles} from '@material-ui/core';

import Typography from '@material-ui/core/Typography'

import MeasurementGraph from "./Graphs/MeasurementGraph"
import HIGraph from "./Graphs/HIGraph"
import HITable from "./HITable"



const useStyles = makeStyles({
    root: {
        width: '100%',
    },
    typography: {
        marginTop: 50,
        textAlign: 'center'
    },
    twoGraphContainer: {
        boxSizing: 'border-box',
        marginTop:50,
        height: 500,
        display: 'flex',
    }
});


export default function TransformerPage(props) {
    const classes = useStyles();

    const [measurementsData, setMeasurementsData] = useState({})
    useEffect(() => {
        const url = "http://localhost:8000/api/transformers/"
        fetch(url + props.match.params.transformerId + "/medicoes/", {
            method: "GET" 
        })
        .then((response) => response.json())
        .then((obj) => {
            setMeasurementsData({
                load: obj.load,
                furfural: obj.furfural,
                dissolved_gases: obj.dissolved_gases,
                oil_quality: obj.oil_quality
            })
        })
        .catch(() => {
            console.log("Can't access: " + url);
        })
        
    }, [setMeasurementsData]);;


    const [healthIndex, setHealthIndex] = useState([]);
    useEffect(() => {
        const url = "http://localhost:8000/api/transformers/" + props.match.params.transformerId + "/HI/"
        fetch(url, {
            method: 'GET'
        })
        .then(response => response.json())
        .then(listObject => {
            setHealthIndex(listObject); 
        })
    }, [setHealthIndex]);
    
    return (
        <div className={classes.root}>
            <Typography variant="h4" className={classes.typography}>
                Transformer {props.match.params.transformerId}
            </Typography>
            <div className={classes.twoGraphContainer}>
                <MeasurementGraph
                  data={measurementsData.load} 
                  graphsList={["load_factor", "power_factor"]}
                  title={"Load"}
                />
                <MeasurementGraph
                  data={measurementsData.oil_quality}
                  graphsList={['breakdown_voltage', 'water_content', 'acidity', 'color', 'interfacial_tension']}
                  title={"Oil Quality"}
                />
            </div>
            <div className={classes.twoGraphContainer}>
                <MeasurementGraph
                  data={measurementsData.furfural}
                  graphsList={["quantity"]}
                  title={"Furfural"}
                />
                <MeasurementGraph
                  data={measurementsData.dissolved_gases}
                  graphsList={['h2', 'ch4', 'c2h6', 'c2h4', 'c2h2', 'co', 'coh2']}
                  title={"Dissolved Gases"}
                />
            </div>
            <div className={classes.twoGraphContainer}>
                <HIGraph
                  data={healthIndex}
                  graphsList={["Algorithm 1", "Algorithm 2", "Algorithm 3", "Algorithm 4"]}
                  title={"Health Indices"}
                />
                <HITable
                  data={healthIndex}
                />
            </div>

        </div>
    );
}