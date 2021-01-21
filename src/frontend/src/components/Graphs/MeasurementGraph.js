import React, {useState} from 'react';

import { makeStyles, Tabs, Tab } from '@material-ui/core';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Card from '@material-ui/core/Card';

import Chart from "./Chart";
import TabPanel from "./TabPanel";

const useStyles = makeStyles({
    tabs: {
        borderRadius: 2,
        height: '10%',
    },
    tabItems: {
        padding: 2,
        fontSize: '0.7rem',
        height: '10%'
    },
    outerContainer: {
        boxSizing: 'border-box',
        marginTop: 8,
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

export default function MeasurementGraph({data, graphsList, title}) {
    const classes = useStyles();

    const [tabSelected, setTabSelected] = useState(0);
    const handleTabChange = (e, selectedTab) => {
        setTabSelected(selectedTab);
    }

    return (
        <div className={classes.outerContainer}>
            {data ? 
            <Paper className={classes.innerContainer}>
                <Card>
                <Typography variant='h5' align='center' style={{paddingTop: 30, height: '10%'}}>
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
                {graphsList.map((obj, idx) => (
                    <TabPanel key={idx} index={idx} value={tabSelected}>
                        <Chart
                            xaxis={data.map(measurement => measurement.datestamp )} 
                            yaxis={{
                                data: data.map(measurement=> {
                                    return measurement[obj];
                                }),
                                label: obj
                            }}
                        />
                    </TabPanel>
                ))}
            </Paper>
              : 
            null
            }
        </div>
    );
}