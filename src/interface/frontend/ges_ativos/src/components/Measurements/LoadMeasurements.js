import React, { Component, useState } from 'react';
import { Tabs, Tab } from '@material-ui/core';
import Chart from "./Chart";
import TabPanel from "./TabPanel";

/*export default class LoadMeasurements extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loadData: this.props.loadData,
            tabDisplay: 0
        }
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(e, value) {
        this.setState({
            ...this.state,
            tabDisplay: value
        });
    }

    render() {
        return (
            <div>
                <Tabs 
                    onChange={this.handleChange}
                    value={this.state.tabDisplay}
                    indicatorColor="primary"
                    textColor="primary"
                    fullWidth
                >
                    <Tab 
                        label="load_factor" 
                    />
                    <Tab 
                        label="power_factor" 
                    />
                </Tabs>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={0}
                >
                    <Chart 
                        xaxis={this.state.loadData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.loadData.map(obj => obj.load_factor),
                            label: "load_factor"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={1}
                >
                    <Chart 
                        xaxis={this.state.loadData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.loadData.map(obj => obj.power_factor),
                            label: "power_factor"
                        }}
                    />
                </TabPanel>
            </div>
        );
    }
}*/

export default function LoadMeasurements({data}) {
    const [tabSelected, setTabSelected] = useState(0);
    
    const handleTabChange = (e) => {
        console.log("changing tabs");
        console.log(e);
    }
    return (
        <div>
            {data ? 
            <Tabs
              value={0}
              onChange={handleTabChange}
            >
                <Tab label="power factor"/>
                <Tab label="power factor"/>
            </Tabs>
              : 
            null
            }
        </div>
    );
}