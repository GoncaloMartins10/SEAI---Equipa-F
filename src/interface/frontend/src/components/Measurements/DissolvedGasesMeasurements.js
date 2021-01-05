import React, { Component } from 'react';
import {Tabs, Tab   } from '@material-ui/core';
import Chart from "./Chart";
import TabPanel from "./TabPanel";

export default class DissolvedGasesMeasurements extends Component {
    constructor(props) {
        super(props);
        console.log(this.props.furfuralData)
        this.state = {
            measurements: this.props.measurements,
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
                    <Tab label="h2" />
                    <Tab label="ch4" />
                    <Tab label="c2h6" />
                    <Tab label="c2h4" />
                    <Tab label="c2h2" />
                    <Tab label="co" />
                    <Tab label="coh2" />
                </Tabs>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={0}
                >
                    <Chart 
                        xaxis={this.state.measurements.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.measurements.map(obj => obj.h2),
                            label: "h2"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={1}
                >
                    <Chart 
                        xaxis={this.state.measurements.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.measurements.map(obj => obj.ch4),
                            label: "ch4"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={2}
                >
                    <Chart 
                        xaxis={this.state.measurements.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.measurements.map(obj => obj.c2h6),
                            label: "c2h6"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={3}
                >
                    <Chart 
                        xaxis={this.state.measurements.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.measurements.map(obj => obj.c2h4),
                            label: "c2h4"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={4}
                >
                    <Chart 
                        xaxis={this.state.measurements.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.measurements.map(obj => obj.c2h2),
                            label: "c2h2"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={5}
                >
                    <Chart 
                        xaxis={this.state.measurements.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.measurements.map(obj => obj.co),
                            label: "co"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={5}
                >
                    <Chart 
                        xaxis={this.state.measurements.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.measurements.map(obj => obj.coh2),
                            label: "coh2"
                        }}
                    />
                </TabPanel>
            </div>
        );
    }
}