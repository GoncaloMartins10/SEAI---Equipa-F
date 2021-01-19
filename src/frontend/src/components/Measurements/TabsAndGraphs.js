import React, { Component, useState } from 'react';

import { makeStyles, Tabs, Tab } from '@material-ui/core';
import Typography from '@material-ui/core/Typography'

import Chart from "./Chart";
import TabPanel from "./TabPanel";


const useStyles = makeStyles({
    tabs: {
        flexBasis: '50%',
        borderRadius: 2,
    },
    tabItems: {
        padding: 2,
        fontSize: '0.7rem'
    },
    outerContainer: {
        width: '50%',
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

export default function TabsAndGraphs({data, graphsList, title}) {
    const classes = useStyles();

    const [tabSelected, setTabSelected] = useState(0);
    const handleTabChange = (e, selectedTab) => {
        setTabSelected(selectedTab);
    }

    return (
        <div className={classes.outerContainer}>
            {data ? 
            <div className={classes.innerContainer}>
                <Typography variant='h5' align='center'>
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
            </div>
              : 
            null
            }
        </div>
    );
}