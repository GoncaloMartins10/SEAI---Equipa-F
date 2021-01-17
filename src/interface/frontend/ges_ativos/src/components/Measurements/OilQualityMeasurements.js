import React, { Component } from 'react';
import {Tabs, Tab} from '@material-ui/core';
import Chart from "./Chart";
import TabPanel from "./TabPanel";

export default class OilQualityMeasurements extends Component {
    constructor(props) {
        super(props);
        this.state = {
            oilQualityData: this.props.oilQualityData,
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
                    <Tab label="breakdown voltage"/>
                    <Tab label="water content"/>
                    <Tab label="acidity" />
                    <Tab label="color" />
                    <Tab label="interfacial tension" />
                </Tabs>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={0}
                >
                    <Chart 
                        xaxis={this.state.oilQualityData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.oilQualityData.map(obj => obj.breakdown_voltage),
                            label: "breakdown voltage"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={1}
                >
                    <Chart 
                        xaxis={this.state.oilQualityData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.oilQualityData.map(obj => obj.water_content),
                            label: "water content"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={2}
                >
                    <Chart 
                        xaxis={this.state.oilQualityData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.oilQualityData.map(obj => obj.acidity),
                            label: "acidity"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={3}
                >
                    <Chart 
                        xaxis={this.state.oilQualityData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.oilQualityData.map(obj => obj.color),
                            label: "color"
                        }}
                    />
                </TabPanel>
                <TabPanel 
                  value={this.state.tabDisplay} 
                  index={4}
                >
                    <Chart 
                        xaxis={this.state.oilQualityData.map(obj => obj.datestamp )} 
                        yaxis={{
                            data: this.state.oilQualityData.map(obj => obj.interfacial_tension),
                            label: "interfacial tension"
                        }}
                    />
                </TabPanel>
            </div>
        );
    }
}