import React, {useEffect, useState } from 'react';
import {makeStyles} from '@material-ui/core';

import Typography from '@material-ui/core/Typography';
import {Grid, Button} from '@material-ui/core';
import {Alert, AlertTitle} from '@material-ui/lab'

import MeasurementGraph from "./Graphs/MeasurementGraph";
import HIGraph from "./Graphs/HIGraph";
import HITable from "./Tables/HITable";
import InferenceTable from './Tables/InferenceTable'



const useStyles = makeStyles({
    root: {
        width: '100%',
    },
    alert: {
        marginTop: 8,
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
    },
    button: {
        marginTop: 30,
        justifyContent: 'center',
        fontWeight: 'bold', 
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

    function handleClick(e) {
        let url = "http://localhost:8000/api/transformers/" + props.match.params.transformerId + "/report/";
        window.open(url); 
    }
    
    const [inferredHI, setInferredHI] = useState({})
    const [processing, setProcessing] = useState(false)
    function inferHI(e) {
        const url = 'http://localhost:8000/api/transformers/infer/';
        setProcessing(true);
        fetch(url, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(json => {
            setProcessing(false);
            setInferredHI(json[props.match.params.transformerId]);
        })
    }
    
    return (
        <Grid container>
            <Grid item xs={12}>
                <Typography variant="h4" className={classes.typography}>
                    Transformer {props.match.params.transformerId}
                </Typography>
            </Grid>
            <Grid container style={{marginTop: 50}}>
                <Grid item xs={12} md={6}>
                <MeasurementGraph
                  data={measurementsData.load} 
                  graphsList={["load_factor", "power_factor"]}
                  title={"Load"}
                />
                </Grid>
                <Grid item xs={12} md={6}>
                <MeasurementGraph
                  data={measurementsData.oil_quality}
                  graphsList={['breakdown_voltage', 'water_content', 'acidity', 'color', 'interfacial_tension']}
                  title={"Oil Quality"}
                />
                </Grid>
            </Grid>
            <Grid container>
                <Grid item xs={12} md={6}>
                <MeasurementGraph
                  data={measurementsData.furfural}
                  graphsList={["quantity"]}
                  title={"Furfural"}
                />
                </Grid>
                <Grid item xs={12} md={6}>
                <MeasurementGraph
                  data={measurementsData.dissolved_gases}
                  graphsList={['h2', 'ch4', 'c2h6', 'c2h4', 'c2h2', 'co', 'coh2']}
                  title={"Dissolved Gases"}
                />
                </Grid>
            </Grid>
            <Grid container>
                <Grid item xs={12} md={6}>
                <HIGraph
                  data={healthIndex}
                  graphsList={["Algorithm 1", "Algorithm 2", "Algorithm 3", "Algorithm 4"]}
                  title={"Health Indices"}
                />
                </Grid>
                <Grid item xs={12} md={3}>
                    <HITable data={healthIndex}/>
                    <Button variant='contained' onClick={inferHI} style={{fontWeight: 'bold', marginLeft: 10, marginTop:8}}>
                        Infer Transformer Health Index
                    </Button>
                    {processing && 
                        <Alert 
                        severity='info'
                        className={classes.alert}
                        >
                            <AlertTitle>Info</AlertTitle>
                            Inferring Health Index
                        </Alert>
                    }
                </Grid>
                <Grid item xs={12} md={3}>
                    {(Object.keys(inferredHI).length !== 0) && 
                        <InferenceTable 
                        data={inferredHI}
                        transformerId={props.match.params.transformerId}
                        />
                    }
                </Grid>
            </Grid>
            <Button variant='contained' className={classes.button} onClick={handleClick}>
                Generate Report for {props.match.params.transformerId}
            </Button>
        </Grid>
    );
}