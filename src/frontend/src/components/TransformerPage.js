import React, {useEffect, useState } from 'react';
import {makeStyles} from '@material-ui/core';

import Typography from '@material-ui/core/Typography'

import TabsAndGraphs from "./Measurements/TabsAndGraphs"



const useStyles = makeStyles({
    typography: {
        textAlign: 'center'
    },
    charts: {
        marginTop: 50,
        display: 'flex',
        flexWrap: 'wrap',
        flexDirection: 'row',
        height: 400
    }
});


export default function TransformerPage(props) {
    const classes = useStyles();

    const [measurementsData, setMeasurementsData] = useState({})
    useEffect(() => {
        const url = "http://localhost:8000/api/transformers/"
        fetch(url + props.match.params.transformerId + "/medicoes", {
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
        
    }, [setMeasurementsData])
    
    return (
        <div>
            <Typography variant="h4" className={classes.typography}>
                Transformer {props.match.params.transformerId}
            </Typography>
            <span> </span>
            <div style={{display:'flex', marginTop: 50, width: '100%', height: 300}}>
                <TabsAndGraphs 
                  data={measurementsData.load} 
                  graphsList={["load_factor", "power_factor"]}
                  title={"Load"}
                />
                <TabsAndGraphs
                  data={measurementsData.oil_quality}
                  graphsList={['breakdown_voltage', 'water_content', 'acidity', 'color', 'interfacial_tension']}
                  title={"Oil Quality"}
                />
            </div>
            <div style={{display:'flex', marginTop: 150, width: '100%', height: 300 }}>
                <TabsAndGraphs
                  data={measurementsData.furfural}
                  graphsList={["quantity"]}
                  title={"Furfural"}
                />
                <TabsAndGraphs
                  data={measurementsData.dissolved_gases}
                  graphsList={['h2', 'ch4', 'c2h6', 'c2h4', 'c2h2', 'co', 'coh2']}
                  title={"Dissolved Gasses"}
                />
            </div>
        </div>
    );
}