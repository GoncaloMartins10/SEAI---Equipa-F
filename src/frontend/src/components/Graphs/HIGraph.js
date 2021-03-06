import React, {useState} from 'react';

import { makeStyles, Tabs, Tab } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Card from '@material-ui/core/Card';

import Chart from "./Chart";
import TabPanel from "./TabPanel";



const useStyles = makeStyles({
    tabs: {
        height: '10%',
        borderRadius: 2,
    },
    tabItems: {
        padding: 2,
        fontSize: '0.7rem'
    },
    outerContainer: {
        marginTop:8,
        width: '100%',
        height: 500,
        '&:first-child': {
            paddingRight: 5,
        },
        '&:last-child': {
            paddingLeft: 5,
        }
    },
    innerContainer: {
        height: '100%'
    }
});


export default function HIGraph({data, graphsList, title}) {
    const classes = useStyles();

    const [tabSelected, setTabSelected] = useState(0);
    const handleTabChange = (e, selectedTab) => {
        setTabSelected(selectedTab);
    }

    const algorithms = [
        {
            datestamp: [], 
            hi: []
        }, 
        {
            datestamp: [], 
            hi: []
        }, 
        {
            datestamp: [], 
            hi:[]
        }, 
        {
            datestamp: [],
            hi: []
        }
    ];
    data.forEach(({datestamp, hi, id_algorithm}, index) => {
        algorithms[id_algorithm-1].hi.push(hi);
        algorithms[id_algorithm-1].datestamp.push(datestamp);
    })

    return (
        <div className={classes.outerContainer}>
            {data ? 
            <Paper className={classes.innerContainer}>
                <Card>
                <Typography variant='h5' align='center' style={{height: '10%', paddingTop: 30}}>
                    {title}
                </Typography>
                <Tabs
                  value={tabSelected}
                  onChange={handleTabChange}
                  className={classes.tabs}
                  variant='scrollable'
                >
                    {graphsList.map((obj, idx) => 
                        <Tab key={idx} label={obj} className={classes.tabItems}/> 
                    )}
                </Tabs>
                </Card>
                {algorithms.map((obj, index) => {
                    return (<TabPanel
                        value={tabSelected} 
                        index={index}
                        key={index}
                    >
                        <Chart
                            xaxis={obj.datestamp} 
                            yaxis={{
                                data: obj.hi,
                                label: `Algorithm ${index}`
                            }} 
                        /> 
                    </TabPanel>)
                })}
            </Paper>
              : 
            null
            }
        </div>
    );
}